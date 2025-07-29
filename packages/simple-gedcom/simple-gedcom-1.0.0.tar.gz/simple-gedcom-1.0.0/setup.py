from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    
    
setup(
    name='simple-gedcom',
    version='1.0.0',
    description='A Python module for parsing and analyzing GEDCOM files.',
    author='mcobtechnology',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mcobtechnology/simple-gedcom",    
    license='GPLv2',
    keywords='python gedcom parser',
    packages=find_packages(),
    python_requires=">=3.6",
)
