#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="LabelGenerator",
    version="0.1.0",
    author="Jimmy Ho",
    author_email="jimmy@example.com",
    description="一个用于生成PDF格式标签的工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jimmypury/labelgenerator",
    project_urls={
        "Bug Tracker": "https://github.com/jimmypury/labelgenerator/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[
        "reportlab>=3.5.0",
        "qrcode>=6.1",
        "pillow>=8.0.0"
    ],
)