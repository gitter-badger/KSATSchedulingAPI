from copy import deepcopy


reservationRequestTemplate = {
    "availabilityReportDate": "2014-10-11T07:28:20.000Z",
    "contactPlan":{
        "satellites":[
            {"name": "SkySat-1",
             "tles": [
                 {"epochDate": "2014-10-10T07:28:20.000Z",
                  "line1": "1 39418U 13066C   15041.51375279  .00003665  00000-0  32287-3 0  9996",
                  "line2": "2 39418  97.7667 121.6977 0020866 279.7964  80.0908 14.96927045 66686"
                  },
                 {"epochDate": "2014-10-11T07:28:20.000Z",
                  "line1": "1 39418U 13066C   15041.51375279  .00003665  00000-0  32287-3 0  9996",
                  "line2": "2 39418  97.7667 121.6977 0020866 279.7964  80.0908 14.96927045 66686"
                  }
             ]
             },
            {"name": "SkySat-2",
             "tles": [
                 {"epochDate": "2014-10-10T07:28:20.000Z",
                  "line1": "1 39418U 13066C   15041.51375279  .00003665  00000-0  32287-3 0  9996",
                  "line2": "2 39418  97.7667 121.6977 0020866 279.7964  80.0908 14.96927045 66686"
                  },
                 {"epochDate": "2014-10-11T07:28:20.000Z",
                  "line1": "1 39418U 13066C   15041.51375279  .00003665  00000-0  32287-3 0  9996",
                  "line2": "2 39418  97.7667 121.6977 0020866 279.7964  80.0908 14.96927045 66686"
                  }
             ]
             }

        ],
        "antennas": [
            {"id":"FBX-1",
             "contacts": [
                 {
                     "id":"SkySat-A-rev1006-Fairbanks-1",
                     "satelliteName":"SkySat-1",
                     "startTime":"2015-10-16T07:00:00Z",
                     "stopTime":"2015-10-16T07:10:00Z"
                 },
                 {
                     "id":"SkySat-B-rev2209-Fairbanks-1",
                     "satelliteName":"SkySat-2",
                     "startTime":"2015-10-18T09:00:00Z",
                     "stopTime":"2015-10-18T09:10:00Z"
                 }
             ]
             },
            {"id":"FBX-2",
             "contacts": [
                 {
                     "id":"SkySat-A-rev1006-Fairbanks-2",
                     "satelliteName":"SkySat-1",
                     "startTime": "2015-10-17T07:00:00Z",
                     "stopTime": "2015-10-17T07:10:00Z",
                 },
                 {
                     "id":"SkySat-B-rev2209-Fairbanks-2",
                     "satelliteName":"SkySat-2",
                     "startTime": "2015-10-19T09:00:00Z",
                     "stopTime": "2015-10-19T09:10:00Z",
                 }
             ]
             }
        ]
    }
}


reservationRequestTemplateWithConflicts = {
    "availabilityReportDate": "2014-10-11T07:28:20.000Z",
    "contactPlan":{
        "satellites":[
            {"name": "SkySat-1",
             "tles": [
                 {"epochDate": "2014-10-10T07:28:20.000Z",
                  "line1": "1 39418U 13066C   15041.51375279  .00003665  00000-0  32287-3 0  9996",
                  "line2": "2 39418  97.7667 121.6977 0020866 279.7964  80.0908 14.96927045 66686"
                  },
                 {"epochDate": "2014-10-11T07:28:20.000Z",
                  "line1": "1 39418U 13066C   15041.51375279  .00003665  00000-0  32287-3 0  9996",
                  "line2": "2 39418  97.7667 121.6977 0020866 279.7964  80.0908 14.96927045 66686"
                  }
             ]
             },
            {"name": "SkySat-2",
             "tles": [
                 {"epochDate": "2014-10-10T07:28:20.000Z",
                  "line1": "1 39418U 13066C   15041.51375279  .00003665  00000-0  32287-3 0  9996",
                  "line2": "2 39418  97.7667 121.6977 0020866 279.7964  80.0908 14.96927045 66686"
                  },
                 {"epochDate": "2014-10-11T07:28:20.000Z",
                  "line1": "1 39418U 13066C   15041.51375279  .00003665  00000-0  32287-3 0  9996",
                  "line2": "2 39418  97.7667 121.6977 0020866 279.7964  80.0908 14.96927045 66686"
                  }
             ]
             }

        ],
        "antennas": [
            {
                "id":"FBX-1",
                "contacts": [
                    {
                        "id":"SkySat-A-rev1006-Fairbanks-1",
                        "satelliteName":"SkySat-1",
                        "startTime": "2015-10-15T07:00:00Z",
                        "stopTime": "2015-10-15T07:10:00Z"
                    },
                    {
                        "id":"SkySat-B-rev2209-Fairbanks-1",
                        "satelliteName":"SkySat-2",
                        "startTime": "2015-10-16T07:00:00Z",
                        "stopTime": "2015-10-16T07:10:00Z"
                    }
                ]
            },
            {"id":"FBX-2",
             "contacts": [
                 {
                     "id":"SkySat-A-rev1006-Fairbanks-2",
                     "satelliteName":"SkySat-1",
                     "startTime": "2015-10-17T07:00:00Z",
                     "stopTime": "2015-10-17T07:10:00Z",
                 },
                 {
                     "id":"SkySat-B-rev2209-Fairbanks-2",
                     "satelliteName":"SkySat-2",
                     "startTime": "2015-10-20T07:00:00Z",
                     "stopTime": "2015-10-20T07:10:00Z",
                 }
             ]
             }
        ]
    }
}

availabilityList = {
    "generationDate":"2015-10-15T10:10:00Z",
    "antennas":[
        {
            "outOfServiceWindows":[
                {
                    "reason":"PLANNED_MAINTENANCE",
                    "startTime":"2015-10-15T00:00:00Z",
                    "stopTime":"2015-10-15T12:00:00Z"
                },
                {
                    "reason":"PLANNED_MAINTENANCE",
                    "startTime":"2015-10-17T00:00:00Z",
                    "stopTime":"2015-10-17T12:00:00Z"
                }
            ],
            "antennaId":"FBX-1"
        },
        {
            "outOfServiceWindows":[
                {
                    "reason":"PLANNED_MAINTENANCE",
                    "startTime":"2015-10-18T00:00:00Z",
                    "stopTime":"2015-10-18T12:00:00Z"
                },
                {
                    "reason":"PLANNED_MAINTENANCE",
                    "startTime":"2015-10-20T00:00:00Z",
                    "stopTime":"2015-10-20T12:00:00Z"
                }
            ],
            "antennaId":"FBX-2"
        }
    ]
}


def reservationRequest():
    return deepcopy(reservationRequestTemplate)

def reservationRequestWithConflicts():
    return deepcopy(reservationRequestTemplateWithConflicts)

def antennaAvailability():
    return deepcopy(availabilityList)