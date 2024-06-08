# wlnfancurve

This is a simplified implementation of [nfancurve](https://github.com/nan0s7/nfancurve) for Wayland-based DEs and compositors. Nfancurve depends on X11's `nvidia-settings` and thus doesn't work under Wayland. This implementation is based on [NVML GPU Control](https://github.com/HackTestes/NVML-GPU-Control) by HackTestes and uses NVIDIA Management Library (NVML) [Python bindings (pynvml)](https://pypi.org/project/nvidia-ml-py/).

## Supported hardware

- NVIDIA GPUs supported by a proprietary driver version >= 520

## Why this exists?

NVML GPU Control is too complex and has many features that I don't really need, like Windows compatibility. This is a stripped down, really basic version, more similar to the nfancurve bash script.

## Installation

1. Clone the repo

```bash
git clone https://github.com/xiyori/wlnfancurve
cd wlnfancurve
```

2. Create a Python virtual environment and install dependencies

```bash
python -m venv nvml
source nvml/bin/activate  # or activate.fish for fish
pip install nvidia-ml-py
```

## How to use

The config file specifies some global parameters and a fan curve. Please refer to the [file](config) for more info. The script supports multiple GPUs, but the curve is shared among all of them.

After editing the config run the script with admin privileges

```bash
python wlnfancurve.py  # put sudo here
```

(Optional) Run the script at boot by installing a systemd unit. Copy configuration and service files

```bash
cp config /etc/wlnfancurve.conf
cp wlnfancurve.service /usr/lib/systemd/system/
```

Inspect the copied service file and change paths for your user. Enable / start the service

```bash
systemctl enable wlnfancurve.service
```
