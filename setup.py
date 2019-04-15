#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from distutils.core import setup

setup(name='ybook',
      version='0.1.1',
      author='Kazuhiro HISHINUMA',
      author_email='kaz@cs.meiji.ac.jp',
      url='https://github.com/kazh98/ybook',
      description='Miscellaneous functions used for Meiji Univ. Seminar I',
      long_description='This is a python package providing miscellaneous functions used for Seminar I, '
                       'a Meiji University compulsory subject.',
      download_url='https://github.com/kazh98/ybook/releases',
      classifiers=['Topic :: Education',
                   'Topic :: Scientific/Engineering',
                   'Intended Audience :: Education',
                   'Intended Audience :: Science/Research',
                   'License :: OSI Approved :: MIT License'],
      install_requires=['numpy>=1.14.2',
                        'sympy>=1.1.1',
                        'matplotlib>=2.2.2'],
      packages=['ybook'],
      )
