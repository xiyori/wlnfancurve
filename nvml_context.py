import pynvml
import ctypes

from dataclasses import dataclass
from contextlib import contextmanager


class GpuNotFound(Exception):
    pass


@dataclass
class GpuInfo:
    handle: object
    nfans: int
    min_speed: int
    last_temp: int = 0


@contextmanager
def manage_nvml():
    pynvml.nvmlInit()
    print("NVML init")
    try:
        yield None
    finally:
        pynvml.nvmlShutdown()
        print("NVML shutdown")


@contextmanager
def manage_fans():
    ngpus = pynvml.nvmlDeviceGetCount()
    if ngpus == 0:
        raise GpuNotFound("No GPUs detected")
    print("Number of GPUs detected:", ngpus)
    print()
    gpus = []
    for i in range(ngpus):
        handle = pynvml.nvmlDeviceGetHandleByIndex(i)
        nfans = pynvml.nvmlDeviceGetNumFans(handle)
        fan_min = ctypes.c_uint(0)
        fan_max = ctypes.c_uint(0)
        pynvml.nvmlDeviceGetMinMaxFanSpeed(handle, ctypes.byref(fan_min), ctypes.byref(fan_max))
        min_speed = fan_min.value
        gpus.append(GpuInfo(handle, nfans, min_speed))
        print("GPU", i)
        print("    Number of fans detected:", nfans)
        print("    Min speed detected:", min_speed)
        print()
    try:
        yield gpus
    finally:
        for gpu in gpus:
            for i in range(gpu.nfans):
                pynvml.nvmlDeviceSetDefaultFanSpeed_v2(gpu.handle, i)
        print("Fan control set back to auto mode")
