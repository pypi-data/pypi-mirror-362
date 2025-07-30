from setuptools import setup, find_packages

setup(
    name="BLSSLIB",
    version=open(r"E:\vs code\files\BLSSLIB\tests\version.txt").read().strip(),
    author="Back",
    description="A Python library for encoding and decoding Build logic save data.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="GPL-3.0-or-later",
    license_files=["LICENSE"],
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
