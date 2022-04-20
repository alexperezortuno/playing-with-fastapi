#!/bin/bash
app_port=$APP_PORT
app_host=$APP_HOST

if [ -z "$app_port" ]; then
    echo "Application port is not set. Using default port: 80"
    app_port=80
else
    echo "Application port: $app_port"
fi

if [ -z "$app_host" ]; then
    echo "Using default host: 0.0.0.0"
fi

gunicorn -k uvicorn.workers.UvicornWorker -w 3 -b "${app_host}:${app_port}" -t 360 --reload --access-logfile - main:app
#& gunicorn --access-logfile - -k --ca_certs ca_certs.txt uvicorn.workers.UvicornWorker -w 3 -b 0.0.0.0:8443 -t 360 --reload --access-logfile - app:app