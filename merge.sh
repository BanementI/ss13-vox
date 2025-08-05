#!/bin/bash
# yeah i use AI generated scripts, fuck you
# also yeah this only works for me so change it to ur config lol

# Paths
NEW_FILE="/mnt/c/Users/bane/Documents/ss13-vox-master/dist/code/modules/mob/living/silicon/ai/vox_sounds.dm"
MAIN_FILE="/mnt/c/Users/bane/Documents/Monkestation2.0/code/modules/mob/living/silicon/ai/vox_sounds.dm"
TMP_MERGED=$(mktemp)

# Function to extract list content and strip leading/trailing blank lines
extract_list() {
    grep -Pzo '(?s)(?<=GLOBAL_LIST_INIT\(vox_sounds, list\().*?(?=\)\))' "$1" \
    | tr -d '\0' \
    | sed '/^[[:space:]]*$/d'
}

# Extract lists
extract_list "$MAIN_FILE" > main_list.txt
extract_list "$NEW_FILE" > new_list.txt

# Merge and sort by the text inside quotes
cat main_list.txt new_list.txt | sort -u -t '"' -k2,2 > "$TMP_MERGED"

# Replace the section in MAIN_FILE
awk -v replacement="$(<"$TMP_MERGED")" '
    BEGIN { in_list = 0 }
    /GLOBAL_LIST_INIT\(vox_sounds, list\(/ { print; print replacement; in_list = 1; next }
    in_list && /\)\)/ { in_list = 0; print; next }
    !in_list { print }
' "$MAIN_FILE" > "${MAIN_FILE}.tmp" && mv "${MAIN_FILE}.tmp" "$MAIN_FILE"

# Cleanup
rm -f main_list.txt new_list.txt "$TMP_MERGED"

echo "Merge complete: $MAIN_FILE updated."

# now we should move the audio files
mv /mnt/c/Users/bane/Documents/ss13-vox-master/dist/sound/announcer/vox_fem/* "/mnt/c/Users/bane/Documents/Monkestation2.0/sound/announcer/vox_fem/"
echo "Moved audio files, probably."
