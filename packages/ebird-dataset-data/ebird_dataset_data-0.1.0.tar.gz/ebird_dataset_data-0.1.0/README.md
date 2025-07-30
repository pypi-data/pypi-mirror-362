# eBird Dataset Data

eBird Dataset Data is a reusable Django app for loading data from the 
[eBird Basic Dataset](https://science.ebird.org/en/use-ebird-data/download-ebird-data-products),
v1.14, into a database.

## Overview

The Cornell Laboratory of Ornithology in Ithaca, New York runs the eBird database
which collects observations of birds from all over the world, and publishes them
on (eBird.org)[https://ebird.org]. The data is also available via the 
[eBird Basic Dataset](https://science.ebird.org/en/use-ebird-data/download-ebird-data-products) which is intended for for analysis and modelling.
This project contains a loader and models to take data from a download (CSV) file 
and load it into a database. From there you can analyse the data with python, 
jupyter notebooks, or build a web site.

To get started, you will need to [sign up](https://secure.birds.cornell.edu/identity/account/create) for an eBird account, 
then [request access](https://ebird.org/data/download), which usually takes 7 days to be reviewed and approved.

## Install

You can use either [pip](https://pip.pypa.io/en/stable/) or [uv](https://docs.astral.sh/uv/)
to download the [package](https://pypi.org/project/ebird-dataset-data/) from PyPI and
install it into a virtualenv:

```shell
pip install ebird-dataset-data
```

or:

```shell
uv add ebird-dataset-data
```

Update `INSTALLED_APPS` in your Django setting:

```python
INSTALLED_APPS = [
    ...
    ebird.dataset.data
]
```

Finally, run the migrations to create the tables:

```python
python manage.py migrate
```

## Demo

If you check out the code from the repository there is a fully functioning
Django site. It contains pages for checklists, observations and species,
where you can browse the records or search by location, observer. date. etc. 
The Django Admin lets you browse and edit the records in the database.

```shell
git clone git@github.com:StuartMacKay/ebird-dataset-data.git
cd ebird-api-data
```

Create the virtual environment:
```shell
uv venv
```

Activate it:
```shell
source .venv/bin/activate
```

Install the requirements:
```shell
uv sync
```

Run the database migrations:
```shell
python manage.py migrate
```

Create a user:
```shell
python manage.py createsuperuser
```

Run the demo:

```shell
python manage.py runserver
```

Now, either visit the site, http:localhost:8000/, or log into the Django Admin, 
http:localhost:8000/admin to browse the tables.

## Project Information

* Documentation: https://ebird-dataset-data.readthedocs.io/en/latest/
* Issues: https://todo.sr.ht/~smackay/ebird-dataset-data
* Repository: https://git.sr.ht/~smackay/ebird-dataset-data
* Announcements: https://lists.sr.ht/~smackay/ebirders-announce
* Discussions: https://lists.sr.ht/~smackay/ebirders-discuss
* Development: https://lists.sr.ht/~smackay/ebirders-develop

The repository is also mirrored on Github:

* Repository: https://github.com/StuartMacKay/ebird-dataset-data

The app is tested on Python 3.10+, and officially supports Django 4.2 LTS, 5.0, 5.1, and 5.2 LTS.

# License

eBird Dataset Data is released under the terms of the [MIT](https://opensource.org/licenses/MIT) license.
