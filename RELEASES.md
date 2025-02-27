# Releases

## 2.4.0
*February 2025*

- Solved an issue where importing could fail in Jupyter notebook because of \_\_spec\_\_.
- Added a cleanup function because why the hell not!


## 2.3.0
*February 2025*

- Added idr_torch.notebook for easy multi-node notebooks on slurm clusters.
- Switched from setup.py to pyproject.toml.
- Use Github actions to auto-publish on release to pypi.


## 2.2.0
*July 2024*

- Confusing aliases were removed.
- Added a summary for the distributed environment.
- New method: init_process_group. Initializes torch distributed environment via `torch.distributed.init_process_group` and returns the correct device.


## 2.1.0
*February 2024*

- Slurm and Default APIs now also set the following environment variables: RANK, LOCAL_RANK, WORLD_SIZE, LOCAL_WORLD_SIZE. It should allow torch to initialize only with environment variables.
- New API Endpoint: idr_torch.device gives a torch CUDA device if possible, otherwise a torch CPU device.


## 2.0.1
*September 2023*

#### Bugs corrected

- Solved an issue where the local world size could not be extracted correctly as the new version of SLURM provides the number of nodes in a multi-node with the following pattern `<local_world_size>(x<nnodes>)`


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
