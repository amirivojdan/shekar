# Installing shekar

## PyPI

You can install Shekar with pip. By default, the `CPU` runtime of ONNX is included, which works on all platforms.

### CPU Installation (All Platforms)

<!-- termynal -->
```bash
$ pip install shekar
---> 100%
Successfully installed shekar!
```
This works on **Windows**, **Linux**, and **macOS** (including Apple Silicon M1/M2/M3).

### GPU Acceleration (NVIDIA CUDA)
If you have an NVIDIA GPU and want hardware acceleration, you need to replace the CPU runtime with the GPU version.

**Prerequisites**

- NVIDIA GPU with CUDA support
- Appropriate CUDA Toolkit installed
- Compatible NVIDIA drivers

<!-- termynal -->
```bash
$ pip install shekar \
  && pip uninstall -y onnxruntime \
  && pip install onnxruntime-gpu
---> 100%
Successfully installed shekar!
```