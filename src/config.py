'''
Created on Apr 18, 2012

@author: lwoydziak
'''
import os
import configparser
import sys
import csv
import json
from singletonbase import Singleton
    
## Singleton
class Env(object, metaclass=Singleton):
    def __init__(self):
        initialJson = '{ \
            "pivotal" : { \
                "login"          : "None", \
                "password"       : "None", \
                "url"            : "http://www.pivotaltracker.com", \
                "project"        : 0, \
                "username"       : "None", \
                "otherUser"      : "None"\
            },\
            "jira" : { \
                "username"       : "None", \
                "password"       : "None", \
                "url"            : "http://www.jira.com", \
                "issueLink"      : "http://www.jira.com/browse", \
                "project"        : "TEST", \
                "timeToUtcHours" : 0, \
                "jql"            : [], \
                "otherUser"       : "None"\
            },\
            "jiraToPivotalUsers" : { \
                "None" : "None"\
            },\
            "jiraToPivotalStatuses" : { \
                "None" : "None" \
            },\
            "skipSyncs" : "addFromJira, fromPivotal, fromJira"\
        }'
        self.json = json.loads(initialJson)
        self.load()
        
    def load(self):        
        filename = ".pivotalacceptance.cfg"
        if "PIVOTAL_ACCEPTANCE_CONFIG_FILE" in os.environ:
            filename = os.environ.get("PIVOTAL_ACCEPTANCE_CONFIG_FILE")
        
        try:
            configFile = open(filename, "r")
        except IOError:
            return
        
        self.json = json.load(configFile)
        
    def get(self, firstLevel, secondLevel=None):
        try:
            if secondLevel is None:
                return self.json[firstLevel]
            else:
                return self.json[firstLevel][secondLevel]
        except KeyError:
            return ""



         
