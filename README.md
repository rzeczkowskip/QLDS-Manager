QLDS Manager
============

**QLDS Manager** is a tool dedicated for Quake Live Server administrators

Core functionality allows to:

* Download SteamCMD and QL server files to specified location
* Update QL server files
* Easily configure multiple servers

Additional functionality:

* Generating supervisord configuration (requires supervisord)
* Keep servers alive
* Start/stop/restart server
* Connect to rcon console (requires zmq)

Installation
============

Default requirements
--------------------

* [Cement][1]
* Python 3+

There are 2 ways to install QLDS Manager.

Preferred way
-------------

Use pip

`pip3 install qlds-manager`

It will install `qldsmanager` script, that will allow you to use Manager as command

Use setuptools manually
-----------------------

For that method to work, you'll need setuptoold installed for your version of Python

Go to the QLDS-Manager dir and run

`python3 setup.py install`

Just like in pip installation, it will create script to use Manage as command

Manual
------

You can install all dependencies manually and use QLDS Manager with

`python3 /path/to/qlds-manager/qldsmanager`

[1]: http://builtoncement.com/