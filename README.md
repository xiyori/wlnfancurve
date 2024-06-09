# wlnfancurve

This is a simplified implementation of [nfancurve](https://github.com/nan0s7/nfancurve) for Wayland-based DEs and compositors. Nfancurve depends on X11's `nvidia-settings` and thus doesn't work under Wayland. This implementation is based on [NVML GPU Control](https://github.com/HackTestes/NVML-GPU-Control) by HackTestes and uses NVIDIA Management Library (NVML) [Python bindings (pynvml)](https://pypi.org/project/nvidia-ml-py/).

## Supported hardware

- NVIDIA GPUs supported by a proprietary driver version >= 520

## Why this exists?

NVML GPU Control is too complex and has many features that I don't really need, like Windows compatibility. This is a stripped down, really basic version, more similar to the nfancurve bash script.

## Installation

On Arch Linux, [wlnfancurve](https://aur.archlinux.org/packages/wlnfancurve) AUR package is available; install it with your favorite AUR helper. Inspect and edit `/etc/wlnfancurve.conf` and enable / start a systemd `wlnfancurve.service`.

### Manual install

1. Clone the repo

```bash
git clone https://github.com/xiyori/wlnfancurve
cd wlnfancurve
```

2. Install the latest NVIDIA proprietary driver. Create a Python virtual environment and install dependencies

```bash
python -m venv nvml
source nvml/bin/activate  # or activate.fish for fish
pip install nvidia-ml-py
```

Alternatively, install the package directly in the system Python (not recommended).

## How to use

The config file specifies some global parameters and a fan curve. Please refer to the [file](config) for more info. The script supports multiple GPUs, but the curve is shared among all of them.

After editing the config run the script with admin privileges

#### AUR version

```bash
systemctl start wlnfancurve.service
```

#### Manual

```bash
python wlnfancurve.py
```

## (Optional) Run the script at boot by installing a systemd unit

#### AUR version

There is no need to copy anything, simply enable `wlnfancurve.service`.

#### Manual

Install `nvidia-ml-py` package in the system Python. It is recommended to use your distro's package manager instead of `pip`. Copy script, configuration and service files (admin privileges required)

```bash
mkdir /usr/bin/wlnfancurve
cp {wlnfancurve.py,nvml_context.py} /usr/bin/wlnfancurve/
cp config /etc/wlnfancurve.conf
cp wlnfancurve.service /usr/lib/systemd/system/
```

Enable / start the service

```bash
systemctl enable wlnfancurve.service
```
