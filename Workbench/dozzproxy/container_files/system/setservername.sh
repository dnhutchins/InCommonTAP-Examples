#!/bin/bash

files="/etc/shibboleth/idp-metadata.xml /etc/shibboleth/shibboleth2.xml"

for file in $files
  do
    sed -i "s|__SERVERNAME__|$SERVERNAME|g" $file
  done

