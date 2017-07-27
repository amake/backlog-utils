Backlog Utils
=============

A tool for doing things with `Backlog <http://www.backlog.jp/>`__.

Usage
=====
See help::

    backlog -h

Requirements
============
Jython 2.7

Quick Install
=============

Put your Backlog credentials in ``~/.backlog.properties``::

    apiKey=[your API key]
    spaceId=[your space ID]

For simplicity, you are recommended to first create a Jython virtualenv like::

    virtualenv -p $(which jython) env
    . env/bin/activate

This package is not on PyPI, so install with::

    pip install --process-dependency-links git+https://github.com/amake/backlog-utils

License
=======

backlog-utils is distributed under the `MIT license <LICENSE.txt>`__.
