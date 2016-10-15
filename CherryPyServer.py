#!/usr/bin/python

# Due to the direct hardware requirements of the Sense Hat framework, this script must be ran as root!!

import cherrypy
from sense_hat import SenseHat
import json

def toCelcius(temp):
    temp *= 9.0
    temp /= 5.0
    temp += 32.0
    
    return temp
# End def

# Instantiate only one SenseHat object, which we will route every request through 
sense = SenseHat()

class SenseHatServer(object):
    @cherrypy.expose
    
    def index(self):
        data = {}
        
        # Since the temperature sensor can be affected by the CPU heatsink heat dissipation, we're going to aggregate every temp we can get from the Pi, aggregate them together, and report back the average of the three
        temp_aggregate = sense.get_temperature() + sense.get_temperature_from_pressure() + sense. get_temperature_from_humidity()
        temp_aggregate /= 3
        
        # Populate return data structure
        data["humidity"] = sense.get_humidity()
        data["temperature"] = toCelcius( temp_aggregate )
        data["pressure"] = sense.get_pressure()
        
        return json.dumps(data)
    # End def
# End class

if __name__ == '__main__':
    
    cherrypy.config.update(
        {
            'server.socket_host': '0.0.0.0',
            'server.socket_port': 74,
        }
    )
    
    cherrypy.quickstart( SenseHatServer())
# End if