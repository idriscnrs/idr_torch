# Releases

## 2.0.0
*August 2023*

This release is a full rewrite of the library.

#### New features

- More data is available (local world size, master port, master address, etc).
- Data is now evaluated at runtime.
- Fixes an issue where the package would not work without a SLURM environment.
- Added new torchrun backend.
- Fixes an issue where the package was not pickable for submitit to use.


## 1.0.0
*Date unknown*

This release contains the first version of idr_torch. In this version, all available data (rank, world_size, etc) is evaluated during the import and is not updated. This does not support usage in any environment other than SLURM.
