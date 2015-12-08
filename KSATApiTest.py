__author__ = 'alanh'
import unittest
import json

from RequestHandler import RequestHandler
from SchemaTestUtils import loadReservationResponseSchema, validateWithChecker, loadAntennaAvailabilitySchema
from DataSimulator import reservationRequest, reservationRequestWithConflicts, antennaAvailability
from KSATSchedulingService import startService, stopService

class KSATApiTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print '***** Service starting ********'
        startService()

    @classmethod
    def tearDownClass(cls):
        print '***** Service exiting ********'
        stopService()

    def testPostReservations(self):
        data = reservationRequest()
        requestHandler = RequestHandler()
        response = requestHandler.postReservations(data)

        self.assertEqual(201, response.status)
        self.assertEqual('Created', response.reason)

        responseSchema = loadReservationResponseSchema()
        validateWithChecker(response.body, responseSchema)

    def testReservationDenied(self):
        data = reservationRequestWithConflicts()
        requestHandler = RequestHandler()
        response = requestHandler.postReservations(data)

        self.assertEqual(409, response.status)
        self.assertEqual('Conflict', response.reason)

    def testGetAntennaAvailability(self):
        requestHandler = RequestHandler()

        startDate =  '2015-10-16T10:00:00Z'
        endDate =  '2015-10-17T10:00:00Z'

        response = requestHandler.getAntennaAvailability(startDate, endDate)

        self.assertEqual(200, response.status)
        self.assertEqual('OK', response.reason)

        responseSchema = loadAntennaAvailabilitySchema()
        validateWithChecker(response.body, responseSchema)



    def testPostAntennaAvailability(self):
        from datetime import datetime as dt
        from TimeUtils import datetimeAsIso8601

        data = antennaAvailability()
        data['generationDate'] = datetimeAsIso8601(dt.now())
        requestHandler = RequestHandler()
        response = requestHandler.postAntennaAvailability(data)
        self.assertEqual(201, response.status)




# Major Reservation Workflow

    def testReservationWorkflow(self):
# - Set Antenna Availabilty: this is testing step only
        from datetime import datetime as dt
        from TimeUtils import datetimeAsIso8601

        data = antennaAvailability()
        data['generationDate'] = datetimeAsIso8601(dt.now())
        requestHandler = RequestHandler()
        response = requestHandler.postAntennaAvailability(data)
        self.assertEqual(201, response.status)

        startDate =  '2015-10-16T10:00:00Z'
        endDate =  '2015-10-17T10:00:00Z'

        response = requestHandler.getAntennaAvailability(startDate, endDate)

        self.assertEqual(200, response.status)
        self.assertEqual('OK', response.reason)

# - Get Antenna Availabilty: this begins every reservation cycle
        startDate =  '2015-10-16T10:00:00Z'
        endDate =  '2015-10-17T10:00:00Z'

        response = requestHandler.getAntennaAvailability(startDate, endDate)
        # TODO capture generation date from availability report

        self.assertEqual(200, response.status)
        self.assertEqual('OK', response.reason)
        responseSchema = loadAntennaAvailabilitySchema()
        validateWithChecker(response.body, responseSchema)

# - Update (POST) reservations.
        data = reservationRequest()
        # TODO consider: do we inject the date form our antenna avail report at this point? Or let service do that
        # TODO update generation date in reservation request before posting
        requestHandler = RequestHandler()
        response = requestHandler.postReservations(data)

        self.assertEqual(201, response.status)
        self.assertEqual('Created', response.reason)
        # TODO assert expected generation date in response

        responseSchema = loadReservationResponseSchema()
        validateWithChecker(response.body, responseSchema)

if __name__ == "__main__":
    unittest.main()
