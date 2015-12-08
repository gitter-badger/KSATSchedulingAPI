from TimeUtils import datetimeAsIso8601
from copy import deepcopy
import json
from datetime import datetime as dt
import cherrypy

from TimeUtils import doWindowsOverlap

class Reservations():

    exposed = True

    def POST(self, **request):
        cl = cherrypy.request.headers['Content-Length']
        rawbody = cherrypy.request.body.read(int(cl))
        body = json.loads(rawbody)
        availabilityList = antennaAvailability()
        (deniedCount, response) = processReservation(body, availabilityList)

        cherrypy.response.status = 409 if deniedCount > 0 else 201

        return json.dumps(response)



class AntennaAvailability():

    exposed = True

    def GET(self, startDate, endDate):
        # date params ignored for now
        cherrypy.response.status = 200
        return json.dumps(antennaAvailability())

    def POST(self):
        cl = cherrypy.request.headers['Content-Length']
        rawbody = cherrypy.request.body.read(int(cl))
        with open('AntennaAvailability.json', 'w') as fp:
            fp.write(rawbody)
        body = json.loads(rawbody)
        cherrypy.response.status = 201
# TODO what do I return
        return json.dumps(antennaAvailability())

def antennaAvailability():
    with open("AntennaAvailability.json", "r") as fp:
        data = fp.read()
    availabilityList = json.loads(data)

    return availabilityList


def processReservation(requestJson, antennaAvailabilityList):
        processedTime = datetimeAsIso8601(dt.now())

        reservationRequest = deepcopy(requestJson)
        deniedCount = 0
        for antenna in reservationRequest['contactPlan']['antennas']:
            antennaId =  antenna['id']
            for contact in antenna['contacts']:
                for antenna in antennaAvailabilityList['antennas']:
                    if antenna['antennaId'] == antennaId :
                        denied = False
                        for window in antenna['outOfServiceWindows']:
                            overlap = doWindowsOverlap(contact['startTime'], contact['stopTime'], window['startTime'], window['stopTime'])
                            denied = denied or overlap


                        contact['status'] = ('DENIED_OUT_OF_SERVICE' if denied else 'RESERVED')
                        contact['processedTime'] = processedTime
                        if denied:
                            deniedCount +=1

        return (deniedCount, reservationRequest)

def startService():
    conf = {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()} }
    cherrypy.tree.mount(Reservations(), "/v1/reservation-api/reservations", conf)
    cherrypy.tree.mount(AntennaAvailability(), '/v1/reservation-api/antennas/availability', conf)
    cherrypy.config.update({'server.socket_port': 9090})
    cherrypy.engine.start()

def stopService():
    cherrypy.engine.exit()

if __name__ == '__main__':
    startService()
