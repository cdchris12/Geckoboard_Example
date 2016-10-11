#!/usr/bin/python
import requests
import json
import os
import sys

# Construct the path to our config file's expected location
loc_str = os.path.dirname( os.path.realpath( sys.argv[0]))
loc_str += "/config.json"

try:
    with open(loc_str, "rw") as fp:
        CONFIG = json.load(fp)
    # End with
except IOError, e:
    exit("No configuration file was found or the configuration file is invalid!!\n\nPlease make sure \"config.json\" exists in the same directory as this script and that it contains vaild JSON data!")
# End try/except block

def main():
    pass
# End def

if __name__ == "__main__":
    main()
# End if