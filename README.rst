:code:`Django REST`ful API to serve requests by the `NebulaNews frontend`_.

.. _NebulaNews frontend: https://github.com/Levee-Solutions/nebulanews-spa

.. contents::

Installation
============
Environment variables
---------------------
The `Django settings` module expects some environment variables to properly work. These are defined in `.env.example`, which you can copy and rename:
.. code:: bash

    cp .env.example .env

Run the project
---------------
You can run the project as a Docker container by running
.. code::bash

    docker compose -f dev.yml up

This will look for a local Docker image for the project, and create it if it doesn't exist. All packages present in `requirements.txt` will be installed in the virtual environment.

We use Poetry to efficiently manage the dependencies of the project.
