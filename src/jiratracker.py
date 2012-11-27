'''
Created on Mar 27, 2012

@author: lwoydziak
'''
import suds
from tracker import Tracker
from jiratrackeritem import JiraTrackerItem
from urllib.parse import urlparse
from jirastatustoaction import JiraStatusToAction
from trackeritemcomment import JiraComment

NAME = 0
JQL = 1

class JiraTracker(Tracker):
    '''
    classdocs
    '''

    def __init__(self, url=None):
        '''
        Constructor
        '''
        super(JiraTracker, self).__init__()
        self.project_ = ["",""]
        self.setLocationTo(url)
        self.timezone_ = None
        self.apiObject(suds.client)
        
    def __del__(self):
        if (self.trackerInstance_ ):
            self.finalize()
    
    def withCredential(self, password):
        super(JiraTracker, self).withCredential(password)
        serviceGetter = self.apiObject_.Client(self.url_, timeout=10000000)
        self.trackerInstance_ = serviceGetter.service
        self.authentication_ = self.trackerInstance_.login(self.user(),self.password())
        pass
    
    def setLocationTo(self, url):
        self.url_ = url
        pass
    
    def location(self):
        return self.url_
    
    def _makeJqlQuery(self, forFilter=None):
        if forFilter is None:
            return self.project()[JQL]
        if self.project()[JQL] is None or self.project()[JQL] is "":
            return forFilter
        return self.project()[JQL] + " and " + forFilter
    
    def _getItems(self, forFilter=None):
        issues = []
        jqlQuery = self._makeJqlQuery(forFilter)
        try:
            issues = self.trackerInstance_.getIssuesFromJqlSearch(self.authentication_, jqlQuery, 4000)
        except Exception as e:
            print (e.fault.faultstring)
        for issue in issues:
            yield self._convertToItem(JiraTrackerItem, issue, self.timezone_)
    
    def finalize(self):
        self.trackerInstance_.logout(self.authentication_)
        self.trackerInstance_ = None
        pass
    
    def update(self, item):
        super(JiraTracker, self).update(item)
        print("Update Jira Ticket:")
        if (item.Id() is None):
            print(item.asRemoteItem())
            issue = self.trackerInstance_.createIssue(self.authentication_, item.asRemoteItem())
        else:
            print(item.piecesToUpdate())
            issue = self.trackerInstance_.updateIssue(self.authentication_, item.Id(), item.piecesToUpdate())
        updatedItem = JiraTrackerItem(issue)
        if "status" in str(item.piecesToUpdate()):
            updatedItem.withStatus(item.status())
            updatedItem = JiraTrackerItem(self._ticketWithUpdatedStatusFrom(updatedItem))
        print(item.comments('new'))
        updatedItem.withComments(item.comments('new'))
        # to be fully complete updatedItem also needs exisiting comments - tbd
        return self.updateCommentsFor(updatedItem)
    
    def _deleteById(self, itemId):
        self.trackerInstance_.deleteIssue(self.authentication_, itemId)
        pass
        
    def addCommentsTo(self, item):
        comments = self.trackerInstance_.getComments(self.authentication_, item.Id())
        if comments is not None:
            for comment in comments:
                item.addComment(JiraComment(comment), 'existing')
        return item

    def updateCommentsFor(self, item):
        comments = item.comments('new')
        for comment in comments[:]:
            self.trackerInstance_.addComment(self.authentication_, item.Id(), comment.forJira())
            #now comments in the new should be moved to existing - tbd
        return item     
    
    def _setExtraFieldsFor(self, item):
        item = super(JiraTracker, self)._setExtraFieldsFor(item)
        parsedUrl = urlparse(self.location())
        item.withJiraUrl("https://" + str(parsedUrl.netloc) + "/browse/" + str(item.jiraKey()))
        return item
    
    def getAvailableStatuses(self):
        return self.trackerInstance_.getStatuses(self.authentication_)
    
    def _ticketWithUpdatedStatusFrom(self, trackerItem):
        actions = self.getNextStatusActionsFor(trackerItem)
        actionToChangeStatus = JiraStatusToAction(trackerItem.status(), actions).Id()
        if actionToChangeStatus is not None:
            return self.trackerInstance_.progressWorkflowAction(self.authentication_, trackerItem.Id(), actionToChangeStatus, [])
        else:
            return trackerItem.underlying()
    
    def getNextStatusActionsFor(self, trackerItem):
        return self.trackerInstance_.getAvailableActions(self.authentication_, trackerItem.Id())

    
    def setTimezone(self, timezone):
        self.timezone_ = timezone
        
    def timezone(self):
        return self.timezone_
    
    
    
    
    
    
    
    
    
