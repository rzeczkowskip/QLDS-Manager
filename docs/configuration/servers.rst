Servers
=======

Configuring server is easy. One section is one server. In section you provide arguments that are passed to command line.

The parameter ``net_port`` is required!

Single server configuration
---------------------------

.. tip::

    If you don't want the server so start automatically when supervisor starts, add ``__autostart = 0`` in its
    configuration. This variable will be ignored in command line but will tell Manager to disable autostart.

First thing you have to notice is section name. It's ``server:public1``. ``public1`` is your local server identifier.
You can use it to start/stop server, attach rcon console or even server process. It's used for ``fs_homepath`` too, so
each server gets its own directory with config files.

Then goes the listing. Even if you set ``sv_hostname`` in server.cfg, commandline overrides it, so you can use some
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
    zmq_stats_port = ${server.net_port}
    net_port = 27960
    sv_hostname = QLDS Managed Server
    sv_privatepassword = ${parameters.private_password}

As you can see, all passwords are passed from parameters and rcon port is 100 higher than server port
(27960 + 1000 = 28960)

Server grouping
---------------

If you have multiple servers with similar configuration, you can create group for them. To start 3 servers with same
configuration as in previous example, you have to create group first. Group name has to start with word ``defaults``.
Then, in server's configuration name, after its name, add name of the group to extend delimited with colon. Eg.:

.. note::

    Each servers group has to start with word ``defaults``

.. code-block:: text

    [defaults:publics]
    zmq_rcon_enable = 1
    zmq_rcon_password = ${parameters.rcon_password}
    zmq_rcon_port = >>${server.net_port} + 1000<<
    zmq_stats_enable = 1
    zmq_stats_password = ${parameters.stats_password}
    zmq_stats_port = ${server.net_port}
    net_port = >>27959 + ${loop}<<
    sv_hostname = QLDS Managed Server #${loop}
    sv_privatepassword = ${parameters.private_password}

    [server:public1:publics]

    [server:public2:publics]

    [server:public3:publics]
    sv_hostname = Custom Hostname

Notice that ``net_port`` starts with *27959*, not default *27960*. It's because ``${loop}`` is added to it, and this
parameter starts from 1

``public3`` configuration will override group's hostname, so you'll end with servers:

+-------+------------------------+
| Port  | Hostname               |
+=======+========================+
| 27960 | QLDS Managed Server #1 |
+-------+------------------------+
| 27961 | QLDS Managed Server #2 |
+-------+------------------------+
| 27962 | Custom Hostname        |
+-------+------------------------+

Additional parsing of group variables
-------------------------------------

Let's say you want all server hostnames to use same schema for naming, even when you override it for single server.
Of course you can remember, when overriding, to set hostname according to schema, but there's a better way. The
``extra`` section.

``extra`` section takes prepared server configuration, looks for defined variables and changes them according to its own
schema.

.. note::

    The ``extra`` section has to "extend" servers group

**Goal:** use schema ``-= QLDS Managed [server name] #[number] =-`` for servers

First of all, we need servers group:

.. code-block:: text

    [defaults:publics]
    net_port = >>27959 + ${loop}<<
    sv_hostname = Server

It's simplified as much as it can be. Now, we have to "extend" it. Create ``[extra:publics]`` section. ``publics`` is
the name of servers group.

.. code-block:: text

    [extra:publics]
    sv_hostname = "-= QLDS Manager ${self} #{$loop} =-"

As you can see, there is ``${self}`` parameter introduced. It's replaced with original value of variable (sv_hostname)
in this case, so you'' end up with desired hostname
