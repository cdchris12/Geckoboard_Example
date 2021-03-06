#!/usr/bin/python
import requests
import json
import os
import sys
import arrow
from requests.auth import HTTPDigestAuth
from time import sleep

# This flag enables or disables the usage of weather information from my personal Raspberry Pi. If you're not me, you probably want to set this flag to false. Note that this will break the script, though...
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
    
    W_API_Key = CONFIG["W_API_Key"] # W Underground's API Key
    G_API_Key = CONFIG["G_API_Key"] # Geckoboard's API Key
    RPi_Address = CONFIG["RPi_Address"] # Raspberry Pi's web address

    if W_API_Key == "" or G_API_Key == "":
        exit("One of the API keys is blank!!\n\nPlease make sure that both API key fields are populated prior to running this script")
    # End if
    
    while True:
        # Get data from W Underground's API
        calc_wx = getWxInfo(W_API_Key)
    
        # Get data from the Raspberry Pi in my basement
        if RPi:
            real_wx = getRPiInfo(RPi_Address)
        else:
            real_wx = {}
        # End if/else block
    
        # Prepare the two dicts to be sent to Geckoboard
        to_send = prepareData(calc_wx, real_wx)
    
        # Send the prepared data to Geckoboard
        ret = sendData(to_send, G_API_Key)
        if not ret:
            exit("Something is wrong with the API call to Geckoboard!!")
        else:
            print "Pushed some data!\nSleeping for 10 minutes..."
        # End if
        
        # Sleep for 10 minutes
        sleep(600)
    # End while
# End def

def getWxInfo(_key):
    # Input is an API key for W Underground
    # Output is a dict containing the following values:
    #   Air Temp
    #   Humidity
    #   Pressure
    
    s = requests.Session()
    r = s.get("http://api.wunderground.com/api/%s/conditions/q/ND/Grand_Forks.json" % _key)
    
    if r.status_code == 200:
        json_data = json.loads(r.text)
        
        parsed_data = {}
        parsed_data["temperature"] = float(json_data["current_observation"]["temp_f"])
        parsed_data["pressure"] = float(json_data["current_observation"]["pressure_mb"])
        parsed_data["humidity"] = float(json_data["current_observation"]["relative_humidity"].replace("%", ""))
        
        s.close()
        
        return parsed_data
    else:
        return {}
    # End if/else block
# End def

def getRPiInfo(addr):
    # Input is the web address of my Raspberry Pi's server
    # Output is a dict containing the following values:
    #   Air Temp
    #   Humidity
    #   Pressure
    
    s = requests.Session()
    r = s.get(addr)
    
    if r.status_code == 200:
        json_data = json.loads(r.text)
        s.close()
        
        # The Raspberry Pi returns some seriously precise values; let's round them to the nearest tenth.
        ret_data = {}
        ret_data["temperature"] = round(json_data["temperature"], 1)
        ret_data["pressure"] = round(json_data["pressure"], 1)
        ret_data["humidity"] = round(json_data["humidity"], 1)
        
        return ret_data
    else:
        print r.status_code
        return {}
    # End if/else block
# End def

def prepareData(calc, real):
    # Input is two dicts
    # Output is a single dict
    
    json_data = {}
    json_data["timestamp"] = arrow.utcnow().format('YYYY-MM-DDTHH:mm:ss').encode('ascii','ignore') + "Z"
    json_data["b_temp"] = real["temperature"]
    json_data["b_press"] = real["pressure"]
    json_data["b_hum"] = real["humidity"] / 100
    json_data["o_temp"] = calc["temperature"]
    json_data["o_press"] = calc["pressure"]
    json_data["o_hum"] = calc["humidity"] / 100
    
    ret_data = {}
    ret_data["data"] = []
    ret_data["data"].append(json_data)
    
    return ret_data
# End def

def sendData(data, key):
    # Input is a dict of values and an API key to Geckoboard
    # Output is a boolean value indicating the success or failure of the API call
    
    headers = {'content-type': 'application/json'}
    
    
    s = requests.Session()
    r = s.post("https://api.geckoboard.com/datasets/weather_data/data", auth=(key, ""), data=json.dumps(data), headers=headers)
    
    if r.status_code == 200:
        return True
    else:
        return False
    # End if/else block
# End def

if __name__ == "__main__":
    main()
# End if