#!/bin/bash

apt install festival festlex-cmu festlex-poslex festlex-oald festvox-rablpc16k libestools2.5 unzip sox vorbis-tools ffmpeg python3 python3-pip -y

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

echo "Should be done!"
echo "Move on to "Generating Sounds"