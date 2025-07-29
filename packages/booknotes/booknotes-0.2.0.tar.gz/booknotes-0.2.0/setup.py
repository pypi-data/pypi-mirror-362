from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="booknotes",
    version="0.2.0",
    description="Terminal-based note app for book lovers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Eren Öğrül",
    author_email="termapp@pm.me",
    url="https://github.com/your-username/book-note-repository",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'booknote = book_note_repository.cli:run',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Environment :: Console :: Curses",
    ],
    python_requires='>=3.6',
)