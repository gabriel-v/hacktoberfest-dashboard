#!/bin/bash -ex

git pull
pipenv install
pipenv run ./manage.py migrate
( cd frontend; yarn build )

