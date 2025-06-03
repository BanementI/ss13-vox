#!/bin/bash

# Doing build-tools
echo "Installing build-tools"
cd python-build-tools
sudo -u "$SUDO_USER" pip install .
cd ..

# Where the voices are stored!
cd hts_tmp

# Unzips everything to lib/
for f in *.tar.*; do tar -xvf "$f"; done

# Copying it to usr/share
mkdir -p /usr/share/festival/voices/us
echo "Copying files..."
cp -r lib/voices/us /usr/share/festival/voices/

# Doing the necessary "fixes" (i dont really know what these do)
cd /usr/share/festival/voices/us
find . -name '*.scm' | while read -r file; do
  sed -i.bak \
    -e "s/(require 'hts)/(require 'hts21compat)/g" \
    -e "s/(Parameter.set 'Synth_Method 'HTS)/(Parameter.set 'Synth_Method 'HTS21)/g" \
    "$file"
done

