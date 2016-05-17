[![Code Climate](https://codeclimate.com/github/dirtycoder/pets/badges/gpa.svg)](https://codeclimate.com/github/dirtycoder/pets)
[![Build Status](https://travis-ci.org/dirtycoder/pets.svg?branch=next)](https://travis-ci.org/dirtycoder/pets)
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

In order to make development and deploy to production simpler there's two settings module.
'dev' for development and 'prod' for production, both based on the 'base' settings.

Look in the settings modules for environment variables which need to be configured.