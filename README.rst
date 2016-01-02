=============================
clcc: OpenCL offline compiler
=============================

.. image:: https://img.shields.io/github/license/Maratyszcza/clcc.svg
  :alt: clcc license: Simplified BSD
  :target: https://github.com/Maratyszcza/clcc/blob/master/LICENSE.rst

clcc is an offline compiler for OpenCL kernels

Installation
------------

.. code-block:: bash

  git clone https://github.com/Maratyszcza/clcc.git
  cd clcc
  pip install --upgrade .

Similar projects
----------------

Active projects:

- Apple ships an offline OpenCL compiler `openclc` for OS X with XCode. It compiles to portable bitcode for CPUs or GPUs, which is recognized by Apple drivers. Mac Developer library `documents how to use it <https://developer.apple.com/library/mac/samplecode/OpenCLOfflineCompilation/Introduction/Intro.html>`_.

- AMD maintains `CLOC - OpenCL Offline Compiler <https://github.com/HSAFoundation/CLOC>`_ for compiling OpenCL kernels to HSAIL and BRIG formats.

- Intel OpenCL SDK contains a `KernelBuilder`. However, it can not build kernels for devices which are not installed on the host system.

- `Mali offline compiler <http://malideveloper.arm.com/resources/tools/mali-offline-compiler/>`_ can compile OpenCL shaders for ARM's OpenCL-enabled Mali devices and reports some statistics useful for performance optimization. However, it doesn't let you save the machine code for a kernel.

Unmaintained projects:

- `Command line interface to the NVIDIA OpenCL compiler from Leith Bade <https://github.com/ljbade/clcc>`_ wraps undocumented interfaces of nVidia OpenCL driver. No updates since 2013.

- `CLCC - The OpenCL kernel Compiler from  George van Venrooij <http://clcc.sourceforge.net/>`_. No updates since 2012.

- `OpenCLcc from Isaac Gelado <https://code.google.com/p/openclcc/>`_. No updates since 2011.

- `CLC: OpenCL compiler and syntax checker from Matias Holm <https://github.com/lorrden/clc>`_. No updates since 2010.

- `OpenCL-Compiler from Chris Lundquist <https://github.com/ChrisLundquist/OpenCL-Compiler.git>`_.  No updates since 2010.
