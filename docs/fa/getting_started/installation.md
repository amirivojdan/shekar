# نصب shekar

## نصب از PyPI

می‌توانید کتابخانهٔ شِکَر را با `pip` نصب کنید. به‌صورت پیش‌فرض، نسخهٔ `CPU` از ONNX نصب می‌شود که روی همهٔ پلتفرم‌ها کار می‌کند.

### نصب نسخهٔ CPU (همهٔ پلتفرم‌ها)

<!-- termynal -->
```bash
$ pip install shekar
---> 100%
Successfully installed shekar!
```

این روش روی **Windows**، **Linux** و **macOS** (از جمله Apple Silicon مانند M1/M2/M3) قابل استفاده است.

### شتاب‌دهی با GPU (NVIDIA CUDA)

اگر کارت گرافیک NVIDIA دارید و می‌خواهید از شتاب سخت‌افزاری استفاده کنید، باید نسخهٔ CPU را با نسخهٔ GPU جایگزین کنید.

**پیش‌نیازها**

- کارت گرافیک NVIDIA با پشتیبانی CUDA
- نصب CUDA Toolkit سازگار
- نصب درایورهای سازگار NVIDIA

<!-- termynal -->
```bash
$ pip install shekar \
  && pip uninstall -y onnxruntime \
  && pip install onnxruntime-gpu
---> 100%
Successfully installed shekar!
```
