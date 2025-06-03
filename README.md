# SS13 VOX

TTS-based announcer inspired by Half Life's announcement system.

**This project was originally written in 2013 when the original creator was still learning python, so it's a bit rough around the edges.** 

This has been tested on WSL2 Ubuntu. You don't need a whole VM for it, look into Windows Subsystem for Linux.

## Installing
1. Clone this repository, duh.

### Automated Installation
1. Run `sudo bash setup.sh` 

### Manual Installation
1. Run `apt install festival festlex-cmu festlex-poslex festlex-oald festvox-rablpc16k libestools2.5 unzip sox vorbis-tools ffmpeg python3 python3-pip -y` to get all the damned packages you need.
3. Go into `hts_tmp` then do `for f in *.tar.*; do tar -xvf "$f"; done` (this loops through every directory. alternatively just unzip it all yourself, all goes into lib/)
4. While still in `hts_tmp`, do `sudo cp -r lib/voices/us /usr/share/festival/voices/`
5. You can't avoid using scripts, buddy. Exit out of `hts_tmp` and do `sudo bash fix.sh`.
6. You're done!

## Generating Sounds

### /vg/-based Servers (UNTESTED)
1. Open `config.yml`
1. Change `codebase` to `vg` so it'll generate the correct code for your server.
Simply edit `wordlists/vg` to taste, and run generate.sh.

Everything you need will end up in `dist/`. Note that old HL VOX sounds like `beep`, `bloop`, etc are not included and are expected to be in `sound/vox/`.

If words come out incorrectly pronounced, add the word to lexicon.txt following the guide at the top of the file. This will generate the required LISP script for you.

### TG-based Servers
You may also wish to duplicate `announcements.txt` and `voxwords.txt` and modify them for TG's needs.  If you choose to do this, make sure to point to the new files in `config.yml`.

# Changing Voices (UNTESTED)
You can select which voice to use for each sex in `config.yml` in the `voices:` list.

## Voice Sexes
<table><tr><th>Sex</th><th>Meaning</th></tr>
<tr><th><code>default</code></th><td>Non-AI automated announcements, like <code>vox_login</code>.</td></tr>
<tr><th><code>fem</code></th><td>Feminine voice</td></tr>
<tr><th><code>mas</code></th><td>Masculine voice</td></tr>
</table>

## Voice IDs
Each voice requires manual tuning and fuckery in order to work with the standardized echoes and reverbs added later during generation, so not every voice in festival is available here.

<table><tr><th>ID</th><th>Sex</th><th>Festival ID</th><th>Notes</th></tr>
<tr><th><code>us-clb</code></th><td>F</td><td><code>nitech_us_clb_arctic_hts</code></td><td>Used by default on /vg/.  US female with no accent.</td></tr>
<tr><th><code>us-rms</code></th><td>M</td><td><code>nitech_us_rms_arctic_hts</code></td><td>Used by default on /vg/.  US male with no accent, sounds kinda like DECTalk without post-processing.</td></tr>
<tr><th><code>us-slt</code></th><td>F</td><td><code>nitech_us_slt_arctic_hts</code></td><td>US female with midwestern accent and flatter voice. Buggy at times: Can drop to a british accent.</td></tr>
</table>

# Adding to the List

Simply edit the `common.txt` in wordlists/, according to the following format:

```
monkey
horse
```

# Words don't sound right
If words are pronounced weirdly, you can specify this in `lexicon.txt`. Read `LEXICON-README.md` for info on that.

# Testing Phrases (UNTESTED)

To test a phrase as though it were from in-game, run (replace `$SEX` with `fem` or `mas`):

```shell
$ python3 test.py --voice=$SEX sarah connor please report to medbay for johnson inspection
```

This will call `play` for you.

# Fixing Generated Code

Coding standards change over time, and this repo is relatively slow to update.  

If you need different dm output, please see `templates/` and edit the appropriate file (`vglist.jinja` or `tglist.jinja`).  Once done, run `generate.sh` again.  Afterwards, please send us a PR so everyone else gets the update.