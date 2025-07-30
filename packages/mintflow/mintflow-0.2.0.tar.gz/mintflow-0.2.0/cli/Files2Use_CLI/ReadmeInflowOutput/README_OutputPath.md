

This folder contains
- `adata_inflowOutput_norm.h5ad`:
    - Inflow predictions are placed in `adata.obs` and `adata.uns`.
    - This is the anndata "after" applying `sc.pp.normalize_total` where `adata.X` is row normalised --> inflow predictions `Xint` and `Xspl` (i.e. `muxint` and `muxspl`) sum up to the normalised version of `adata.X`.
- `adata_inflowOutput_unnorm.h5ad`:
  - Inflow predictions are placed in `adata.obs` and `adata.uns`.
  - This is the anndata "before" applying `sc.pp.normalize_total` where `adata.X` is not row normalised --> inflow predictions `Xint` and `Xspl` (i.e. `muxint` and `muxspl`) sum up to the un-normalised version of `adata.X`.
- `log_inflow_module.txt`: contains inflwo pytorch modules whereby one can inspect the architecture of each submodule.
- Different subfolders: Each subfolder contains a separate README.md file. Please refer to those files for info about each folder.

