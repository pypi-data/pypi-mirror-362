from setuptools import setup, find_packages
import os

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="forgeffects",
    version="0.2.5",
    description="A package for forgotten effects theory computation.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Claudio Esteban Araya Toro",
    author_email="claudioesteban.at@gmail.com",
    url="https://github.com/claudio-araya/forgeffects",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "forgeffects": ["dataset/*.npy"],  
    },
    install_requires=[
        "tensorflow==2.13",
        "tensorflow_probability==0.20.0",
        "numpy>=1.18",
        "pandas>=1.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9, <=3.11',
)

