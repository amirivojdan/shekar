import os

import onnxruntime as ort


def get_onnx_providers() -> list[str]:
    """
    Get the list of available ONNX Runtime execution providers, prioritizing GPU providers if available.
    This function checks for the presence of various execution providers and returns a list ordered by preference.
    Returns:
        list: A list of available ONNX Runtime execution providers ordered by preference.
    """

    PREFERRED = [
        "TensorrtExecutionProvider",  # NVIDIA TensorRT
        "CUDAExecutionProvider",  # NVIDIA CUDA
        "ROCMExecutionProvider",  # AMD ROCm (Linux)
        "DmlExecutionProvider",  # Windows DirectML
        "OpenVINOExecutionProvider",  # Intel CPU/iGPU
        "CoreMLExecutionProvider",  # macOS
        "CPUExecutionProvider",  # always last
    ]

    available = ort.get_available_providers()
    providers = [ep for ep in PREFERRED if ep in available]
    return providers


def create_onnx_session(model_path, *, sess_options=None):
    """Create a session with consistent FP32 CUDA math across batch shapes."""
    use_tf32 = os.environ.get("SHEKAR_USE_TF32", "0")
    if use_tf32 not in {"0", "1"}:
        raise ValueError("SHEKAR_USE_TF32 must be 0 or 1.")
    providers = get_onnx_providers()
    if "CUDAExecutionProvider" in providers:
        # GPU wheels can use pip-installed cuDNN without a global library-path change.
        from importlib.metadata import PackageNotFoundError, version

        for package in ("nvidia-cudnn-cu13", "nvidia-cudnn-cu12"):
            try:
                version(package)
            except PackageNotFoundError:
                continue
            ort.preload_dlls(cuda=False, cudnn=True)
            break
    options = [
        {"use_tf32": use_tf32} if p == "CUDAExecutionProvider" else {}
        for p in providers
    ]
    return ort.InferenceSession(
        str(model_path),
        sess_options=sess_options,
        providers=providers,
        provider_options=options,
    )
