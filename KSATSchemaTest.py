'''
Created on Jul 29, 2015

@author: alanh
'''

import unittest
from jsonschema import ValidationError
from SchemaTestUtils import validateWithChecker, loadSchemaFor
from DataSimulator import reservationRequest


class KSATSchemaTest(unittest.TestCase):

    def testValidateDateTime(self):
        schema = {
            "type": "object",
            "properties": {
                "price": {"type": "number"},
                "name": {"type": "string"},
                "expirationDate": {"type": "string", "format": "date-time"}
            }
        }
        try:
            validateWithChecker({"name": "Eggs", "price": 34.99, "expirationDate": "xxx"}, schema)
        except ValidationError as e:
            print e.message
            pass

    def testMinLengthString(self):
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string", "minLength": 1}
            }
        }
        validateWithChecker({"name": "SkySat-1"}, schema)

        try:
            validateWithChecker({"name": ""}, schema)
        except ValidationError as e:
            print "testMinLenghtString %s" % e.message
            pass

    def testFixedLengthString(self):
        schema = {
            "type": "object",
            "properties": {
                "line1": {"type": "string", "minLength": 69, "maxLength": 69}
            }
        }

        validateWithChecker({"line1": "1 39418U 13066C   15041.51375279  .00003665  00000-0  32287-3 0  9996"}, schema)

        try:
            validateWithChecker({"line1": "1 39418U 13066C   15041.51375279  .00003665  00000-0  32287-3 0"}, schema)  # shortened
        except ValidationError as e:
            print "testValidateWithinRange %s" %e.message
            pass

    def testValidateWithinRange(self):
        schema = {
            "type": "object",
            "properties": {
                "azimuth": {"type": "number", "format": "float", "minimum": 0.0, "maximum": 360,
                            "exclusiveMaximum": True}
            }
        }
        validateWithChecker({"azimuth": 0.1}, schema)
        validateWithChecker({"azimuth": 359.9999}, schema)

        try:
            validateWithChecker({"azimuth": 360}, schema)
        except ValidationError as e:
            print e.message
            pass

        try:
            validateWithChecker({"azimuth": -0.1}, schema)
        except ValidationError as e:
            print "testValidateWithinRange: %s" % e.message
            pass

    def testValidateBelowMaximum(self):
        schema = {
            "type": "object",
            "properties": {
                "latitude": {"type": "number", "format": "float", "minimum": -180, "maximum": 180,
                             "exclusiveMinimum": True, "exclusiveMaximum": True}
            }
        }
        validateWithChecker({"latitude": -179.999}, schema)
        validateWithChecker({"latitude": 179.9999}, schema)

        try:
            validateWithChecker({"latitude": 180}, schema)
        except ValidationError as e:
            print e.message
            pass

        try:
            validateWithChecker({"latitude": -180}, schema)
        except ValidationError as e:
            print "testValidateBelowMaximum: %s" % e.message
            pass

    def testPattern(self):
        schema = {
            "type": "object",
            "properties": {
                "line1": {"type": "string",
                          "pattern": "^1"
                          }
            }
        }
        validateWithChecker({"line1": "1 39418U 13066C   15041.51375279  .00003665  00000-0  32287-3 0  9996"}, schema)

        try:
            validateWithChecker({"line1": "2 39418U 13066C   15041.51375279  .00003665  00000-0  32287-3 0  9996"}, schema)
        except ValidationError as e:
            print  "testPattern: %s" % e.message
            pass

    def testValidateMinArraySize(self):
        schema = {
            "type": "object",
            "properties": {
                "tags": {
                    "type": "array",
                    "items": {
                        "type": "number"
                    },
                    "minItems": 1
                }
            },
            "required" : ["tags"]

        }

        validateWithChecker({"tags": [1,]}, schema)
        validateWithChecker({"tags": [1,2]}, schema)

        try:
            validateWithChecker({"tags": []}, schema)
        except ValidationError as e:
            print  "testValidateMinArraySize: %s" % e.message
            pass


    def testValidateReservationRequest(self):
        schema = loadSchemaFor("ReservationRequest")
        request = reservationRequest()
        validateWithChecker(request, schema)

    def testValidateDateFormat(self):
        schema = loadSchemaFor("ReservationRequest")
        request = reservationRequest()
        request['availabilityReportDate'] = "xyz"
        try:
            validateWithChecker(request, schema)
            self.fail()
        except ValidationError as e:
            print e.message
            pass


    def reservationRequestWithErrors(self):
        request = reservationRequest()
        request['availabilityReportDate'] = "bogus-date"
        return request

if __name__ == "__main__":
    unittest.main()
