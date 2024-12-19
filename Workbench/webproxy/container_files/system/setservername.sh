#!/bin/bash

files="/etc/shibboleth/idp-metadata.xml /var/www/html/index.html /mdload/grouper-sp.xml /mdload/midpoint-sp.xml /mdload/mpproxy-sp.xml /mdload/comanage-sp.xml /mdload/proxy-sp.xml /mdload/wordpress-sp.xml /mdload/match-sp.xml"

for file in $files
  do
    sed -i "s|__CSPHOSTNAME__|$CSPHOSTNAME|g" $file
  done

