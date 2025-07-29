eBird API Data
==============
eBird API Data is a reusable Django app for loading data from eBird into a database.

Overview
--------
.. overview-start

The Cornell Laboratory of Ornithology in Ithaca, New York runs the eBird database
which collects observations of birds from all over the world. All the observations
are published on `eBird.org`_, and they also make them available via an `API`_.
This project contains a loader and models to take data from the API and load it into
a database. From there you can analyse the data with python, jupyter notebooks, or
build a web site.

To get started, you will need to `sign up`_ for an eBird account, if you don't
already have one and `register`_ to get an API key. Make sure you read and
understand the `Terms of use`_, and remember bandwidth and servers cost money,
so don't abuse the service. If you need large numbers of observations, then
sign up to receive the `eBird Basic Dataset`_.

.. _eBird.org: https://ebird.org
.. _API: https://documenter.getpostman.com/view/664302/S1ENwy59
.. _sign up: https://secure.birds.cornell.edu/identity/account/create
.. _register: https://ebird.org/data/download
.. _Terms of use: https://www.birds.cornell.edu/home/ebird-api-terms-of-use/
.. _eBird Basic Dataset: https://science.ebird.org/en/use-ebird-data/download-ebird-data-products

.. overview-end

Install
-------
.. install-start

You can use either `pip`_ or `uv`_ to download the `package`_ from PyPI and
install it into a virtualenv:

.. code-block:: console

    pip install ebird-api-data

or:

.. code-block:: console

    uv add ebird-api-data

Update ``INSTALLED_APPS`` in your Django setting:

.. code-block:: python

    INSTALLED_APPS = [
        ...
        ebird.api.data
    ]

Finally, run the migrations to create the tables:

.. code-block:: python

    python manage.py migrate

.. _pip: https://pip.pypa.io/en/stable/
.. _uv: https://docs.astral.sh/uv/
.. _package: https://pypi.org/project/ebird-api-data/

.. install-end

Demo
----

.. demo-start

If you check out the code from the repository there is a fully functioning
Django site. It only contains the admin pages, but that is sufficient for
you to browse the data.

.. code-block:: console

    git clone git@github.com:StuartMacKay/ebird-api-data.git
    cd ebird-api-data

Create the virtual environment:

.. code-block:: console

    uv venv

Activate it:

.. code-block:: console

    source venv/bin/activate

Install the requirements:

.. code-block:: console

    uv sync

Run the database migrations:

.. code-block:: console

    python manage.py migrate

Create a user:

.. code-block:: console

    python manage.py createsuperuser

Create a copy of the .env.example file and add your API key:

.. code-block:: console

    cp .env.example .env

.. code-block:: console

    EBIRD_API_KEY=<my api key>

Now, download data from the API:

.. code-block:: console

    python manage.py add_checklists --days 2 US-NY-109

This loads all the checklists, submitted in the past two days by birders in
Tompkins County, New York, where the Cornell Lab is based. You can use any
location code used by eBird, whether it's for a country, state/region, or
county. Remember, read the terms of use.

Run the demo:

.. code-block:: console

    python manage.py runserver

Now log into the `Django Admin <http:localhost:8000/admin>` to browse the tables.

.. demo-end

Project Information
-------------------

* Documentation: https://ebird-api-data.readthedocs.io/en/latest/
* Issues: https://github.com/StuartMacKay/ebird-api-data/issues
* Repository: https://github.com/StuartMacKay/ebird-api-data

The app is tested on Python 3.10+, and officially supports Django 4.2, 5.0 and 5.1.

eBird API Data is released under the terms of the `MIT`_ license.

.. _MIT: https://opensource.org/licenses/MIT
