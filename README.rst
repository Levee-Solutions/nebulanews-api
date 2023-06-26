:code:`Django RESTful API` API to serve requests by the `NebulaNews frontend`_.

.. _NebulaNews frontend: https://github.com/Levee-Solutions/nebulanews-spa

.. contents:: Table of Contents

Installation
============
Environment variables
---------------------
The `Django settings` module expects some environment variables to properly work. These are defined in :code:`.env.example`, which you can copy and rename:

    cp .env.example .env

Run the project
---------------
You can run the project as a Docker container by running

    docker compose -f dev.yml up

This will look for a local Docker image for the project, and create it if it doesn't exist. All packages present in :code:`requirements.txt` will be installed in the virtual environment.

We use Poetry to efficiently manage the dependencies of the project.
