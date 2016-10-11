#!/usr/bin/python
import cherrypy
from sense_hat import SenseHat
import json

sense = SenseHat()

class SenseHatServer(object):
    @cherrypy.expose
    
    def index(self):
        data = {}
        data["humidity"] = sense.get_humidity()
        data["temperature"] = sense.get_temperature()
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