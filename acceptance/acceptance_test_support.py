'''
Created on May 3, 2012

@author: lwoydziak
'''
from config import Env
import sys
sys.path.insert(0, "src")
from singletonbase import Singleton
from jiratracker import JiraTracker
from pivotaltracker import PivotalTrackerFor
from trackeritemstatus import TrackerItemStatus
from mappivotaltojirastatus import PivotalToJiraStatusMap
from timezonejira import JiraTimezone

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
        aComment = "I am adding this comment"
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
        statuses = tracker.getAvailableStatuses()
        PivotalToJiraStatusMap().addMapping(jira="Closed", pivotal="accepted")
        PivotalToJiraStatusMap().addMapping(jira="New", pivotal="unscheduled")
        PivotalToJiraStatusMap().addMapping(jira="In Work", pivotal="started")
        PivotalToJiraStatusMap().addMapping(jira="In Work", transitionFrom="Assigned")
        PivotalToJiraStatusMap().insert(statuses)
    
class SingleJira(object, metaclass=Singleton):
    def __init__(self):
        tracker = JiraTracker(Env().jiraUrl)
        tracker.setTimezone(JiraTimezone(Env().jiraTimeToUtcHours))
        tracker.loginAs(Env().jiraUsername).withCredential(Env().jiraPassword)
        tracker.selectProject([Env().jiraProject, next(Env().jiraJql())])
        self.tracker_ = tracker
        
    def instance(self):
        return self.tracker_
    
class SinglePivotal(object, metaclass=Singleton):
    def __init__(self):
        tracker = PivotalTrackerFor(Env().pivotalTrackerProject)
        tracker.loginAs(Env().pivotalTrackerUsername).withCredential(Env().pivotalTrackerPassword)
        self.tracker_ = tracker
        
    def instance(self):
        return self.tracker_
        
      
        