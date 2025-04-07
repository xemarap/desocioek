from setuptools import setup, find_packages

setup(
    name="desocioek",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "numpy",
        "pxstatspy",
    ],
    python_requires=">=3.7",
    author="Emanuel Raptis",
    description="A package for analyzing socioeconomic data at DeSO level",
    long_description=open("README.md").read() if "README.md" else "",
    long_description_content_type="text/markdown",
    url="https://github.com/xemarap/desocioek",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License"
        "Intended Audience :: Developers, Analysts",
        "Programming Language :: Python :: 3"
    ]
)