# 📊 PySysMetrics

**PySysMetrics** is a lightweight Python package and CLI tool that monitors memory usage (CPU & GPU) of active Python processes. Ideal for profiling and debugging resource consumption in machine learning or long-running data workflows.


## 📦 Installation

Install via pip:

```bash
pip install pysysmetrics
```


## 🚀 Features

* 📈 Monitor **CPU memory usage** for all Python processes.
* 🔥 Track **GPU memory usage** (via NVIDIA NVML).
* ⏱️ Configurable interval for periodic monitoring.
* 🧪 Minimal dependencies, easy to integrate in workflows.
* ✅ Works on Linux, macOS, and Windows (CPU only).


## 🛠️ Usage

Run the CLI directly after installing:

```bash
pysysmetrics --cpu 2
```

### Available Options

| Flag      | Description                          | Example   |
| --------- | ------------------------------------ | --------- |
| `--cpu N` | Monitor CPU memory every `N` seconds | `--cpu 5` |
| `--gpu N` | Monitor GPU memory every `N` seconds | `--gpu 3` |

### Examples

```bash
# Monitor CPU memory every 2 seconds
pysysmetrics --cpu 2

# Monitor GPU memory every 5 seconds
pysysmetrics --gpu 5
```

If no arguments are passed, a help message is displayed:

```bash
pysysmetrics
```


## 📚 Python API

You can also use `pysysmetrics` programmatically in your own Python scripts:

```python
from pysysmetrics.core import cpu, gpu

# Monitor CPU usage every 3 seconds
cpu.monitor_cpu_memory(interval=3)

# Monitor GPU usage every 2 seconds
gpu.monitor_gpu_memory(interval=2)
```


## 🔧 Requirements

* Python 3.7 or later

## 📌 Notes

* **GPU monitoring** requires:

  * NVIDIA GPU with drivers installed
  * Working `nvidia-smi`
  * Python bindings for NVML (`pynvml`)