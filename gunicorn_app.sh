#!/usr/bin/env bash
pipenv run gunicorn --bind 0.0.0.0:8079 pilot2019.app:application
