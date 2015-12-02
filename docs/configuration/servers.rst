Servers
=======

Configuring server is easy. One section is one server. In section you provide arguments that are passed to command line.

The parameter ``net_port`` is required!

Single server configuration
---------------------------

First thing you have to notice is section name. It's ``server:public1``. ``public1`` is your local server identifier.
You can use it to start/stop server, attach rcon console or even server process. It's used for ``fs_homepath`` too, so
each server gets its own directory with config files.

Then goes the listing. Even if you set ``sv_hostname`` in server.cfg, commandline overwrites it, so you can use some
default server.cfg and use Manager for instance-specific variables.

Look at the example below:

.. note::

    Each server's section has to start with word ``server``

.. code-block:: text

    [server:public1]
    zmq_rcon_enable = 1
    zmq_rcon_password = ${parameters.rcon_password}
    zmq_rcon_port = >>${server.net_port} + 1000<<
    zmq_stats_enable = 1
    zmq_stats_password = ${parameters.stats_password}
    zmq_stats_port = 27960
    net_port = >>27960 + ${loop}<<
    sv_hostname = QLDS Managed Server
    sv_privatepassword = ${parameters.private_password}

As you can see, all passwords are passed from parameters and rcon port is 100 higher than server port
(27960 + 1000 = 28960)
