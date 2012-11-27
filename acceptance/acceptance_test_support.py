'''
Created on May 3, 2012

@author: lwoydziak
'''
import sys
sys.path.insert(0, "src")
from config import Env
from singletonbase import Singleton
from jiratracker import JiraTracker
from pivotaltracker import PivotalTrackerFor
from trackeritemstatus import TrackerItemStatus
from mappivotaltojirastatus import PivotalToJiraStatusMap
from mapusers import PivotalToJiraUserMap
from timezonejira import JiraTimezone
from trackeritemcomment import TrackerItemComment

class Testing(object):

    @staticmethod
    def canUpdateItemsIn(tracker, test):
        item = next(tracker.items())
        newSummary = "updated summary"
        newDescription = "yep - updated"
        item.withSummary(newSummary).withDescription(newDescription)
        tracker.update(item)
        item = next(tracker.items())
        test.assertEqual(item.summary(), newSummary)
        test.assertEqual(item.description(), newDescription)
        
    @staticmethod
    def addCommentToItemIn(tracker):
        item = next(tracker.items())
        aComment = TrackerItemComment("I am adding this comment")
        item.addComment(aComment)
        tracker.update(item)
        return aComment
    
    @staticmethod
    def putItemToTrackerAndChangeStatusTo(status, item, tracker):
        tracker.update(item)
        item = next(tracker.items())
        status = TrackerItemStatus(status)
        item.withStatus(status)
        tracker.update(item)
        return status
    
    @staticmethod
    def mapStatuses(tracker):
        jiraToPivotalStatuses = Env().get("jiraToPivotalStatuses") 
        for jira in jiraToPivotalStatuses.keys():
            if jira is not "transitions":
                PivotalToJiraStatusMap().addMapping(jira, jiraToPivotalStatuses[jira])
        try: 
            transitions = jiraToPivotalStatuses["transitions"]
            for transition in transitions.keys():
                PivotalToJiraStatusMap().addMapping(transition, transitionFrom=transitions[transition])
        except KeyError:
            pass 
        PivotalToJiraStatusMap().insert(tracker.getAvailableStatuses())
        
    @staticmethod
    def mapUsers():
        jiraToPivotalUsers = Env().get("jiraToPivotalUsers") 
        for jira in jiraToPivotalUsers.keys():
            PivotalToJiraUserMap().addMapping(jira, jiraToPivotalUsers[jira])
    
class SingleJira(object, metaclass=Singleton):
    def __init__(self):
        tracker = JiraTracker(Env().get("jira", "url"))
        tracker.setTimezone(JiraTimezone(Env().get("jira", "timeToUtcHours")))
        tracker.loginAs(Env().get("jira","username")).withCredential(Env().get("jira","password"))
        tracker.selectProject([Env().get("jira","project"), Env().get("jira","jql")[0]])
        self.tracker_ = tracker
        
    def instance(self):
        return self.tracker_
    
class SinglePivotal(object, metaclass=Singleton):
    def __init__(self):
        tracker = PivotalTrackerFor(Env().get("pivotal", "project"))
        tracker.loginAs(Env().get("pivotal", "login")).withCredential(Env().get("pivotal", "password"))
        self.tracker_ = tracker
        
    def instance(self):
        return self.tracker_
        
      
        