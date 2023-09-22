#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
from typing import List, Union

from .base import API
from .modifiers import AutoMasterAddressPort


@AutoMasterAddressPort
class SlurmAPI(API):
    priority: int = 10000
    name: str = "Slurm"

    def is_launcher(self) -> bool:
        return "SLURM_STEP_ID" in os.environ

    def rank(self) -> int:
        return int(os.environ["SLURM_PROCID"])

    def local_rank(self) -> int:
        return int(os.environ["SLURM_LOCALID"])

    def world_size(self) -> int:
        return int(os.environ["SLURM_STEP_NUM_TASKS"])

    def local_world_size(self) -> int:
        lws = os.environ["SLURM_STEP_TASKS_PER_NODE"]
        lws = lws.split("(")[0]
        return int(lws)

    def num_nodes(self) -> int:
        return int(os.environ["SLURM_STEP_NUM_NODES"])

    def cpus(self) -> int:
        cpu = int(os.environ.get("SLURM_CPUS_PER_TASK", 0))
        return cpu or len(os.sched_getaffinity(0))

    def gpus(self) -> List[str]:
        step_gpus = os.environ.get("SLURM_STEP_GPUS", None)
        if step_gpus is not None:
            return step_gpus.split(",")
        return []

    def nodelist(self) -> Union[List[str], str]:
        compact_nodelist = os.environ["SLURM_STEP_NODELIST"]
        try:
            from hostlist import expand_hostlist
        except ImportError:
            return compact_nodelist
        else:
            return expand_hostlist(compact_nodelist)

    @staticmethod
    def get_first_host(hostlist: str) -> str:
        """
        Get the first host from SLURM's nodelist.
        Example: Nodelist="Node[1-5],Node7" -> First node: "Node1"
        Args:
            hostlist(str): the compact nodelist as given by SLURM
        Returns:
            (str): the first node to host the master process
        """
        from re import findall, split, sub

        regex = "\[([^[\]]*)\]"
        all_replacement: list[str] = findall(regex, hostlist)
        new_values = [split("-|,", element)[0] for element in all_replacement]
        for i in range(len(new_values)):
            hostlist = sub(regex, new_values[i], hostlist, count=1)
        return hostlist.split(",")[0]

    def master_address(self) -> str:
        nodelist = self.nodelist()
        if isinstance(nodelist, list):
            return nodelist[0]
        return self.get_first_host(nodelist)

    def jobid(self) -> int:
        return int(os.environ["SLURM_JOB_ID"])

    def port(self) -> int:
        return 10000 + self.jobid() % 20000
