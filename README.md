# idr_torch

## Description

Permet de récupérer les variables SLURM afin de gérér le multi-GPU/multi-noeuds pour le parallélisme sur Pytorch.

```python
import torch.distributed as dist
import idr_torch

if idr_torch.rank == 0:
    print(">>> Training on ", len(idr_torch.hostnames), " nodes and ", idr_torch.size, " processes") 

dist.init_process_group(backend='nccl', 
                        init_method='env://', 
                        world_size=idr_torch.size, 
                        rank=idr_torch.rank)
```


Si on veut rajouter une nouvelle API, on peut la mettre dans le dossier `api` et l'importer dans le `__init__.py`. Ou alors on peut la coder n'importe où, et après appeler `idr_torch.register_api(nouvelle_api)`.
Les nouvelles APIs doivent hériter de `idr_torch.API`. Si on veut faire en sorte que la MASTER_ADDR et le MASTER_PORT soit mis automatiquement (dans le cas où le lanceur ne le fait pas comme SLURM), alors il faut utiliser `idr_torch.AutoMasterAddressPort` comme métaclasse de notre nouvelle API.

On patche aussi le profiler. Il suffit de remplacer `from torch.profiler import ...` par `from idr_torch.profiler import ...`.

Note : idr_torch est compatible avec submitit.

## Installation

### With [idr-pypi](https://idrforge.prive.idris.fr/assistance/outils/idr_pypi) 🐍 (by default)

```bash
pip install idris[torch]
```

### Master from [idr-pypi](https://idrforge.prive.idris.fr/assistance/outils/idr_pypi) 🐍

```bash
pip install idris-nightly[torch]
```

### From source

```bash
git clone https://idrforge.prive.idris.fr/assistance/outils/idr_torch.git
cd idr_torch
pip install .
```
