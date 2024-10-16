from setuptools import setup, find_packages
import os

base_dir = os.path.dirname(__file__)

setup(
    name="eagle-downloader",
    version="1.0.2.1",
    packages=find_packages(),
    setup_requires="setuptools",
    install_requires=[
        "yt-dlp==2023.9.24",
        "questionary==1.10.0",
        "tqdm==4.66.1",
        "colorama==0.4.6",
    ],
    entry_points={
        "console_scripts": [
            "eagle=eagle_downloader.main:main",
        ],
    },
    author="Gustavo Franco",
    author_email="contact@gfrancodev.com",
    description="A CLI tool to download media from YouTube.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/gfrancodev/eagle-downloader",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
