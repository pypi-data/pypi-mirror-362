'''
The version of the `ImputerAndDisentangler` where it only has the disengl part, and has two completely separate transformer modules for x_int and x_spl.
'''

import numpy as np
from enum import Enum
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch_geometric as pyg
from linformer_pytorch import Linformer, Padder

from .impanddisentgl import MaskLabel


class SubgraphEmbeddingDisentTwoSep(nn.Module):
    def __init__(self, num_genes, dim_embedding, dim_em_iscentralnode, num_celltypes, flag_use_int_u, flag_use_spl_u):
        '''
        :param num_genes: .
        :param dim_embedding: The dim of embedding for each cell, must be a multiple of 4.
        :param num_celltypes: dimension of the cell type vector (same as the niche vector).
        '''
        super(SubgraphEmbeddingDisentTwoSep, self).__init__()
        # grab args
        self.dim_embedding = dim_embedding
        self.dim_em_iscentralnode = dim_em_iscentralnode
        self.num_celltypes = num_celltypes
        self.flag_use_int_u = flag_use_int_u
        self.flag_use_spl_u = flag_use_spl_u

        assert(self.dim_embedding%4 == 0)
        # make internals
        self.encoder_x = nn.Linear(
            num_genes,
            dim_embedding,
            bias=True  # TODO: should it be False, or tunable?
        )  # the initial linear transformation on x (so pe can be added to it).
        self.embedding_iscentralnode = nn.Embedding(
            num_embeddings=2,
            embedding_dim=self.dim_em_iscentralnode
        )  # This emebedding tells whether the cell is among the central nodes returned by the Neighloader.
        '''
        self.embedding_blankorobserved = nn.Embedding(
            num_embeddings=2,
            embedding_dim=self.dim_em_blankorobserved
        )
        '''

    @torch.no_grad()
    def _position_encoding(self, batch, ten_xy_absolute:torch.Tensor):
        '''
        The positional embedding as done in cellplm paper.
        :return:
        '''
        ten_xy = ten_xy_absolute[batch.n_id.tolist(), :]+0.0  # [N, 2] where N is the size of subgraph.

        # min-max normaliztion to get xy in [0, 100]
        ten_xy = ten_xy - torch.min(ten_xy, 0).values.unsqueeze(0)  # [N, 2]
        ten_xy = ten_xy / torch.clamp(torch.max(ten_xy, 0).values.unsqueeze(0), min=0.0001, max=torch.inf) # [N, 2]
        ten_xy = 100.0*ten_xy  # [N,2] in [0,100]

        #  compute pe
        dby4 = self.dim_embedding//4
        denum = torch.exp(
            (torch.tensor(range(dby4)) / dby4) * np.log(10000.0)
        ).unsqueeze(0).to(ten_xy_absolute.device) # [1, dby4]
        x_sin = torch.sin(ten_xy[:, 0].unsqueeze(1) / denum)  # [N, bdy4]
        x_cos = torch.cos(ten_xy[:, 0].unsqueeze(1) / denum)  # [N, bdy4]
        y_sin = torch.sin(ten_xy[:, 1].unsqueeze(1) / denum)  # [N, bdy4]
        y_cos = torch.cos(ten_xy[:, 1].unsqueeze(1) / denum)  # [N, bdy4]
        pe = torch.cat(
            [x_sin, x_cos, y_sin, y_cos],
            1
        )  # [N, self.dim_embedding]
        return pe



    def forward(self, batch, prob_maskknowngenes:float, ten_xy_absolute:torch.Tensor):
        '''
        :param batch: the batch returned by pyg's neighborloader.
            - batch.x is a sparse matrix (e.g. adata.X).
            - batch.x must be raw counts (this function does log1p normalization) .
        :param prob_maskknowngenes: #TODO add the important documentation.
        :param ten_xy_absolute: the xy coordinates for the entire graph (not only the batch).
        :return:
        '''
        assert(ten_xy_absolute.size()[0] > batch.x.shape[0])
        x = torch.log(
            1.0 + batch.x.to_dense()
        ).to(ten_xy_absolute.device)
        ten_initmask = torch.tensor([False]*len(batch.y.tolist())).unsqueeze(0).to(ten_xy_absolute.device)
           # no imputation now --> no unobserved expvect. (batch.y == MaskLabel.UNKNOWN_TEST.value)
        with torch.no_grad():
            if torch.any(ten_initmask):
                x[ten_initmask, :] = x[ten_initmask, :] * 0  # to mask expressions kept for testing.
        xe = self.encoder_x(x)  # [N, dim_embedding]
        with torch.no_grad():
            if torch.any(ten_initmask):
                xe[ten_initmask, :] = xe[ten_initmask, :] * 0  # to mask expressions kept for testing.

        with torch.no_grad():
            pe = self._position_encoding(
                batch=batch,
                ten_xy_absolute=ten_xy_absolute
            ).detach()  # [N, dim_embedding]
            em_iscentralnode = self.embedding_iscentralnode(
                torch.tensor(
                    batch.batch_size * [1] + (x.size()[0] - batch.batch_size) * [0]
                ).to(ten_xy_absolute.device)
            ).detach()  # [N, 10]


            assert (
                batch.y.size()[1] == (batch.INFLOWMETAINF['dim_u_int'] + batch.INFLOWMETAINF['dim_u_spl'])
            )
            ten_u_int = batch.y[:, 0:batch.INFLOWMETAINF['dim_u_int']].to(ten_xy_absolute.device) if (self.flag_use_int_u) else None
            ten_u_spl = batch.y[:, batch.INFLOWMETAINF['dim_u_int']::].to(ten_xy_absolute.device) if (self.flag_use_spl_u) else None


            # define the masking token
            '''
            Note: Gene expression vectors are unknown in two cases
            - case 1. the expression vector is kept for testing.
            - case 2. the expression vector is known, but is kept hidden from the imputer.
                - done by setting to False with probability `prob_maskknowngenes`.
            In both cases the imputer must not be able to distinguish between the two.
            But the imputation loss is only defined on case 2.
            '''
            ten_masked_c1 = torch.tensor([False]*len(batch.y.tolist())).to(ten_xy_absolute.device)
              # no imputation now --> no unobserved expvect. (batch.y == MaskLabel.UNKNOWN_TEST.value).to(ten_xy_absolute.device)
            a = ~ten_masked_c1  # a; available expression vectors.
            a : torch.Tensor
            if torch.any(a) and (prob_maskknowngenes > 0.0):
                a[a == True] = a[a == True] & torch.tensor(
                    [np.random.rand() > prob_maskknowngenes for _ in range(torch.sum(a == True).tolist())]
                ).to(ten_xy_absolute.device)
            assert (torch.all(a))  # assert all expvects are available.
            '''
            em_blankorobserved = self.embedding_blankorobserved(
                a+0
            )  # [N, 10]
            '''
            ten_manually_masked = (~ten_masked_c1) & (~a)

            #mask xe
            if torch.any(~a):
                xe[~a, :] = xe[~a, :] * 0

        list_em_final = [xe+pe, em_iscentralnode]
        if self.flag_use_int_u:
            list_em_final.append(ten_u_int)
        if self.flag_use_spl_u:
            list_em_final.append(ten_u_spl)

        em_final = torch.cat(
            list_em_final,
            1
        )

        return em_final, ten_manually_masked



class DisentanglerTwoSep(nn.Module):
    def __init__(self, kwargs_genmodel, maxsize_subgraph, kwargs_em_intandspl, kwargs_tformer_int, kwargs_tformer_spl):
        '''
        :param maxsize_subgraph: the max size of the subgraph returned by pyg's NeighLoader.
        :param kwargs_em_intandspl: A single token embedding is used for both int and spl transformers.
        :param kwargs_tformer_int: other than `channels` and `input_size` which is determined by `maxsize_subgraph`
        :param kwargs_tformer_spl: other than `channels` and `input_size` which is determined by `maxsize_subgraph`

        '''
        super(DisentanglerTwoSep, self).__init__()

        # num_celltypes, flag_use_int_u, flag_use_spl_u

        self.num_celltypes = kwargs_em_intandspl['num_celltypes']
        self.flag_use_int_u = kwargs_em_intandspl['flag_use_int_u']
        self.flag_use_spl_u = kwargs_em_intandspl['flag_use_spl_u']

        # tfm_int
        dim_tf_int = kwargs_em_intandspl['dim_embedding'] + kwargs_em_intandspl['dim_em_iscentralnode']
        if self.flag_use_int_u:
            dim_tf_int += kwargs_genmodel['dict_varname_to_dim']['u_int']
        if self.flag_use_spl_u:
            dim_tf_int += kwargs_genmodel['dict_varname_to_dim']['u_spl']

        self.module_em_intandspl = SubgraphEmbeddingDisentTwoSep(**kwargs_em_intandspl)
        self.module_tf_int = Padder(
            Linformer(**{
                **{'input_size':maxsize_subgraph, 'channels':dim_tf_int},
                **kwargs_tformer_int
            })
        )

        # tfm_spl
        dim_tf_spl = dim_tf_int + 0
        self.module_tf_spl = Padder(
            Linformer(**{
                **{'input_size': maxsize_subgraph, 'channels': dim_tf_spl},
                **kwargs_tformer_spl
            })
        )

        # make the heads ===
        self.module_linearhead_muxint = nn.Sequential(
            nn.LeakyReLU(),
            nn.Linear(dim_tf_int, dim_tf_int),
            nn.LeakyReLU(),
            nn.Linear(dim_tf_int, kwargs_em_intandspl['num_genes'])
        )  # TODO: maybe add more layers to this head?
        self.module_linearhead_muxspl = nn.Sequential(
            nn.LeakyReLU(),
            nn.Linear(dim_tf_spl, dim_tf_spl),
            nn.LeakyReLU(),
            nn.Linear(dim_tf_spl, kwargs_em_intandspl['num_genes'])
        )  # TODO: maybe add more layers to this head?


        self.module_linearhead_sigmaxint = nn.Sequential(
            nn.LeakyReLU(),
            nn.Linear(dim_tf_int, kwargs_em_intandspl['num_genes'])
        )
        self.module_linearhead_sigmaxspl = nn.Sequential(
            nn.LeakyReLU(),
            nn.Linear(dim_tf_spl, kwargs_em_intandspl['num_genes'])
        )
        self._check_args()

    def _check_args(self):
        pass

    def forward(self, batch, prob_maskknowngenes:float, ten_xy_absolute:torch.Tensor):
        '''
        :param batch:
        :param prob_maskknowngenes: must be zero for `Disentangler`, this arg is kept for consistency.
        :param ten_xy_absolute:
        :return:
        '''
        assert(prob_maskknowngenes == 0.0)
        x_log1p = torch.log(
            1.0 + batch.x.to_dense()  # TODO: how to make sure that batch.x contains the count data ???
        ).to(ten_xy_absolute.device)
        x_cnt = batch.x.to_dense().to(ten_xy_absolute.device).detach() + 0.0

        # pass to tf_int and tf_spl
        ten_in_tf_bothintspl, ten_manually_masked = self.module_em_intandspl(
            batch=batch,
            prob_maskknowngenes=0.0,
            ten_xy_absolute=ten_xy_absolute
        )  # [N, dim_tf1], [N]
        ten_out_tf_int = self.module_tf_int(ten_in_tf_bothintspl.unsqueeze(0))[0, :, :]  # [N, dim_tf1] in [-inf, inf]
        ten_out_tf_spl = self.module_tf_spl(ten_in_tf_bothintspl.unsqueeze(0))[0, :, :]  # [N, dim_tf1] in [-inf, inf]

        assert (not torch.any(ten_manually_masked))
        loss_imputex = None
        ten_out_imputer = 0.0



        # compute muxint, muxspl
        with torch.no_grad():
            oneon_x_nonzero = (x_cnt > 0.0) + 0  # [N, num_genes]

        muxint = torch.clamp(
            self.module_linearhead_muxint(ten_out_tf_int) * oneon_x_nonzero,
            min=0.00001 * torch.ones_like(x_cnt),  # TODO: maybe tune?
            max=x_cnt
        )  # [N, num_genes]
        muxspl = torch.clamp(
            self.module_linearhead_muxspl(ten_out_tf_spl) * oneon_x_nonzero,
            min=0.00001 * torch.ones_like(x_cnt),  # TODO: maybe tune?
            max=x_cnt
        )  # [N, num_genes]




        # compute sigmaxint, sigmaxspl
        sigmaxint = torch.clamp(
            self.module_linearhead_sigmaxint(ten_out_tf_int),
            min=0.00001,  # TODO: maybe tune?
            max=torch.inf
        )  # [N, num_genes]
        sigmaxspl = torch.clamp(
            self.module_linearhead_sigmaxspl(ten_out_tf_spl),
            min=0.00001,  # TODO: maybe tune?
            max=torch.inf
        )  # [N, num_genes]
        return dict(
            muxint=muxint,
            muxspl=muxspl,
            sigmaxint=sigmaxint,
            sigmaxspl=sigmaxspl,
            ten_out_imputer=ten_out_imputer + 0.0,
            loss_imputex=loss_imputex
        )





