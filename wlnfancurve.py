import pynvml
import argparse
import configparser
import json
import time
import ctypes
import signal
import sys

from nvml_context import manage_nvml, manage_fans, GpuInfo


class UnsupportedDriverVersion(Exception):
    pass


def main():
    def sigterm_handler(signum, frame):
        sys.exit()

    signal.signal(signal.SIGTERM, sigterm_handler)

    parser = argparse.ArgumentParser(
        prog='wlnfancurve',
        description='Control Nvidia GPU fan speed in Wayland'
    )
    parser.add_argument('-c', '--config', default='./config', help='configuration file (default: ./config)')
    args = parser.parse_args()

    config = configparser.ConfigParser()
    config.read(args.config)

    interval = int(config['time']['interval'])
    hysteresis = int(config['time']['hysteresis'])

    fan_curve = json.loads(config['curve']['fan_curve'])
    temp_curve = json.loads(config['curve']['temp_curve'])
    if len(fan_curve) != len(temp_curve):
        raise ValueError("Fan curve and temp curve don't match")

    with manage_nvml():
        major = int(pynvml.nvmlSystemGetDriverVersion().split('.')[0])
        if major < 520:
            raise UnsupportedDriverVersion('Driver version is lower than 520')

        with manage_fans() as gpus:
            while True:
                for gpu in gpus:
                    control_speed(gpu, hysteresis, fan_curve, temp_curve)
                time.sleep(interval)


def control_speed(gpu: GpuInfo, hysteresis: int,
                  fan_curve: list, temp_curve: list) -> int:
    current_temp = pynvml.nvmlDeviceGetTemperature(gpu.handle, pynvml.NVML_TEMPERATURE_GPU)
    if abs(current_temp - gpu.last_temp) < hysteresis:
        return

    for probe_speed, probe_temp in zip(fan_curve, temp_curve):
        if current_temp <= probe_temp:
            set_fan_speed(gpu, probe_speed, current_temp)
            return

    set_fan_speed(gpu, 100, current_temp)  # 100% speed for higher temps


def set_fan_speed(gpu: GpuInfo, speed: int, current_temp: int):
    for i in range(gpu.nfans):
        current_speed = pynvml.nvmlDeviceGetFanSpeed_v2(gpu.handle, i)
        if speed != current_speed:
            if speed < gpu.min_speed:
                pynvml.nvmlDeviceSetDefaultFanSpeed_v2(gpu.handle, i)
            else:
                pynvml.nvmlDeviceSetFanSpeed_v2(gpu.handle, i, speed)
            gpu.last_temp = current_temp
            print(f"Fan {i} speed set to:", speed)


if __name__ == '__main__':
    main()
