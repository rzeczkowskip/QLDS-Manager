Manager configuration
=====================

Default values
---------------

+------------------------+----------------------------+
| Description            | Location                   |
+========================+============================+
| steamcmd               | ~/steamcmd                 |
+------------------------+----------------------------+
| QL files               | ~/QLserver                 |
+------------------------+----------------------------+
+------------------------+----------------------------+
| Servers configuration  | ~/.qldsmanager/servers     |
+------------------------+----------------------------+
| Rcon configuration     | ~/.qldsmanager/rcon        |
+------------------------+----------------------------+
+------------------------+----------------------------+
| Supervisord            | ~/.local/bin/supervisord   |
+------------------------+----------------------------+
| Supervisorctl          | ~/.local/bin/supervisorctl |
+------------------------+----------------------------+

Setting new values
------------------

To set new paths and file locations, run Manager like:

.. code-block:: text

    qldsmanager configure <arguments>

.. note::

    You can get list of available arguments with

    .. code-block:: text

        qldsmanager configure --help

    It will display help block

Available arguments are

+---------------------+------------+------------------------------------------------------------+
| Argument            | Type       | Description                                                |
+=====================+============+============================================================+
| ``--steamcmd``      | Directory  | Location for SteamCMD                                      |
+---------------------+------------+------------------------------------------------------------+
| ``--ql``            | Directory  | Location for QL server files                               |
+---------------------+------------+------------------------------------------------------------+
+---------------------+------------+------------------------------------------------------------+
| ``--servers``       | File       | Server list configuration file                             |
+---------------------+------------+------------------------------------------------------------+
| ``--rcon``          | File       | Optional rcon list configuration file                      |
+---------------------+------------+------------------------------------------------------------+
+---------------------+------------+------------------------------------------------------------+
| ``--supervisor``    | Executable | Supervisord executable (eg.: ``/usr/bin/supervisord``)     |
+---------------------+------------+------------------------------------------------------------+
| ``--supervisorctl`` | Executable | Supervisorctl executable (eg.: ``/usr/bin/supervisorctl``) |
+---------------------+------------+------------------------------------------------------------+

.. note::

    You can set more than one argument at a time in any order, eg..:

    .. code-block:: text

        qldsmanager configure --servers ~/qlds_servers --ql ~/qlds_ql_files