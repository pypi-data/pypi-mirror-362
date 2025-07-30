from setuptools import setup, find_packages

setup(
    name="gabiteodoru-sugar",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pandas",
        #"oyaml",
        "more_itertools",
    ],
    author="Gabi Teodoru",
    author_email="gabiteodoru@gmail.com",
    description="Gabi's syntactic sugar & other utils",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/gabiteodoru/sugar",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)