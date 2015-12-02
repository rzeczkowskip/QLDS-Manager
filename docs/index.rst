.. QLDS Manager documentation master file, created by
   sphinx-quickstart on Sun Nov 29 20:03:46 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to QLDS Manager's documentation!
========================================

QLDS Manager is a tool dedicated for Quake Live Server administrators

Core functionality allows to:

* Download SteamCMD and QL server files to specified location
* Update QL server files
* Easily configure multiple servers

Additional functionality:

* Generating supervisord configuration (requires supervisord)
* Keep servers alive
* Start/stop/restart server
* Connect to rcon console (requires zmq)

Documenatation
--------------

.. toctree::
   :maxdepth: 20

   install
   configuration/index
