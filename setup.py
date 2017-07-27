from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='backlog-utils',
    version='1.0',
    description='Utilities for Backlog',
    long_description=long_description,
    url='https://github.com/amake/backlog-utils',
    author='Aaron Madlon-Kay',
    author_email='aaron@madlon-kay.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Bug Tracking',
        'Topic :: Software Development :: Documentation',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='backlog',
    py_modules=['backlog_utils'],
    install_requires=['https://github.com/amake/jyven/tarball/master#egg=package-1.0'],
    entry_points={
        'console_scripts': [
            'backlog=backlog_utils:main',
        ],
    },
)
