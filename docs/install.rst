Installation
============

Requirements
------------

* `Cement <http://builtoncement.com/>`_
* Python 3+

Optional requirements
---------------------

* `ØMQ <http://zeromq.org/bindings:python>`_ - if you want to use RCON
* `Supervisor <http://supervisord.org/>`_ - if you want to start/stop servers

Preferred way
-------------

Use pip

.. code-block:: text

    pip3 install qlds-manager

It will install ``qldsmanager`` script, that will allow you to use Manager as command

Use setuptools manually
-----------------------

For that method to work, you'll need setuptools installed for your version of Python

Go to the QLDS-Manager dir and run

.. code-block:: text

    python3 setup.py install

Just like in pip installation, it will create script to use Manage as command

Manual
------

You can install all dependencies manually and use QLDS Manager with

.. code-block:: text

    python3 /path/to/qlds-manager/qldsmanager
