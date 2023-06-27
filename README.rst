:code:`Django REST` ful API to serve requests by the `NebulaNews frontend`_.

.. _NebulaNews frontend: https://github.com/Levee-Solutions/nebulanews-spa

.. contents:: Table of contents

Installation
============
Environment variables
---------------------
The ``Django settings`` module expects some environment variables to properly work. These are defined in ``.env.example``, which you can copy and rename: ::

    $ cp .env.example .env

Run the project
---------------
You can run the project as a Docker container by running ::

    $ docker compose -f dev.yml up

This will look for a local Docker image for the project, and create it if it doesn't exist. All packages present in ``requirements.txt`` will be installed in the virtual environment.

Database
--------
To populate the Postgres database, you can download the `MIND dataset`_ files (we recommend the **MIND-small** version for testing).

.. _Mind dataset: https://msnews.github.io/

Once you have them, run the following commands to upload the articles and interactions: ::

    $ docker compose -f dev.yml run --rm nebula-django python src/manage.py import_mind_news --file <path to news.tsv file>
