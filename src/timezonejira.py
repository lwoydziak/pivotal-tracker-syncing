'''
Created on Jun 24, 2012

@author: lwoydziak
'''

from datetime import timedelta, tzinfo
import time

class timeWrapper:
    def __init__(self, time):
        self.time = time
    
    def timezone(self):
        return self.time.timezone
    
    def altzone(self):
        return self.time.altzone
    
    def daylight(self):
        return self.time.daylight
    
    def mktime(self, tt):
        return self.time.mktime(tt)

    def localtime(self, stamp):
        return self.time.localtime(stamp)

class JiraTimezone(tzinfo):
    """JiraTimeZone"""
    def __init__(self, offset, timeIn=None): 
        self.offset = offset
        self.time = timeWrapper(time) if timeIn is None else timeIn
        self.standardOffset = timedelta(seconds = -self.time.timezone())
        if self.time.daylight():
            self.daylightOffset = timedelta(seconds = -self.time.altzone())
        else:
            self.daylightOffset = self.standardOffset
        
        self.daylightAdjustment  = self.daylightOffset - self.standardOffset

    def utcoffset(self, dt):
        return timedelta(hours=self.offset) + self.dst(dt)

    def tzname(self, dt):
        return "JiraTimezone"
    
    def _isdst(self, dt):
        tt = (dt.year, dt.month, dt.day,
              dt.hour, dt.minute, dt.second,
              dt.weekday(), 0, -1)
        stamp = self.time.mktime(tt)
        tt = self.time.localtime(stamp)
        return tt.tm_isdst > 0

    def dst(self, dt):
        if self._isdst(dt):
            return self.daylightAdjustment
        else:
            return timedelta(0)
        