from setuptools import setup, find_packages
import pathlib

this_dir = pathlib.Path(__file__).parent
readme = (this_dir / "README.md").read_text(encoding="utf-8")

setup(
    name="markyy",
    version="0.2.1",
    author="Eren Öğrül",
    author_email="termapp@pm.me",
    description="A terminal-based markdown editor using curses",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/bearenbey/marky",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
    ],
    entry_points={
        "console_scripts": [
            "marky=marky.cli:main",
        ]
    },
    python_requires=">=3.7",
    include_package_data=True,
)