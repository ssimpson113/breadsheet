"""
Setup file for Breadsheet
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="breadsheet",
    version="1.0.0",
    author="Your Name",
    description="A baking calculator with baker's percentages and unit conversions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "streamlit>=1.28.0",
    ],
    entry_points={
        "console_scripts": [
            "breadsheet=app:main",
        ],
    },
)
