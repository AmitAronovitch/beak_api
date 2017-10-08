#!/usr/bin/env python
from setuptools import setup, find_packages

meta = dict(
    name='beak_api',
    version='0.2.0',
    description='API for Hamakor conference data'
)

if __name__ == '__main__':
    setup(
        python_requires='>=2.7.9',

        install_requires=[
            'funcsigs;python_version<"3.3"',
            'appdirs',
            'python-dateutil',
            'bottle',
            'pony',
        ],

        setup_requires=['pytest-runner'],
        tests_require=[
            'pytest', 'WebTest'
        ],
        packages=find_packages(),  # ['beak']

        **meta
    )
