#!/bin/bash

cd /usr/share/festival/voices/us
find . -name '*.scm' | while read -r file; do
  sed -i.bak \
    -e "s/(require 'hts)/(require 'hts21compat)/g" \
    -e "s/(Parameter.set 'Synth_Method 'HTS)/(Parameter.set 'Synth_Method 'HTS21)/g" \
    "$file"
done