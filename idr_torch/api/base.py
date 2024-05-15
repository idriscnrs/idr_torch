#! /usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import List, Union, TYPE_CHECKING

if TYPE_CHECKING:
    import torch


def keep_as_func(func: callable) -> callable:
    setattr(func, "__keep_as_func__", True)
    return func


class API(ABC):
    priority: int = 5000
    name: str = "AbstractAPI"

    @abstractmethod
    def is_launcher(self) -> bool:
        """
        Detects if the given API is the one used to launch the current job.
        """
        raise NotImplementedError()

    @abstractmethod
    def rank(self) -> int:
        """
        Property containing the rank of the process.
        """
        raise NotImplementedError()

    @abstractmethod
    def local_rank(self) -> int:
        """
        Property containing the local rank of the process.
        """
        raise NotImplementedError()

    @abstractmethod
    def world_size(self) -> int:
        """
        Property containing the number of processes launched.
        """
        raise NotImplementedError()

    @abstractmethod
    def local_world_size(self) -> int:
        """
        Property containing the number of processes launched of each node.
        """
        raise NotImplementedError()

    @abstractmethod
    def num_nodes(self) -> int:
        """
        Property containing the number of nodes.
        """
        raise NotImplementedError()

    @abstractmethod
    def cpus(self) -> int:
        """
        Property containing the number of CPUs allocated to each process.
        """
        raise NotImplementedError()

    @abstractmethod
    def gpus(self) -> List[str]:
        """
        Property containing all GPUs ids.
        """
        raise NotImplementedError()

    @abstractmethod
    def nodelist(self) -> Union[str, List[str]]:
        """
        Property containing the list of nodes.
        """
        raise NotImplementedError()

    @abstractmethod
    def master_address(self) -> str:
        """
        Property containing the master node.
        """
        raise NotImplementedError()

    @abstractmethod
    def port(self) -> int:
        """
        Property containing the port to communicate with the master process.
        """
        raise NotImplementedError()

    def is_master(self) -> bool:
        """
        Detects whether the process is the master (i.e. the rank 0).
        """
        return self.rank() == 0

    def device(self) -> "torch.device":
        import torch

        if torch.cuda.is_available():
            return torch.device(f"cuda:{self.local_rank()}")
        else:
            return torch.device("cpu")

    @keep_as_func
    def init_process_group(self, *args, **kwargs) -> "torch.device":
        import torch.distributed as dist
        _kwargs = dict(rank=self.rank(), world_size=self.world_size())
        _kwargs.update(**kwargs)
        dist.init_process_group(*args, **kwargs)
        return self.device()
