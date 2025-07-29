from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")
setup(
    name="timelap",
    version="0.0.1",
    description="A simple time measuring library",
    author="aftxrlifx",
    packages=find_packages(),
    python_requires=">=3.7",
    long_description=long_description,
    long_description_content_type="text/markdown"
)