from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="brucelog",
    version="1.1.3",
    description="A very sleek, modern, and monochrome logger modification",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="zappy",
    author_email="zappy@zappy.com",
    url="https://github.com/bornpaster/bruce",
    py_modules=["brucelog"],
    python_requires=">=3.6",
    install_requires=[],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    license="MIT",
    keywords="logger logging terminal minimal monochrome",
    project_urls={ 
        "Source": "https://github.com/bornpaster/bruce",
        "Tracker": "https://github.com/bornpaster/bruce/issues",
    },
)
