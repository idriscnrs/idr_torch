#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import atexit
import inspect
import os
import signal
import subprocess
import warnings
from functools import cached_property, wraps
from textwrap import dedent
from typing import Any, Callable

from IPython import get_ipython

import idr_torch

try:
    import ipyparallel as ipp
    import ipyparallel.client.magics as ipp_magics
except ImportError:
    IPYPARALLEL_AVAILABLE = False
else:
    IPYPARALLEL_AVAILABLE = True


__spec__ = None
__IS_MASTER__: bool = True

def getsource(func: Callable, /, ignore_first_n_lines: int = 0) -> str:
    src = inspect.getsource(func)
    while ignore_first_n_lines > 0:
        src = src[src.find("\n") + 1:]
        ignore_first_n_lines -= 1
    return dedent(src)
        

def dependent_on_ipyparallel(func: Callable) -> Callable:

    if IPYPARALLEL_AVAILABLE:
        return func
    else:
        warnings.warn(
            message=(
                "ipyparallel is not available so idr_torch.notebook cannot be used. "
                "To use it, install it. For instance with\n"
                "\t- pip install ipyparallel\n"
                "\t- pip install idr_torch[notebook]\n"
                "This functionality is currently a no-op."
            ),
        )
        @wraps(func)
        def wrapper(*args, **kwargs):
            pass
        return wrapper

def only_if_launched(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(self: "ParallelInterface", *args, **kwargs) -> Callable:
        if self.launched:
            return func(self, *args, **kwargs)
        else:
            raise RuntimeError(
                "Distributed execution has not been set up yet. "
                "You should call idr_torch.notebook.launch"
            )
    return wrapper


def only_on_master(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(self: "ParallelInterface", *args, **kwargs) -> Callable:
        if __IS_MASTER__:
            return func(self, *args, **kwargs)
        else:
            raise RuntimeError(
                "This function is only available on the master process but "
                "you are in distributed mode. Use `%autopx` to disable it."
            )
    return wrapper

class ParallelInterface():

    def __init__(self):
        super().__init__()
        self.rc = None
        self.launched = False
        self.setup_signal_handlers()
        self.controller_process = None
        self.engine_process = None

    @cached_property
    def host(self) -> str:
        with warnings.catch_warnings(action="ignore", category=idr_torch.IdrTorchWarning):
            return idr_torch.hostname

    @cached_property
    def num_engines(self) -> int:
        return int(os.environ["SLURM_NTASKS"])

    @cached_property
    def cluster_id(self) -> str:
        return f"cluster_{self.num_engines}"

    @cached_property
    def ipp_magics_manager(self) -> "ipp_magics.ParallelMagics":
        ipython = get_ipython()
        return ipython.magics_manager.magics["line"]["autopx"].__self__

    def kill_process(self, process: subprocess.Popen) -> None:
        if process and process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
        return None

    @dependent_on_ipyparallel
    @only_if_launched
    @only_on_master
    def cleanup(self):
        if self.launched:
            if self.rc is not None:
                self.rc.shutdown()
                self.rc = None

            self.controller_process = self.kill_process(self.controller_process)
            self.engine_process = self.kill_process(self.engine_process)
            self.launched = False

    def setup_signal_handlers(self):
        def handler(signum, frame):
            self.cleanup()
            signal.signal(signum, signal.SIG_DFL)
            os.kill(os.getpid(), signum)

        atexit.register(self.cleanup)
        signal.signal(signal.SIGTERM, handler)
        signal.signal(signal.SIGINT, handler)

    def launch_controller(self) -> None:
        self.controller_process = subprocess.Popen(
            ["ipcontroller", "--ip", self.host, "--cluster-id", self.cluster_id],
            stderr=subprocess.PIPE,
        )
        buffer_accumulator = ""
        while True:
            new_output = self.controller_process.stderr.read(1).decode('utf-8')
            if new_output == "\n":
                if "subscription started" in buffer_accumulator:
                    break
            else:
                buffer_accumulator += new_output
        print("Controller started")

    def launch_engines(self) -> None:
        self.engine_process = subprocess.Popen(
            ["srun", "ipengine", "--cluster-id", self.cluster_id],
            stderr=subprocess.PIPE,
        )
        buffer_accumulator = ""
        num_registered_engines = 0
        while True:
            new_output = self.engine_process.stderr.read(1).decode('utf-8')
            if new_output == "\n":
                if "Completed registration" in buffer_accumulator:
                    num_registered_engines += 1
                    if num_registered_engines == int(os.environ["SLURM_NTASKS"]):
                        break
            else:
                buffer_accumulator += new_output
        print("All Engines started")

    def launch_client(self) -> ipp.Client:
        self.rc = ipp.Client(cluster_id=self.cluster_id)
        self.rc.wait_for_engines(n=self.num_engines, interactive=False)

    @staticmethod
    def on_client_start() -> None:
        import idr_torch.notebook

        idr_torch.notebook._parallel_interface.launched = True
        idr_torch.notebook.__IS_MASTER__ = False

    @dependent_on_ipyparallel
    def launch(self) -> None:
        self.launch_controller()
        self.launch_engines()
        self.launch_client()
        on_client_start = getsource(self.on_client_start, ignore_first_n_lines=2)
        self.ipp_magics_manager.parallel_execute(on_client_start)
        self.launched = True
        self.enable()

    @dependent_on_ipyparallel
    @only_if_launched
    def enable(self) -> None:
        self.ipp_magics_manager._enable_autopx()

    @dependent_on_ipyparallel
    @only_if_launched
    @only_on_master
    def push(self, D: dict[str, Any] = {}, **kwargs: Any) -> None:
        _dict: dict[str, Any] = {}
        _dict.update(D)
        _dict.update(kwargs)
        self.rc[:].push(_dict)

    @dependent_on_ipyparallel        
    @only_if_launched
    @only_on_master
    def pull(self, *names: str) -> dict[str, list[Any]]:
        gathered = self.rc[:].pull(names, block=True)
        output: dict[str, list[Any]] = {}
        for idx, name in enumerate(names):
            output[name] = []
            for rank in range(len(gathered)):
                output[name].append(gathered[rank][idx])
        return output


_parallel_interface = ParallelInterface()

enable = _parallel_interface.enable
launch = _parallel_interface.launch
push = _parallel_interface.push
pull = _parallel_interface.pull
cleanup = _parallel_interface.cleanup
