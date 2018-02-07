# Pets

[![Code Climate](https://codeclimate.com/github/jllorencetti/pets/badges/gpa.svg)](https://codeclimate.com/github/jllorencetti/pets)
[![Build Status](https://travis-ci.org/jllorencetti/pets.svg?branch=master)](https://travis-ci.org/jllorencetti/pets)
[![Coverage Status](https://coveralls.io/repos/github/jllorencetti/pets/badge.svg?branch=master)](https://coveralls.io/github/jllorencetti/pets?branch=master)
[![Updates](https://pyup.io/repos/github/jllorencetti/pets/shield.svg)](https://pyup.io/repos/github/jllorencetti/pets/)

Pets is a website where people can publish lost pets
and pets available for adoption.

Users can create an account with a username and password,
or they can use their Twitter and Facebook to login. You can also extend it to use other providers as it's backed by [python-social-auth](https://pypi.python.org/pypi/python-social-auth).

Images uploaded by users are cropped with [easy-thumbnails](https://pypi.python.org/pypi/easy-thumbnails) to improve the site performance.

## Installing

### Requirements

* [Python](https://python.org) 3.4 or newer
* [PostgreSQL](https://www.postgresql.org) running with a _database_, _username_ and _password_ to be used with Pets.


### Fork and clone the repository

First fork the project using GitHub, than clone it locally:

```console
git clone https://github.com/<username>/pets.git
cd pets
```

### Configure your instance

The project configuration uses [python-decouple](https://pypi.python.org/pypi/python-decouple/) to dynamically read environment variables and `.env` files.

If you want, you can get started by copying `contrib/sample-env` as `.env`:

```console
cp contrib/sample-env pets/.env
```

Then you have to set following variables:

#### Basic Django settings

* **`SECRET_KEY`**: [Django's secret key](https://docs.djangoproject.com/en/1.8/ref/settings/#std:setting-SECRET_KEY)
* **`ALLOWED_HOSTS`** (e.g. `127.0.0.1, .localhost`) [Django's allowed hosts](https://docs.djangoproject.com/en/1.8/ref/settings/#allowed-hosts)
* **`DJANGO_SETTINGS_MODULE`**: In order to make development and deploy to production simpler there's two settings module; `pets.settings.dev` for development and `pets.settings.prod` for production.

#### Database

* **`DATABASE_URL`**: (e.g. `postgres://username:password@server:port/database_name`) [Database URL](https://github.com/kennethreitz/dj-database-url#url-schema)
* **`DB_CONN_MAX_AGE`**: (e.g. `0`) [Django's database `CONN_MAX_AGE`](https://docs.djangoproject.com/en/1.8/ref/settings/#std:setting-CONN_MAX_AGE`)

#### Email configuration

* **`SENDGRID_API_KEY`**: API key of you SendGrid account.
* **`DEFAULT_FROM_EMAIL`**: The email address that will be used as the `from` email field.

#### OAuth

If you want to login via social media, you will have to create apps as a developer [at Facebook](https://developers.facebook.com) and/or [Twitter](https://apps.twitter.com). Once you're done, set the _app secret_ and _app key_ for each of them:

* `SOCIAL_AUTH_FACEBOOK_KEY`
* `SOCIAL_AUTH_FACEBOOK_SECRET`
* `SOCIAL_AUTH_TWITTER_KEY`
* `SOCIAL_AUTH_TWITTER_SECRET`

### Other dependencies

#### Install Pillow dependencies

As Pets uses [Pillow](https://pypi.python.org/pypi/Pillow), some extra packages are needed. In a Debian based Linux this should do the job:

```console
sudo apt-get install python-dev python3.x-dev libjpeg8-dev 
```

#### Download ChromeDriver

You just need to download and unzip the latest [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) and place it somewhere in your search path.

### Install Python packages

```console
pip install -r requirements/local.txt
```

### Test

Execute all tests, it will take some minutes.

```console
cd pets
python manage.py test
```

Please, do not commit changes if any test fails. Ask for help here instead.