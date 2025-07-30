# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os

# Safely load README
def read_readme():
    try:
        with open("README.md", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return "Autonomous quantum AI research agent."

setup(
    name="QuantumMetaGPT",
    version="1.0.0",
    description="Autonomous quantum AI research agent",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    author="Quantum Research Team",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "qiskit>=0.44",
        "qiskit-ibmq-provider",
        "stable-baselines3",
        "arxiv",
        "openai",
        "transformers",
        "torch",
        "matplotlib",
        "pylatex",
        "cryptography",
        "fastapi",
        "uvicorn",
        "python-dotenv",
        "gym",
        "quantummeta-license"
    ],
    entry_points={
        "console_scripts": [
            "qmetagpt = main:main",
            "qmetagpt-license = qmetagpt.security_licensing.cli_license:cli"
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: Other/Proprietary License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
)
