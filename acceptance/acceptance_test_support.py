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
    
class SingleJira(object, metaclass=Singleton):
    def __init__(self):
        tracker = JiraTracker(Env().jiraUrl)
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
        
      
        