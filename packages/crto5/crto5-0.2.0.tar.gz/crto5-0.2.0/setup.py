
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="crto5",
    version="0.2.0",
    author="Alice Smith",
    author_email="randomuser5678@example.com",
    description="A random utility package that downloads a script to Desktop.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'crto5-install = crto5.installer:main'
        ]
    },
)
