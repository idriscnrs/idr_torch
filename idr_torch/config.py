#! /usr/bin/env python
# -*- coding: utf-8 -*-

from .api.base import API

# Endpoints redirection
rank = API.rank
local_rank = API.local_rank
world_size = API.world_size
local_world_size = API.local_world_size
num_nodes = API.num_nodes
cpus = API.cpus
gpu_ids = API.gpus
nodelist = API.nodelist
master_addr = API.master_address
master_port = API.port
is_master = API.is_master
device = API.device
init_process_group = API.init_process_group
hostname = API.hostname

# Aliases
ntasks = world_size
size = world_size
local_size = local_world_size
ntasks_per_node = local_world_size
nnodes = num_nodes
cpus_per_task = cpus
master_address = master_addr
init_pg = init_process_group
init = init_process_group


__all__ = [
    "rank",
    "local_rank",
    "world_size",
    "local_world_size",
    "num_nodes",
    "cpus",
    "gpu_ids",
    "nodelist",
    "master_addr",
    "master_port",
    "ntasks",
    "size",
    "local_size",
    "ntasks_per_node",
    "nnodes",
    "cpus_per_task",
    "master_address",
    "is_master",
    "device",
    "init_process_group",
    "init_pg",
    "init",
    "hostname",
]
