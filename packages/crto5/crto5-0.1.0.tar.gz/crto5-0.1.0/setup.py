from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="crto5",
    version="0.1.0",
    author="John Doe",
    author_email="randomuser1234@example.com",
    description="A random utility package.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'tq1-install = tq1.installer:main'
        ]
    },
)
