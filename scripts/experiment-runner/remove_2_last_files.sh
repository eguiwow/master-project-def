#!/bin/bash
# remove last 2 files of an specific folder
# $1 <path/to/folder>
ls -t "$1" |
  head -n 2 |
  xargs -I {} rm -f "$1/{}"