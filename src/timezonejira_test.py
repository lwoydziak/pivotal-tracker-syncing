'''
Created on Jun 24, 2012

@author: lwoydziak
'''
import unittest
from datetime import datetime, timedelta
from timezonejira import JiraTimezone, timeWrapper
from mockito.mocking import mock
from mockito.matchers import any
from time import struct_time, localtime
from mockito.mockito import when

class JiraTimezoneTest(unittest.TestCase):
    def jiraTimezoneSetupForTimeStamp(self, timeStamp, daylightTimeHappening):
        time = mock()
        when(time).timezone().thenReturn(25200)
        when(time).daylight().thenReturn(daylightTimeHappening)
        when(time).altzone().thenReturn(21600)
        when(time).mktime(any()).thenReturn(timeStamp)
        timeAsStructure = localtime(timeStamp)
        when(time).localtime(timeStamp).thenReturn(timeAsStructure)
        return time
        
    def test_withDaylightSavingsTime(self):
        offset = -8
        time = self.jiraTimezoneSetupForTimeStamp(1340728930.0, 1)
        jiraTimezone = JiraTimezone(offset, time)
        dateTime = datetime.now()
        self.assertEqual("JiraTimezone", jiraTimezone.tzname(None))
        self.assertEqual(timedelta(hours=1), jiraTimezone.dst(dateTime))
        self.assertEqual(timedelta(hours=offset+1), jiraTimezone.utcoffset(dateTime))
        
    def test_withOutDaylightSavingsTime(self):
        offset = -9
        time = self.jiraTimezoneSetupForTimeStamp(1353688930.0, 0)
        jiraTimezone = JiraTimezone(offset, time)
        dateTime = datetime.now()
        self.assertEqual(timedelta(hours=0), jiraTimezone.dst(dateTime))
        self.assertEqual(timedelta(hours=offset+0), jiraTimezone.utcoffset(dateTime))
        
    def test_timeWrapper(self):
        timeToBeWrapped = mock()
        testTime = timeWrapper(timeToBeWrapped)
        self.assertEqual(str(testTime.timezone()), str(timeToBeWrapped.timezone))
        self.assertEqual(str(testTime.altzone()), str(timeToBeWrapped.altzone))
        self.assertEqual(str(testTime.daylight()), str(timeToBeWrapped.daylight))
        tracer = "trace"
        when(timeToBeWrapped).mktime(any()).thenReturn(tracer)
        self.assertEqual(testTime.mktime(None), tracer)
        when(timeToBeWrapped).localtime(any()).thenReturn(tracer)
        self.assertEqual(testTime.localtime(None), tracer)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()