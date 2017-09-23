#!/usr/bin/env python
from setuptools import setup, find_packages

meta = dict(
    name = 'beak_api',
    version = '0.1.0',
    description = 'API for Hamakor conference data'
)

if __name__ == '__main__':
    setup(
        install_requires = [
            'appdirs',
            'python-dateutil',
            'bottle',
            'pony',
        ],
        tests_require = [
            'WebTest',
        ],
        packages = find_packages(), #['beak']
        
        **meta
    )
