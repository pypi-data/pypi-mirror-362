from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent.resolve()
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="booknotes",
    version="0.2.5",
    description="A terminal-based book note-taking app with tags and search",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Eren Öğrül",
    author_email="termapp@pm.me",
    license="GPL-3.0-or-later",
    packages=find_packages(include=["book_notes*"]),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'booknotes = book_notes.cli:run',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Environment :: Console :: Curses",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Utilities",
    ],
    python_requires='>=3.6',
)
