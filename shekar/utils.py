import re
import onnxruntime as ort


def is_informal(text, threshold=1) -> bool:
    """
    Classifies Persian text into formal or informal based on predefined regex patterns and counts the number of informal matches.
    This function is an implementation of:
    https://fa.wikipedia.org/wiki/%D9%88%DB%8C%DA%A9%DB%8C%E2%80%8C%D9%BE%D8%AF%DB%8C%D8%A7:%D8%A7%D8%B4%D8%AA%D8%A8%D8%A7%D9%87%E2%80%8C%DB%8C%D8%A7%D8%A8/%D9%81%D9%87%D8%B1%D8%B3%D8%AA/%D8%BA%DB%8C%D8%B1%D8%B1%D8%B3%D9%85%DB%8C

    Args:
        text (str): The input Persian text.

    Returns:
        tuple: True or False
    """
    informal_patterns = [
        r"(?:ن?می‌? ?|ب|ن)(?:[یا]فشون|پاشون|پرورون|پرون|پوسون|پوشون|پیچون|تابون|تازون|ترسون|ترکون|تکون|تونست|جنبون|جوشون|چپون|چربون|چرخون|چرون|چسبون|چشون|چکون|چلون|خارون|خراشون|خشکون|خندون|خوابون|خورون|خون|خیسون|درخشون|رسون|رقصون|رنجون|رون|دون|سابون|ستون|سوزون|ش|شورون|غلتون|فهمون|کوبون|گذرون|گردون|گریون|گزین|گسترون|گنجون|لرزون|لغزون|لمبون|مالون|ا?نداز|نشون|هراسون|وزون)(?:م|ی|ه|یم|ید|ن)",
        r"(?:ن?می‌? ?|ب|ن)(?:چا|خا|خوا)(?:م|ی|د|یم|ید|ن)",
        r"(?:ن?می‌? ?|ب)(?:مون|شین|گ)(?:م|ی|ه|یم|ید|ن)",
        r"(?:ن?می‌? ?|ن)(?:دون|د|تون)(?:م|ی|ه|یم|ید|ن)",
        r"(?:نمی‌? ?|ن)(?:یا)(?:م|ه|یم|ید|ن)",
        r"(?:می‌? ?)(?:ر)(?:م|ی|ه|یم|ید|ن)",
        r"(?:ن?می‌? ?|ب|ن)(?:در|پا|کاه|گا|ایست)ن",
        r"(?:ن?می‌? ?|ب|ن)دون(?:م|ی|ه|یم|ید|ن)",
        r"(?:ازش|اونه?ا|ایشون|اینجوری?|این[وه]|بازم|باهاش|براتون|برام|بهش|بی‌خیال|تموم|چ?جوری|چیه|دیگه|کدوم|مونده|زبون|همینه)",
        r"(?:آروم|آشیونه|آشیون|اومدم|برم|اونه|اون‌|ایرونی|اینا|بادمجون|بدونیم|بذار|بریم|بشیم|بشین|بنداز|بچگونه|بیابون|بیگیر|تهرون|تونستم|خمیردندون|خودتون|خودشون|خودمونی|خودمون)",
        r"(?:خوروندن|خونه|خیابون|داره|داروخونه|داغون|دخترونه|دندون|رودخونه|زمونه|زنونه|سوزوندن|قلیون|مردونه|مهمون|موندم|میام|میونه|میون|می‌دونیم|نتونستم|ندونیم)",
        r"(?:نذار|نریم|نسوزوندن|نشونه|نشون|نموندم|نمیاد|نمیام|نمیان|نمیایم|نمیاین|نمیای|نمیدونید|نمی‌دونیم|نمی‌دونین|نیستن|نیومدم|هستن|همزبون|همشون|پسرونه|پشت بوم|کوچیک|تمومه)",
    ]

    match_count = 0

    for pattern in informal_patterns:
        matches = re.findall(pattern, text)
        match_count += len(matches)

    classification = True if match_count >= threshold else False
    return classification


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
