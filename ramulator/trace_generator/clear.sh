#!/bin/bash

# Input file
input_file=$1

# Output file
output_file=$2

# Process the file with awk
awk '{$NF=""; sub(/[[:space:]]+$/, ""); print $0}' "$input_file" > "$output_file"
