"""
MimicX AI
Human-like AI for everyone.
"""

__version__ = "0.1.6"
__author__ = 'MimicX'
__credits__ = 'AI Researcher at MimicX'

import os
import urllib.request

all_classes = []
domains = ['mimicvision','mimictext','mimicvoice','mimicfeel','mimictwin','mimicphy','mimicsense','mimicmind']
modelFolderUrl = 'https://speedpresta.s3.us-east-1.amazonaws.com/mimicx'
modelNameBase = 'mimicx_'

# Retrieve Domains Libs
for module in domains:
    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir, module + '.so')

    if not os.path.exists(file_path):
        try:
            url = modelFolderUrl + '/' + module + '/' +  module + '.so'
            urllib.request.urlretrieve(url, file_path)
        except:
            print('Unsupported Domain!')

    if os.path.exists(file_path):

        if module == 'mimicvision':
            from .mimicvision import MimicVision
            all_classes.append(MimicVision)

        if module == 'mimictext':
            from .mimictext import MimicText
            all_classes.append(MimicText)


        if module == 'mimicvoice':
            from .mimicvoice import MimicVoice
            all_classes.append(MimicVoice)

        if module == 'mimicfeel':
            from .mimicfeel import MimicFeel
            all_classes.append(MimicFeel)


        if module == 'mimictwin':
            from .mimictwin import MimicTwin
            all_classes.append(MimicTwin)

        if module == 'mimicphy':
            from .mimicphy import MimicPhy
            all_classes.append(MimicPhy)


        if module == 'mimicsense':
            from .mimicsense import MimicSense
            all_classes.append(MimicSense)

        if module == 'mimicmind':
            from .mimicmind import MimicMind
            all_classes.append(MimicMind)


__all__ = all_classes