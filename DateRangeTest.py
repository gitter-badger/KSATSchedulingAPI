
import unittest
from datetime import datetime as dt

from TimeUtils import isDateWithin, doWindowsOverlap, datetimeAsIso8601, iso8601AsDatetime


class DateRangeTest(unittest.TestCase):

    def testDatetimeFromIso8601(self):
        startDate = dt(2015, 10, 13, 13, 10, 0)
        isoString = datetimeAsIso8601(startDate)
        convertedDate = iso8601AsDatetime(isoString)
        self.assertEqual(startDate, convertedDate)

    def testNow(self):
        isoString = datetimeAsIso8601(dt.now())
        print isoString

    def testDateWithin(self):
        date1 = dt(2015, 10, 13, 13, 10, 0)
        date2 = dt(2015, 10, 13, 13, 11, 0)

        self.assertTrue(isDateWithin(dt(2015, 10, 13, 13, 10, 30), date1, date2)) # middle
        self.assertTrue(isDateWithin(date1, date1, date2))                        # endtime
        self.assertTrue(isDateWithin(date2, date1, date2))                        # starttime

        self.assertFalse(isDateWithin(dt(2015, 10, 13, 13, 9, 59), date1, date2)) # before
        self.assertFalse(isDateWithin(dt(2015, 10, 13, 13, 11, 1), date1, date2)) # after

    def testWindowsOverlap(self):

        outageStart = dt(2015, 10, 13, 13, 10, 00)
        outageEnd = dt(2015, 10, 13, 13, 20, 00)

        before = dt(2015, 10, 13, 13, 9, 00)
        withinEarly = dt(2015, 10, 13, 13, 11, 00)
        withinLate = dt(2015, 10, 13, 13, 19, 00)
        after = dt(2015, 10, 13, 13, 30, 00)

        # Contact Start before, End within
        self.assertTrue(doWindowsOverlap(before, withinLate, outageStart, outageEnd ))
        # Contact Start/End within
        self.assertTrue(doWindowsOverlap(withinEarly, withinLate, outageStart, outageEnd ))
        # Contact Start within. End after
        self.assertTrue(doWindowsOverlap(withinEarly, after, outageStart, outageEnd ))
        # Contact Start before, Contact End after
        self.assertTrue(doWindowsOverlap(before, after, outageStart, outageEnd ))

        # Contact Start = Window End
        self.assertTrue(doWindowsOverlap(outageEnd, after, outageStart, outageEnd ))
        # Contact End = Window Start
        self.assertTrue(doWindowsOverlap(before, outageStart, outageStart, outageEnd ))



