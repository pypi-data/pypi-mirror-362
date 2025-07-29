"""
Setup file for the package
"""

from setuptools import find_packages, setup

with open("pypiReadme.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="tako_alerts_system",
    version="0.2.7",
    author="Gabriel González",
    author_email="gabriel.gonzalez@meliusid.com",
    description="Read PyPI package information",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/melius/itsTako_alerts_library",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
