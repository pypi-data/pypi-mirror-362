"""
MimicX AI
Human-like AI for everyone.
"""

__version__ = "0.1.5"
__author__ = 'MimicX'
__credits__ = 'AI Researcher at MimicX'

import os
import urllib.request

domains = ['mimicvision']
modelFolderUrl = 'https://speedpresta.s3.us-east-1.amazonaws.com/mimicx'
modelNameBase = 'mimicx_'

# Retrieve Domains Libs
for module in domains:
    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir, module + '.so')

    if not os.path.exists(file_path):
        url = modelFolderUrl + '/' + module + '/' +  module + '.so'
        urllib.request.urlretrieve(url, file_path)

# Retrieve Domains Classes
from .mimicvision import MimicVision

__all__ = ['MimicVision']