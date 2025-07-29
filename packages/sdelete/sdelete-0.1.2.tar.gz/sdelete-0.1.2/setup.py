from setuptools import setup, find_packages
from pathlib import Path

# Read the README.md for long description
this_dir = Path(__file__).parent
long_description = (this_dir / "README.md").read_text(encoding="utf-8")

setup(
    name="sdelete",
    version="0.1.2",
    author="Eren Öğrül",
    author_email="termapp@pm.me",
    description="A terminal UI app for secure file deletion using Python and ncurses.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bearenbey/sdelete",  # Change this to your GitHub repo
    packages=find_packages(),
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        "Environment :: Console",
        "Topic :: System :: Archiving :: Backup",
        "Topic :: Utilities"
    ],
    entry_points={
        "console_scripts": [
            "sdelete = sdelete.cli:main"
        ]
    },
    include_package_data=True,
    zip_safe=False,
)