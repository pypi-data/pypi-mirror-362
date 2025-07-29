from setuptools import setup, find_packages

setup(
    name="fletch_lib",
    version="0.1.1",
    packages=find_packages(),
    author="Fletcher Smith",
    author_email="fletcherbsmith@gmail.com",
    description="A simple utility package for personal use.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/fbsmith/fletch",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11"
)

