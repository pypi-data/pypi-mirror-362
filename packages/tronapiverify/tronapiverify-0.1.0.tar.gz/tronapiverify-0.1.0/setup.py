from setuptools import setup, find_packages

setup(
    name="tronapiverify",  # unique on PyPI
    version="0.1.0",
    author="Coder",
    author_email="yinomi4405@lhory.com",
    description="API to verify private key",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
