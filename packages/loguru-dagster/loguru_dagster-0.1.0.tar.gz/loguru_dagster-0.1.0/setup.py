from setuptools import setup, find_packages

setup(
    name="loguru-dagster",
    version="0.1.0",
    description="A lightweight bridge to integrate Loguru logging with Dagster assets.",
    author="Ahmet Sahiner",
    author_email="ahmethasimsahiner@gmail.com",
    url="https://github.com/albersfast/loguru-dagster",
    packages=find_packages(),
    install_requires=[
        "dagster>=1.0.0",
        "loguru>=0.7.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License"
    ],
    python_requires=">=3.7",
)
