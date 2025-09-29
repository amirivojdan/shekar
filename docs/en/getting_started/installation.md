# Installing shekar

## PyPI

You can install Shekar with pip. By default, the `CPU` runtime of ONNX is included.

<!-- termynal -->
```bash
$ pip install shekar
---> 100%
Successfully installed shekar!
```

If you want `GPU` acceleration, install with the gpu extra:

<!-- termynal -->
```bash
$ pip install "shekar[gpu]"
---> 100%
Successfully installed shekar!
```

**Notes:**

- The GPU extra installs onnxruntime-gpu (not available for macOS).
- If you are unsure which to pick, start with the default CPU install.
- Both CPU and GPU versions expose the same API, only performance differs depending on your hardware.