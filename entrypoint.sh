#!/usr/bin/env sh
gunicorn -k uvicorn.workers.UvicornWorker -w 3 -b 0.0.0.0:80 -t 360 --reload --access-logfile - main:app
#& gunicorn --access-logfile - -k --ca_certs ca_certs.txt uvicorn.workers.UvicornWorker -w 3 -b 0.0.0.0:8443 -t 360 --reload --access-logfile - app:app