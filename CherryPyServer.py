#!/usr/bin/python

# Due to the direct hardware requirements of the Sense Hat framework, this script must be ran as root!!

import cherrypy
from sense_hat import SenseHat
import json

# Instantiate only one SenseHat object, which we will route every request through 
sense = SenseHat()

class SenseHatServer(object):
    @cherrypy.expose
    
    def index(self):
        data = {}
        
        # Convert from Celcius to Farenheit
        temp = sense.get_temperature()
        temp *= 9.0
        temp /= 5.0
        temp += 32.0 # Gotta use 32.0, because we want to add a float to a float
        
        # Populate return data structure
        data["humidity"] = sense.get_humidity()
        data["temperature"] = temp
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