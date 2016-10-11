#!/usr/bin/python
import requests
import json
import os
import sys

# This flag enables or disables the usage of weather information from my personal Raspberry Pi. If you're not me, you probably want to set this flag to false.
RPi = True

# Construct the path to our config file's expected location
loc_str = os.path.dirname( os.path.realpath( sys.argv[0]))
loc_str += "/config.json"

# Try to open our config file, and exit gracefully if it isn't present or valid
try:
    with open(loc_str, "rw") as fp:
        CONFIG = json.load(fp)
    # End with
except IOError, e:
    exit("No configuration file was found or the configuration file is invalid!!\n\nPlease make sure \"config.json\" exists in the same directory as this script and that it contains vaild JSON data!")
# End try/except block

def main():
    #TODO:
    # Connect to Wunderground's API and get temperature data for Grand Forks every 10 minutes.
    # (Optional) Build some sort of API interface for your Raspberry pi which will serve out temperature information from its sense hat
    # Prepare the data returned from either/both of these sources for transmittal to Geckoboard's API
    # Upload the data to Geckoboard
    # Configure this to all run every 10 minutes
    
    W_API_Key = CONFIG["W_API_Key"] # W Underground's API Key
    G_API_Key = CONFIG["G_API_Key"] # Geckoboard's API Key

    if W_API_Key is "" or G_API_Key is "":
        exit("One of the API keys is blank!!\n\nPlease make sure that both API key fields are populated prior to running this script")
    # End if
    
    while True:
        # Get data from W Underground's API
        calc_wx = getWxInfo(W_API_Key)
    
        # Get data from the Raspberry Pi in my basement
        if RPi:
            real_wx = getRPiInfo()
        else:
            real_wx = {}
        # End if/else block
    
        # Prepare the two dicts to be sent to Geckoboard
        to_send = prepareData(calc_wx, real_wx)
    
        # Send the prepared data to Geckoboard
        sendData(to_send, G_API_Key)
        
        # Sleep for 10 minutes
        os.sleep(600)
    # End while
# End def

def getWxInfo(key):
    pass
# End def

def getRPiInfo():
    pass
# End def

def prepareData(calc, real):
    pass
# End def

def sendData(data, key):
    pass
# End def

if __name__ == "__main__":
    main()
# End if