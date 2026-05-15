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
