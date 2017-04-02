#!/usr/bin/env python

from os.path import join, dirname, abspath

try:
    from setuptools import setup
except ImportError as error:
    from distutils.core import setup

CURDIR = dirname(abspath(__file__))

version_file = join(dirname(abspath(__file__)), 'src', 'ModbusLibrary', 'version.py')

# get VERSION from version file
with open(version_file) as file:
    code = compile(file.read(), version_file, 'exec')
    exec(code)

CLASSIFIERS = """
Development Status :: 4 - Beta
License :: MIT
Operating System :: OS Independent
Intended Audience :: Developers
Intended Audience :: Testers
Programming Language :: Python
Topic :: Software Development :: Testing
Topic :: System Development :: Testing
"""[1:-1]

setup(name         = 'robotframework-modbus',
      version      = VERSION,
      description  = 'Modbus TCP/IP testing library for Robot Framework',
      author       = 'Florian Kromer',
      author_email = 'thinwybk@mailbox.org',
      url          = 'http://github.com/fkromer/robotframework-modbus/',
      license      = 'MIT',
      keywords     = 'robotframework testing test automation modbus tcp',
      platforms    = 'any',
      classifiers  = CLASSIFIERS.splitlines(),
      package_dir  = {'' : 'src'},
      packages     = ['ModbusLibrary'],
      long_description = open(join(CURDIR, 'README.md')).read(),
      install_requires=[
            'robotframework',
            'robotframework-rammbock'
      ],
)
