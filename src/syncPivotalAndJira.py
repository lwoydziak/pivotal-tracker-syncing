#! /usr/bin/env python
import sys
#from trackersyncby import ReverseSync
from syncfunctions import syncPivotalAndJira
from mappivotaltojirastatus import PivotalToJiraStatusMap
from mapusers import PivotalToJiraUserMap
from pivotaltracker import PivotalTrackerFor
from jiratracker import JiraTracker
from timezonejira import JiraTimezone
from config import Env

__version__ = '0.1.0'
__all__ = ['', 'main']

def mapWorkflow():
    jiraToPivotalStatuses = Env().get("jiraToPivotalStatuses") 
    for jira in jiraToPivotalStatuses.keys():
        if jira is not "transitions":
            PivotalToJiraStatusMap().addMapping(jira, jiraToPivotalStatuses[jira])
    try: 
        transitions = jiraToPivotalStatuses["transitions"]
        for transition in transitions.keys():
            PivotalToJiraStatusMap().addMapping(transition, transitionFrom=transitions[transition])
    except KeyError:
        return
    
def mapUsers():
    jiraToPivotalUsers = Env().get("jiraToPivotalUsers") 
    for jira in jiraToPivotalUsers.keys():
        PivotalToJiraUserMap().addMapping(jira, jiraToPivotalUsers[jira])
        
def getTrackers():
    project = Env().get("pivotal", "project")
    pivotalTracker = PivotalTrackerFor(project)
    pivotalTracker.loginAs(Env().get("pivotal", "login")).withCredential(Env().get("pivotal", "password"))
    jira = JiraTracker(Env().get("jira", "url"))
    jira.setTimezone(JiraTimezone(Env().get("jira", "timeToUtcHours")))
    jira.loginAs(Env().get("jira","username")).withCredential(Env().get("jira","password"))
    PivotalToJiraStatusMap().insert(jira.getAvailableStatuses())
    return jira, pivotalTracker

def jiraDetails():
    return Env().get("jira","jql"), Env().get("jira","project"), Env().get("jira","issueLink")

def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    
    mapWorkflow()
    mapUsers()
    jira, pivotal = getTrackers()
    jiraProjects, jiraBaseProject, jiraIssueLink = jiraDetails()
    
    syncPivotalAndJira(jira, pivotal, jiraProjects, jiraBaseProject, jiraIssueLink, Env().get("skipSyncs"))
            
#    print ("Reverse sync Pivotal Items:")
#    
#    reverseSyncFor = TrackerSyncBy.syncingItem(JiraIssue, andOmitPivotalTrackerCreatedComments, Direction=ReverseSync)
#    
#    for pivotalStory in pivotal.items("state:started,finished,delivered,accepted includedone:true"):
#        aJiraKey = pivotalStory.jiraKey()
#        if aJiraKey is not None:
#            pivotalStory.withJiraUrl("https://jira.int.fusionio.com/browse/"+aJiraKey)
#            reverseSyncFor(pivotalStory, toTracker=jira, fromTracker=pivotal)
    
    print ("DONE!")
    return 0

if __name__ == '__main__':
    if sys.argv[0] is None:
        # fix for weird behaviour when run with python -m
        # from a zipped egg.
        sys.argv[0] = 'connector.py'
    sys.exit(main())
