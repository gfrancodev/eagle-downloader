from setuptools import setup, find_packages

setup(
    name="eagle-downloader",
    version="1.0.1",
    packages=find_packages(),
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
    url="https://github.com/gfrancodev/eagle-downloader",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11.10",
)
