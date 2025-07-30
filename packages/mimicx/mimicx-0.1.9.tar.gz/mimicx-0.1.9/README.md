# MIMICX AI Library 📚

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![PyPI version](https://img.shields.io/pypi/v/genai-processors.svg)](https://pypi.org/project/mimicx/)

**Build Modular, Asynchronous, and Composable AI Pipelines for Generative AI.**

Mimicx AI is a lightweight Python library for giving machines human-level perception and decision-making capabilities by enabling advanced perception, contextual reasoning, autonomous decision-making, and intuitive human-machine interaction.

At its core, Mimicx structures its capabilities into specialized domains — `Vision`, `Text`, `Voice`, `Feel`, `Twin`, `Phy`, `Sense`, and `Mind` — each targeting a unique dimension of machine perception, reasoning, and interaction.

## Face Recognition Sample 

```python
import os
from mimicx import MimicVision

# Get the current directory of this script (or notebook)
folder_path = os.path.dirname(__file__)

if __name__ == "__main__":
    # Initialize the MimicVision client
    client = MimicVision()

    # Load the face recognition model
    client.load('face_recognition')

    # Define image paths
    img_path_1 = os.path.join(folder_path, "image1.png")
    img_path_2 = os.path.join(folder_path, "image2.png")

    # Extract face features from both images
    features1 = client.extract_face_feature(img_path_1)
    features2 = client.extract_face_feature(img_path_2)

    # Compare the two sets of face features
    result = client.compare_features_faces(features1, features2)

    # Print the similarity score or the error message
    if isinstance(result, (float, int)):
        print(f"Face similarity: {result:.2f}")
    else:
        print(result)
```



## Iris Recognition Sample 

```python
import os
from mimicx import MimicVision

# Get the current directory of this script
folder_path = os.path.dirname(__file__)

if __name__ == "__main__":
    # Initialize the MimicVision client
    client = MimicVision()

    # Load the iris recognition model
    client.load('iris_recognition')

    # Define image paths
    img_path_1 = os.path.join(folder_path, "image1.png")
    img_path_2 = os.path.join(folder_path, "image2.png")

    # Extract iris features
    features1 = client.extract_iris_feature(img_path_1)
    features2 = client.extract_iris_feature(img_path_2)

    # Compare iris features
    result = client.compare_features_iris(features1, features2)

    if isinstance(result, (float, int)):
        print(f"Iris similarity: {result:.2f}")
    else:
        print(result)

```


## Notes
* Ensure that the images exist in the same directory as this script.

* The MimicX package must be installed and properly configured.

* The load('face_recognition') call initializes the face recognition model.



## ✨ Key Features

*   **MimicVision**:  processes and interprets visual data, enabling advanced image and video understanding.

*   **MimicText**: handles natural language processing and contextual text reasoning.

*   **MimicVoice**: works with audio signals for speech recognition, synthesis, and voice interaction.

*   **MimicFeel**: captures and interprets tactile and sensory data to simulate touch and emotion.

*   **MimicTwin**: creates and manages digital twins, bridging physical and virtual environments.

*   **MimicPhy**: interfaces with physical systems for autonomous control and robotics.

*   **MimicSense**: integrates multisensory data streams for comprehensive environmental awareness.

*   **MimicMind**: enables high-level cognitive functions including planning, decision-making, and adaptive learning.


## 📦 Installation

The GenAI Processors library requires Python 3.10+.

Install it with:

```bash
pip install mimicx
```


## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for
guidelines on how to contribute to this project.

## 📜 License

This project is licensed under the MIT License, See the
[LICENSE](LICENSE) file for details.

## Mimicx Terms of Services

If you make use of Mimicx via the MimicX library, please ensure you
review the [Terms of Service](https://mimicx.ai).
