__author__ = 'alanh'

import json
import requests
from KSATConnectionParameters import schedulingParameters as sp
from Response import Response


class RequestHandler():

    def __init__(self):
        self.headers = {'content-type': 'application/json'}

    def _reservationUrl(self):
        return "http://%s:%d%sreservations" % (sp['host'], sp['port'], sp['baseUrl'])

    def _antennaAvailabilityUrl(self):
        return "http://%s:%d%santennas/availability" % (sp['host'], sp['port'], sp['baseUrl'])

    def postReservations(self, requestJsonObject):
        r = requests.post(self._reservationUrl(), json.dumps(requestJsonObject), headers = self.headers)
        response = Response(r.status_code, r.reason, json.loads(r.text))
        return response

    def getAntennaAvailability(self, startDate, endDate):
        dates = {'startDate' : startDate, 'endDate' : endDate }
        r = requests.get(self._antennaAvailabilityUrl(), params = dates,  headers = self.headers)
        response = Response(r.status_code, r.reason, json.loads(r.text))
        return response

    def postAntennaAvailability(self, requestJsonObject):
        r = requests.post(self._antennaAvailabilityUrl(), json.dumps(requestJsonObject), headers = self.headers)
        response = Response(r.status_code, r.reason, json.loads(r.text))
        return response


