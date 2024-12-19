#!/bin/bash

files="/etc/shibboleth/idp-metadata.xml"

for file in $files
  do
    sed -i "s|__CSPHOSTNAME__|$CSPHOSTNAME|g" $file
  done


