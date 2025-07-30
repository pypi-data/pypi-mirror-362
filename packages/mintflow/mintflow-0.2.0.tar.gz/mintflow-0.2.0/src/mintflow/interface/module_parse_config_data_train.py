import copy
import os, sys
import yaml
import importlib
import importlib.resources
from .. import data
from ..data import default_config_files


def _errormsg_config_data(fname_config_data, key_raisederror):
    toret = "An error occured when trying to access {} from the config file {}.\n".format(
        key_raisederror,
        fname_config_data
    )
    toret = toret + "Please refer to TODO: for sample file config_data_train.yml, and double check the config file that you have provided {}.".format(
        fname_config_data
    )
    return toret


# ..data.default_config_files
def get_defaultconfig_data_train(num_tissue_sections):
    """
    Returns the default file for `config_data_train.yml`
    :param num_tissue_sections: number of tissue sections.
    :return:
    """
    f = importlib.resources.open_binary(
        "mintflow.data.default_config_files",
        "config_data_train.yml"
    )
    try:
        config_data_train = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        print("Something went wrong when attempting to read the default `config_data_train.yml.`")
        print(exc)

    for idx_new_slice in range(num_tissue_sections-1):
        config_data_train['list_tissue']['anndata{}'.format(idx_new_slice+2)] = copy.deepcopy(config_data_train['list_tissue']['anndata1'])
        config_data_train['list_tissue']['anndata{}'.format(idx_new_slice + 2)]['file'] = config_data_train['list_tissue']['anndata{}'.format(idx_new_slice + 2)]['file'].replace(
            "adata_1.h5ad",
            "adata_{}.h5ad".format(idx_new_slice + 2)
        )

    return config_data_train






def verify_and_postprocess_config_data_train(dict_config_data, fname_config_data=""):

    # load config_data_train.yml
    # with open(fname_config_data, 'rb') as f:
    #     try:
    #         dict_config_data = yaml.safe_load(f)
    #     except yaml.YAMLError as exc:
    #         print(exc)
    #         raise Exception(
    #             "Something went wrong when reading the config file for training. (backtrace printed above).\n" +
    #             "Please refer to TODO: for sample file config_data_train.yml"
    #         )

    # check the structure of config_data.yaml ================================
    if set(dict_config_data.keys()) != {'list_tissue'}:
        raise Exception(
            _errormsg_config_data(
                fname_config_data=fname_config_data,
                key_raisederror='list_tissue'
            )
        )

    num_samples = len(dict_config_data['list_tissue'].keys())

    if list(dict_config_data['list_tissue'].keys()) != ['anndata{}'.format(s + 1) for s in range(num_samples)]:
        raise Exception(
            "An error occured when attempting to read [anndata1, ...,  anndata{}] from the provided config data file {}.\n".format(
                num_samples,
                fname_config_data
            ) + "Please refer to TODO: for sample file config_data_train.yml"
        )

    set_keys_eachanndata = {
        'file',
        'obskey_cell_type',
        'obskey_sliceid_to_checkUnique',
        'obskey_x',
        'obskey_y',
        'obskey_biological_batch_key',
        'config_neighbourhood_graph',
        'config_dataloader_train',
        'config_sq_pl_spatial_scatter',
        'batchsize_compute_NCC'
    }
    for idx_sample, key_sample in enumerate(['anndata{}'.format(s + 1) for s in range(num_samples)]):
        if key_sample != 'anndata{}'.format(idx_sample + 1):
            raise Exception(
                _errormsg_config_data(
                    fname_config_data=fname_config_data,
                    key_raisederror=key_sample
                )
            )

        if set(dict_config_data['list_tissue'][key_sample].keys()) != set_keys_eachanndata:
            raise Exception(
                _errormsg_config_data(
                    fname_config_data=fname_config_data,
                    key_raisederror=" some fields under {}.".format(key_sample)
                )
            )

    # Fished checking the config file
    # Now parse the config file and return a list of dicts ===
    list_toret = []
    for idx_sample, key_sample in enumerate(['anndata{}'.format(s + 1) for s in range(num_samples)]):
        list_toret.append(
            dict_config_data['list_tissue'][key_sample]
        )

    return list_toret




