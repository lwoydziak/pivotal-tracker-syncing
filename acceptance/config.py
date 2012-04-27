'''
Created on Apr 18, 2012

@author: lwoydziak
'''
import os
import configparser

class Singleton(type):
    def __init__(cls, name, bases, dictionary):
        super(Singleton, cls).__init__(name, bases, dictionary)
        cls._instance = None

    def __call__(self, *args, **kw):
        if self._instance is None:
            self._instance = super(Singleton, self).__call__(*args, **kw)

        return self._instance
    
## Singleton
class Env(object, metaclass=Singleton):
    def __init__(self):
        self.pivotalTrackerUsername = "None"
        self.pivotalTrackerPassword = "None"
        self.pivotalTrackerUrl = "http://www.pivotaltracker.com"
        self.pivotalTrackerProject = 0
        
        self.jiraUsername = "None"
        self.jiraPassword = "None"
        self.jiraUrl = "http://www.jira.com"
        self.jiraProject = "TEST"
        self.jiraJql = ""
 
        if 'PIVOTAL_ACCEPTANCE_USE_CFG' in os.environ:            
            if os.environ['PIVOTAL_ACCEPTANCE_USE_CFG'] == '1':
                self.load()
            else:
                self.load_config_from_env()
        else:
            self.load()

    def load_config_from_env(self):
        self.pivotalTrackerUsername = os.environ['PIVOTAL_TRACKER_USERNAME'] if 'PIVOTAL_TRACKER_USERNAME' in os.environ else "None"
        self.pivotalTrackerPassword = os.environ['PIVOTAL_TRACKER_PASSWORD'] if 'PIVOTAL_TRACKER_PASSWORD' in os.environ else "None"
        self.pivotalTrackerUrl      = os.environ['PIVOTAL_TRACKER_URL'] if 'PIVOTAL_TRACKER_URL' in os.environ else "None"
        self.pivotalTrackerProject  = int(os.environ['PIVOTAL_TRACKER_PROJECT']) if 'PIVOTAL_TRACKER_PROJECT'     in os.environ else None

        self.jiraUsername = os.environ['JIRA_USERNAME'] if 'JIRA_USERNAME' in os.environ else "None"
        self.jiraPassword = os.environ['JIRA_PASSWORD'] if 'JIRA_PASSWORD' in os.environ else "None"
        self.jiraUrl = os.environ['JIRA_URL'] if 'JIRA_URL' in os.environ else"http://www.jira.com"
        self.jiraProject = os.environ['JIRA_PROJECT'] if 'JIRA_PROJECT' in os.environ else "TEST"
        self.jiraJql = os.environ['JIRA_JQL'] if 'JIRA_JQL' in os.environ else ""

    def load(self):        
        filename = ".pivotalacceptance.cfg"
        if "PIVOTAL_ACCEPTANCE_CONFIG_FILE" in os.environ:
            filename = os.environ.get("PIVOTAL_ACCEPTANCE_CONFIG_FILE")

        config = configparser.ConfigParser()
        config.read(filename)
        
        self.pivotalTrackerUsername = config.get("settings", "pivotalTrackerUsername")
        self.pivotalTrackerPassword = config.get("settings", "pivotalTrackerPassword")
        self.pivotalTrackerUrl = config.get("settings", "pivotalTrackerUrl")
        self.pivotalTrackerProject = config.getint("settings", "pivotalTrackerProject")
        
        self.jiraUsername = config.get("settings", "jiraUsername")
        self.jiraPassword = config.get("settings", "jiraPassword")
        self.jiraUrl = config.get("settings", "jiraUrl")
        self.jiraProject = config.get("settings", "jiraProject")
        self.jiraJql = config.get("settings", "jiraJql")
