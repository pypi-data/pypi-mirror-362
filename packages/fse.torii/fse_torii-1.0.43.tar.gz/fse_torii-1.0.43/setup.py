#!/usr/bin/env python

from distutils.core import setup


setup(name='fse.torii',
      version='1.0.43',
      description='Torii',
      author='Fujitsu Systems Europe',
      packages=['torii', 'torii.services', 'torii.data', 'torii.dao', 'torii.decorators', 'torii.managers'],
      install_requires=[
            'requests-toolbelt==1.0.0',
            'numpy==1.24.2',
            'pymongo==4.3.3'
        ]
      )
