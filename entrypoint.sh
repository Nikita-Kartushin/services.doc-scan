#!/bin/bash

# ALPINE
# rc-update add nginx default
# rc-status
# touch /run/openrc/softlevel
# Релоад конфигурации nginx
# service nginx restart

# DEBIAN
service nginx start
service nginx -s reload

# запуск
export LOGPATH="logs/services.doc-scan.log"
gunicorn --workers 4 \
         --worker-class aiohttp.GunicornWebWorker \
         --bind 127.0.0.1:6160 \
         --log-level INFO \
         --name "services.doc-scan" \
         --log-file "$LOGPATH" \
         --access-logfile "$LOGPATH" \
         run:create_wsgi_app
