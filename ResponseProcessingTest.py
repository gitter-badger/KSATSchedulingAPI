__author__ = 'alanh'

import unittest
from datetime import datetime as dt

from DataSimulator import reservationRequest, reservationRequestWithConflicts, antennaAvailability
from SchemaTestUtils import loadReservationResponseSchema, validateWithChecker, loadSchemaFor
from KSATSchedulingService import processReservation, antennaAvailability
from TimeUtils import datetimeAsIso8601, doWindowsOverlap


class ResponseProcessingTest(unittest.TestCase):

    def testDeconflictReservation(self):
        processedTime = datetimeAsIso8601(dt.now())

        reservationRequest = reservationRequestWithConflicts()

        availabilityList = antennaAvailability()
        for antenna in reservationRequest['contactPlan']['antennas']:
            antennaId =  antenna['id']
            for contact in antenna['contacts']:
                for antenna in availabilityList['antennas']:
                    if antenna['antennaId'] == antennaId :
                        denied = False
                        for window in antenna['outOfServiceWindows']:
                            overlap = doWindowsOverlap(contact['startTime'], contact['stopTime'], window['startTime'], window['stopTime'])
                            denied = denied or overlap

                        contact['status'] = ('DENIED_OUT_OF_SERVICE' if denied else 'RESERVED')
                        contact['processedTime'] = processedTime

        expectedStatusList = {
            'SkySat-A-rev1006-Fairbanks-1' :  'DENIED_OUT_OF_SERVICE',
            'SkySat-B-rev2209-Fairbanks-1' :  'RESERVED',
            'SkySat-A-rev1006-Fairbanks-2' :  'RESERVED',
            'SkySat-B-rev2209-Fairbanks-2' :  'DENIED_OUT_OF_SERVICE',
        }
        for antenna in reservationRequest['contactPlan']['antennas']:
            for contact in antenna['contacts']:
                # print  "'%s\' :  '%s'" % (contact['id'], contact['status'])
                self.assertEqual(contact['status'], expectedStatusList[contact['id']])
        pass


    def testProcessReservation(self):
        response = reservationResponse()
        minDateLength =  len('2015-09-29T13:52:35')
        for antenna in response['contactPlan']['antennas']:
            for contact in antenna['contacts']:
                self.assertEqual(contact['status'], 'RESERVED')
                self.assertGreater(len(contact['processedTime']), minDateLength)

    def testValidateReservationResponse(self):
        response = reservationResponse()
        responseSchema = loadReservationResponseSchema()
        validateWithChecker(response, responseSchema)

    def testValidateContactResponse(self):
        schema = loadSchemaFor("Contact")
        requiredList = schema['definitions']['Contact']['required']
        requiredList.append("status")
        requiredList.append("processedTime")

        processedTime = datetimeAsIso8601(dt.now())
        data = {
            "id":"SkySat-A-rev1006-Fairbanks-1",
            "satelliteName":"SkySat-1",
            "startTime": "2014-10-10T07:28:20.000Z",
            "stopTime": "2014-10-10T07:29:20.000Z",
            "status" : "RESERVED",
            "processedTime" : processedTime
        }
        validateWithChecker(data, schema)


    def testDeniedCode(self):
        deniedCount = 0
        value = 409 if deniedCount > 0 else 201
        print value

def reservationResponse():
    requestJson = reservationRequest()
    (deniedCount, response) = processReservation(requestJson, antennaAvailability())
    return response

if __name__ == '__main__':
    unittest.main()
