'''
Created on Jun 22, 2012

@author: lwoydziak
'''
from datetime import timedelta, tzinfo

class UTC(tzinfo):
    """UTC"""

    def utcoffset(self, dt):
        return timedelta(0)

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return timedelta(0)