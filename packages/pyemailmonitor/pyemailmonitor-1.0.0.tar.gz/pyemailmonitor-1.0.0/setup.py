from setuptools import setup, find_packages

setup(
    name="pyemailmonitor",
    version="1.0.0",
    author="Zhao Yutao",
    author_email="zhaoyutao22@mails.ucas.ac.cn",
    description="Python email monitoring library for program status notifications",
    # long_description=open('README.md').read(),
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