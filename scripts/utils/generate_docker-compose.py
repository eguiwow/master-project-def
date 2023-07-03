import sys
import re

# Path to the source Docker Compose YAML file
source_file = sys.argv[1]

# Path to the new Docker Compose YAML file
new_file = sys.argv[2]

# Value to set for the 'cpus' field
new_cpus_value = sys.argv[3]

# Iterate over each service in the compose data
with open(source_file, "r") as source_file, open(new_file, "w") as new_file:
    for line in source_file:
        # Search for lines that start with 'cpus:'
        if re.match(r"^\s*cpus:", line):
            # Replace the existing value with the new value
            line = f"    cpus: {new_cpus_value}\n"
        # Write the modified or original line to the output file
        new_file.write(line)