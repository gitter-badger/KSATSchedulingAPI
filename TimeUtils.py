from datetime import datetime as dt

def isDateWithin(dateToCheck, startDate, endDate):
    return (dateToCheck >= startDate) and (dateToCheck <= endDate)

def doWindowsOverlap(contactStart, contactEnd, windowStart, windowEnd):
    if isDateWithin(contactStart, windowStart, windowEnd):
        return True
    if isDateWithin(windowStart, contactStart, contactEnd):
        return True

    return False

# isoformat() alone doesn't make json schema validator happy
def datetimeAsIso8601(dateTime):
    return  dateTime.strftime("%Y-%m-%dT%H:%M:%SZ")


def iso8601AsDatetime(isoString):
    convertedDate = dt.strptime(isoString, "%Y-%m-%dT%H:%M:%SZ")
    return convertedDate