from os import path

from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="pygolf",
    version="1.0.1",
    description="An automatic python code shortener",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bluesheeptoken/PyGolf",
    author="Bluesheeptoken",
    # For a list of valid classifiers, see https://pypi.org/classifiers/
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    license="MIT",
    packages=find_packages(exclude=["test"]),
    keywords="golfcode shorten_code golf",
    python_requires=">=3.6, <4",
    install_requires=["argparse", "astroid", "pyperclip"],
    entry_points={"console_scripts": ["pygolf = pygolf.__main__:main"]},
)
