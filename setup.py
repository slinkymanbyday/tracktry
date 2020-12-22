"""Setup configuration."""
import setuptools

with open("README.md", "r") as fh:
    LONG = fh.read()
setuptools.setup(
    name="tracktry",
    version="0.1.1",
    author="slinkymanbyday",
    author_email="slinkymanbyday@gmail.com",
    description="",
    long_description=LONG,
    install_requires=['aiohttp'],
    long_description_content_type="text/markdown",
    url="https://github.com/slinkymanbyday/tracktry",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
