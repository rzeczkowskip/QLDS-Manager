Configuration syntax
====================

Configuration is held in simple .ini file

The file is parsed before passing it to command like, so you can use or define parameters

Parameters
----------

You can set parameters used later in configuration. For example, if you want to use same passwords in every server,
you can put something like that

.. code-block:: text

    [parameters]
    rcon_password = secret-rcon-pass
    stats_password = stats-password
    private_password = elite-only

Now to use those parameters in configuration, call them with ``${parameters.*}`` where * is parameter name

.. note::

    To get parameter, use

    .. code-block:: text

        ${parameters.*}

Global parameters
-----------------

There are 2 pre-defined global parameters, which cannot be overwritten. Those parameters are:

* ``${loop}``
* ``${global.loop}``

``${loop}`` is gives current iteration in server group, so its value increases by 1 after each server parsed in servers
group

``${global.loop}`` is global iteration pointer, so its value increases by 1 after each server parsed, regardless of
group it's in

Self parameters
---------------

With the parameters above, you can set some contants. But what if you want to get current server configuration value?

Instead of using ``${parameter.*}`` use ``${server.*}``.

.. note::

    To get server variable, use

    .. code-block:: text

        ${server.net_port.*}

Math
----

You can use mathematical expressions in You configuration!

Each expression has to be between ``>>`` and ``<<``

.. note::

    Example math expression, where we set zmq_rcon_port 1000 higher than server's port

    .. code-block:: text

        zmq_rcon_port = >>${server.net_port} + 1000<<


Sections
--------

In addition to ``[parameters]`` section, all other sections have to start with pre-defined words. Those words are:

+--------------+------------------------------------------------+
| Word         | Purpose                                        |
+==============+================================================+
| ``server``   | Single server configuration                    |
+--------------+------------------------------------------------+
| ``defaults`` | Server's group defaults/fallback configuration |
+--------------+------------------------------------------------+
| ``extra``    | Extras added to server's group                 |
+--------------+------------------------------------------------+
