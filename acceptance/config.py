'''
Created on Apr 18, 2012

@author: lwoydziak
'''
import os
import configparser
import sys
import csv
sys.path.insert(0, "src")
from singletonbase import Singleton
    
## Singleton
class Env(object, metaclass=Singleton):
    def __init__(self):
        self.pivotalTrackerLogin = "None"
        self.pivotalTrackerPassword = "None"
        self.pivotalTrackerUrl = "http://www.pivotaltracker.com"
        self.pivotalTrackerProject = 0
        self.pivotalTrackerUsername = "None"
        self.pivotalTrackerOtherUser = "None"
        
        self.jiraUsername = "None"
        self.jiraPassword = "None"
        self.jiraUrl = "http://www.jira.com"
        self.jiraProject = "TEST"
        self.jiraTimeToUtcHours = 0
        self.jiraJql_ = []
        self.jiraJqlReader_ = []
        self.jiraOtherUser = "None"
 
        if 'PIVOTAL_ACCEPTANCE_USE_CFG' in os.environ:            
            if os.environ['PIVOTAL_ACCEPTANCE_USE_CFG'] == '1':
                self.load()
            else:
                self.load_config_from_env()
        else:
            self.load()

    def load_config_from_env(self):
        self.pivotalTrackerLogin = os.environ['PIVOTAL_TRACKER_LOGIN'] if 'PIVOTAL_TRACKER_LOGIN' in os.environ else "None"
        self.pivotalTrackerPassword = os.environ['PIVOTAL_TRACKER_PASSWORD'] if 'PIVOTAL_TRACKER_PASSWORD' in os.environ else "None"
        self.pivotalTrackerUrl      = os.environ['PIVOTAL_TRACKER_URL'] if 'PIVOTAL_TRACKER_URL' in os.environ else "None"
        self.pivotalTrackerProject  = int(os.environ['PIVOTAL_TRACKER_PROJECT']) if 'PIVOTAL_TRACKER_PROJECT'     in os.environ else None
        self.pivotalTrackerUsername = os.environ['PIVOTAL_TRACKER_USERNAME'] if 'PIVOTAL_TRACKER_USERNAME' in os.environ else "None"
        self.pivotalTrackerOtherUser = os.environ['PIVOTAL_TRACKER_OTHER_USER'] if 'PIVOTAL_TRACKER_OTHER_USER' in os.environ else "None"

        self.jiraUsername = os.environ['JIRA_USERNAME'] if 'JIRA_USERNAME' in os.environ else "None"
        self.jiraPassword = os.environ['JIRA_PASSWORD'] if 'JIRA_PASSWORD' in os.environ else "None"
        self.jiraUrl = os.environ['JIRA_URL'] if 'JIRA_URL' in os.environ else"http://www.jira.com"
        self.jiraProject = os.environ['JIRA_PROJECT'] if 'JIRA_PROJECT' in os.environ else "TEST"
        self.jiraTimeToUtcHours = int(os.environ['JIRA_TIME_TO_UTC_HOURS'] if 'JIRA_TIME_TO_UTC_HOURS' in os.environ else 0)
        self.jiraJqlReader_ = csv.reader(os.environ['JIRA_JQL'], quotechar='\'', delimiter=',') if 'JIRA_JQL' in os.environ else []
        self.jiraOtherUser = os.environ['JIRA_OTHER_USER'] if 'JIRA_OTHER_USER' in os.environ else "None"

    def load(self):        
        filename = ".pivotalacceptance.cfg"
        if "PIVOTAL_ACCEPTANCE_CONFIG_FILE" in os.environ:
            filename = os.environ.get("PIVOTAL_ACCEPTANCE_CONFIG_FILE")

        config = configparser.ConfigParser()
        config.read(filename)
        
        self.pivotalTrackerLogin = config.get("settings", "pivotalTrackerLogin")
        self.pivotalTrackerPassword = config.get("settings", "pivotalTrackerPassword")
        self.pivotalTrackerUrl = config.get("settings", "pivotalTrackerUrl")
        self.pivotalTrackerProject = config.getint("settings", "pivotalTrackerProject")
        self.pivotalTrackerUsername = config.get("settings", "pivotalTrackerUsername")
        self.pivotalTrackerOtherUser = config.get("settings", "pivotalTrackerOtherUser")
        
        self.jiraUsername = config.get("settings", "jiraUsername")
        self.jiraPassword = config.get("settings", "jiraPassword")
        self.jiraUrl = config.get("settings", "jiraUrl")
        self.jiraProject = config.get("settings", "jiraProject")
        self.jiraTimeToUtcHours = config.getint("settings", "jiraTimeToUtcHours")
        self.jiraJqlReader_ = csv.reader(config.get("settings", "jiraJql"), quotechar='\'', delimiter=',')
        self.jiraOtherUser = config.get("settings", "jiraOtherUser")
        
    def jiraJql(self):
        self._initializeJql()
        for jql in self.jiraJql_:
            yield jql
        
    def _initializeJql(self):
        for jql in self.jiraJqlReader_:
            jqlAsStr = str(jql[0]) 
            if "" == jqlAsStr:
                continue
            jql = jqlAsStr.strip('\'')
            self.jiraJql_.append(jql) 
         
