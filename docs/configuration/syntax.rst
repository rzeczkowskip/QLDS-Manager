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
