#!/usr/bin/env python3
import os
from setuptools import find_packages, setup
import shutil


def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), "README.md")
    with open(readme_path, "r", encoding="utf-8") as fh:
        return fh.read()


def read_requirements():
    req_path = os.path.join(os.path.dirname(__file__), "requirements.txt")
    with open(req_path, "r", encoding="utf-8") as fh:
        deps = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

    return deps


def get_package_data():
    data_files = []

    data_files.extend(
        [
            "config.yaml",
            "default_models.yaml",
        ]
    )
    return data_files


setup(
    name="phocr",
    version=open("version.txt").read().strip(),
    author="PuHui Lab",
    author_email="puhuilab@gmail.com",
    description="High-Performance OCR Toolkit",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/puhuilab/phocr",
    packages=find_packages(),
    package_data={
        "phocr": get_package_data(),
    },
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
        "cpu": [
            "onnxruntime>=1.17.0",
        ],
        "cuda": [
            "onnxruntime-gpu>=1.17.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "phocr=phocr.main:main",
        ],
    },
    keywords="ocr, text recognition, computer vision, deep learning",
    project_urls={
        "Bug Reports": "https://github.com/puhuilab/phocr/issues",
        "Source": "https://github.com/puhuilab/phocr",
        "Documentation": "https://github.com/puhuilab/phocr#readme",
    },
)
