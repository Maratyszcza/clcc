#!/usr/bin/env python

from clcc import __version__
from distutils.core import setup
import os


def read_text_file(path):
    with open(os.path.join(os.path.dirname(__file__), path)) as f:
        return f.read()


def main():
    setup(name="clcc",
        version=__version__,
        description="OpenCL offline compiler",
        long_description=read_text_file("README.rst"),
        author="Marat Dukhan",
        author_email="maratek@gmail.com",
        url="https://www.github.com/Maratyszcza/clcc",
        classifiers=[
            "Environment :: Console",
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Developers",
            "Intended Audience :: Science/Research",
            "License :: OSI Approved :: BSD License",
            "Operating System :: Microsoft :: Windows",
            "Operating System :: POSIX :: Linux",
            "Operating System :: MacOS :: MacOS X",
            "Natural Language :: English",
            "Programming Language :: Python",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Programming Language :: Other",
            "Topic :: Software Development",
            "Topic :: Software Development :: Compilers",
            "Topic :: Utilities"
        ],
        packages=["clcc"],
        zip_safe=False,
        scripts=os.path.join("bin", "clcc"))


if __name__ == '__main__':
    main()
