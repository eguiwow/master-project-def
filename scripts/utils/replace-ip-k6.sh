#!/bin/bash

root_folder="/home/eguiwow/THESIS/tts-thesis-master/k6-test-GL6"
old_ip="145.108.225.16"
new_ip="145.108.225.17"
old_name="MadaDinga"
new_name="AnderEguiluz"

# Find all .js files in the root folder and its subfolders
find "$root_folder" -type f -name "*.js" -print0 | while IFS= read -r -d '' file_path; do
    # Replace the old IP with the new IP in the file
    sed -i "s/$old_ip/$new_ip/g" "$file_path"
    sed -i "s/$old_name/$new_name/g" "$file_path"
done

echo "IP replacement completed successfully."
