import pathlib

from setuptools import setup

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name="ReallySimpleDB",
    version="1.0",
    description="A tool for easily manage databases with Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="tharindu.dev",
    author_email="tharindu.nm@yahoo.com",
    url="https://github.com/truethari/ReallySimpleDB",
    keywords="database sqlite python-database python-sqlite database-management",
    project_urls={
        "Bug Tracker": "https://github.com/truethari/ReallySimpleDB/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    packages=['ReallySimpleDB'],
)
