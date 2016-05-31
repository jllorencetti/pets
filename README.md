[![Code Climate](https://codeclimate.com/github/dirtycoder/pets/badges/gpa.svg)](https://codeclimate.com/github/dirtycoder/pets)
[![Build Status](https://travis-ci.org/dirtycoder/pets.svg?branch=next)](https://travis-ci.org/dirtycoder/pets)
[![Coverage Status](https://coveralls.io/repos/github/dirtycoder/pets/badge.svg?branch=next)](https://coveralls.io/github/dirtycoder/pets?branch=next)
[![Requirements Status](https://requires.io/github/dirtycoder/pets/requirements.svg?branch=next)](https://requires.io/github/dirtycoder/pets/requirements/?branch=next)

## Pets

It's a website where people can publish their lost pets,
and pets available for adoption.

Users can create an account with a username and password,
or they can use Twitter and Facebook to login. You can
also extend it to use other providers as I use
python-social-auth here.

Images uploaded by users are cropped with easy-thumbnails
to improve the site performance.

It's still a work in progress


### How to contribute to the project

1. Fork and clone the repository;
2. Configure your instance;
   * Remember to configure the username, password and database in your postgreSQL. 
3. Install Pillow dependencies;
4. Install PhantonJS, see the julionc [tutorial](https://gist.github.com/julionc/7476620);
5. Install project requirements;
6. Execute all tests, it will take some minutes. 

```console
git clone https://github.com/<username>/pets.git && cd pets
cp contrib/sample-env pets/.env
sudo apt-get install python-dev python3.x-dev libjpeg8-dev 
#Install PhantomJS
pip install -r requirements.txt
cd pets && python manage.py test
```

__Some observations:__
* Use Python 3.4 or newer; 
* In order to make development and deploy to production simpler there's two settings module 'dev' for development and 'prod' for production, both based on the 'base' settings.
* Do not make changes if some test fail. Ask for help.