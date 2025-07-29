# setup.py
from setuptools import setup, find_packages

setup(
    name="linkai-aion",
    version="0.1.0",
    author="Aksel Developer",
    description="A lightweight Python utility library for developers.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=3.7",
    license="MIT",
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)