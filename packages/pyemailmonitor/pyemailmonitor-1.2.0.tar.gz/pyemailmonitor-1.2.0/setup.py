from setuptools import setup, find_packages
import os
from pathlib import Path

def read_file(filename):
    base_dir = Path(__file__).parent
    file_path = (base_dir / filename).resolve()
    with open(file_path, encoding='utf-8') as f:
        return f.read()

setup(
    name="pyemailmonitor",
    version="1.2.0",
    author="Zhao Yutao",
    author_email="zhaoyutao22@mails.ucas.ac.cn",
    description="Python email monitoring library for program status notifications",
    long_description=read_file('README.md'),
    long_description_content_type="text/markdown",
    url="https://github.com/PoseZhaoyutao/pyemailmonitor",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[],
    entry_points={
        'console_scripts': [
            'email-monitor=pyemailmonitor.cli:main',
        ],
    },
)