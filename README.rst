===============================================
Beak API - REST/json API for use by Hamakor NPO
===============================================

This package contains WSGI apps for serving some API's on Hamakor server.

- Conference speakers and agenda, for use by: websites, mobile apps,
  Kodi plugins.
  
  * PyCon-IL old API (used by the mobile apps of PyCon-IL 2016).
  * PyCon-IL API, for 2016, 2017, and future :-)
 
- Other

Installation
------------

Quick-Start
===========

.. code-block:: bash

  ~$ sudo apt-get install git python-virtualenv

This assumes a stable debian-based distro. Depending on your distro, you may
have to use some other commands. Just make sure you have git_ and virtualenv_
installed).

Also, code bellow assumes that your distro's default python version is 2.7.
If it is python3-based, you may need to install `python3.x-venv` instead of
`python-virtualenv`, and use `python -m venv` instead of `virtualenv` below.

.. code-block:: bash

  ~$ git clone --recursive https://github.com/AmitAronovitch/beak_api.git
  ~$ cd beak_api

Note: --recursive is required for auto-filling your new database with actual data

.. code-block:: bash

  ~/beak_api$ virtualenv -p python3 env
  ~/beak_api$ env/bin/python setup.py develop
  ~/beak_api$ env/bin/python -m beak.api.run

This will start a local API server on port 8080 (test it by pointing browsing
locally to http://127.0.0.1:8080/api/list , then close using Ctrl-C on the
terminal).

Now, save the following file as `~/.config/beakapi/options.py`

.. code-block:: python

  #log_level = DEBUG
  #debug_sql = False
  #pycon2016_db = '/home/amit/.local/share/beakapi/pyconil2016.sqlite'
  
  # following are used for the standalone runner (beak.api.run)
  host = '0.0.0.0' #127.0.0.1 for local host only, 0.0.0.0 for all interfaces
  port = 8080

This config tells the server to listen on all devices (you should choose a
port number which is open on the firewall). Other parameters in the config
control the debug level and the location of the DB (the database had been built
and auto-filled on your first run).

Now, you can run the configured stand-alone server in the background:

.. code-block:: bash

  ~/beak_api$ env/bin/python -m beak.api.run 2>&1 | cat >beak.api.log &
  
.. _git: https://git-scm.com/download/linux
.. _virtualenv: https://virtualenv.pypa.io/en/stable/installation/

Installing behind a WSGI-compatible web-server
==============================================

The `beak.api` package contains the `app` object, which is a standard WSGI
application. Refer to the web-server's doc to see how to configure it for
running a WSGI app.

Following example assumes apache2 with mod-wsgi, and uses a virtualenv (as
opposed to installing the dependencies on your system python).
You should create the virtualenv using the same Python version that your
`mod-wsgi` package usage (beak-api only supports versions 2.7.9 and upper.
However, distros using an older 2.7.x version of Python might have an
alternative, python3-based mod-wsgi, which should work).

The beak_api repo contains a file `beak_api.wsgi` which should be usable
for `mod-wsgi`.

TODO: complete the example...

Usage
-----
TODO

Adding New API
--------------
TODO

Copyright & License
-------------------

Copyright (c) 2017, `Hamakor <https://www.hamakor.org.il/>`_. MIT License.
