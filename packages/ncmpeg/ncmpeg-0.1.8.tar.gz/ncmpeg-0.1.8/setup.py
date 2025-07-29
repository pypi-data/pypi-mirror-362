from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="ncmpeg",
    version="0.1.8",
    description="A terminal UI for FFmpeg built with Python and ncurses.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Eren Öğrül",
    author_email="termapp@pm.me",
    license="MIT",
    python_requires=">=3.8",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "ncmpeg = ncmpeg.cli:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        "Topic :: Multimedia :: Video :: Conversion",
        "Topic :: Utilities",
    ],
    include_package_data=True,
)
