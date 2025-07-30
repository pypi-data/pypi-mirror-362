from setuptools import setup, find_packages

setup(
    name="mimicx",
    version="0.1.8",
    author="MimicX AI",
    author_email="mimicx@speedpresta.com",
    description="Human-like AI for everyone — vision, text, voice, and more in one simple package.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    #install_requires=['mpi4py>=2.0','numpy', ],
    url="https://github.com/Mimicx-AI/pip-package",
    packages=find_packages(),
    license='MIT',
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.9",
)