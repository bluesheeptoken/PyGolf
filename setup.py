from os import path

from setuptools import setup

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="pygolf",
    version="0.0.0",
    description="An automatic python code reducer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bluesheeptoken/PyGolf",
    author="Bluesheeptoken",
    # For a list of valid classifiers, see https://pypi.org/classifiers/
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    keywords="golfcode reduce golf",
    python_requires=">=3.5, <4",
    install_requires=["astroid"],
    entry_points={"console_scripts": ["pygolf = pygolf.__main__:main",],},
)