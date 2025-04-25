#!/bin/sh
#
/usr/local/bin/startup.sh &
php-fpm -D &
wait
