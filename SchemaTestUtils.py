__author__ = 'alanh'

import json
from jsonschema import validate, FormatChecker
from copy import deepcopy

def validateWithChecker(data, schema):
    validate(data, schema, format_checker=FormatChecker())

def loadBaseSchema():
    fp1 = open("SchemaTemplate.json").read()
    baseSchema = json.loads(fp1)

    fp2 = open("KSATSchema.swagger.json")
    swaggerSchema = json.load(fp2)
    definitions = swaggerSchema['definitions']

    baseSchema['definitions'] = definitions
    return deepcopy(baseSchema)

def loadSchemaFor(definitionName):
    schema = loadBaseSchema()
    schema['$ref'] = "#/definitions/%s" % definitionName
    return deepcopy(schema)

def loadReservationResponseSchema():
    schema = loadSchemaFor("ReservationRequest")
    requiredList = schema['definitions']['Contact']['required']
    requiredList.append("status")
    requiredList.append("processedTime")
    return deepcopy(schema)

def loadAntennaAvailabilitySchema():
    schema = loadSchemaFor("AntennaAvailabilityReport")
    return deepcopy(schema)
