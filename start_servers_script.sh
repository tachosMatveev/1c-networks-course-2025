#!/bin/bash

gunicorn --bind 0.0.0.0:8081 server:app --workers 4 &
gunicorn --bind 0.0.0.0:8082 server:app --workers 4 &
gunicorn --bind 0.0.0.0:8083 server:app --workers 4 &

