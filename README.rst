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

(or, depending on your distro, use some other way to make sure you have
git_ and virtualenv_ installed).

.. code-block:: bash

  ~$ git clone --recursive https://github.com/AmitAronovitch/beak_api.git
  ~$ cd beak_api

Note: --recursive is required for auto-filling your new database with actual data

.. code-block:: bash

  ~/beak_api$ virtualenv -p python3 env
  ~/beak_api$ env/bin/python setup.py develop
  ~/beak_api$ env/bin/python -m beak.api.run

This will start a local API server on port 8080 (test it with local browser,
then close using Ctrl-C).

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

TODO: document in details

The `beak.api` package contains the `app` object, which is a standard WSGI
application. Refer to the web-server's doc to see how to configure it for
running a WSGI app.

Usage
-----
TODO

Adding New API
--------------
TODO

Copyright & License
-------------------

Copyright (c) 2017, `Hamakor <https://www.hamakor.org.il/>`_. MIT License.


