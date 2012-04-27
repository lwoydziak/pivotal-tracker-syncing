'''
Created on Mar 27, 2012

@author: lwoydziak
'''
import suds
from tracker import Tracker
from jiratrackeritem import JiraTrackerItem

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
    
    def items(self):
        items = self._getItems()
        for index, item in enumerate(items):
            items[index] = self.updateItemWithComments(item)
        return items
    
    def _getItems(self):
        issues = []
        try:
            issues = self.trackerInstance_.getIssuesFromJqlSearch(self.authentication_, self.project_[JQL], 4000)
        except Exception as e:
            print (e.fault.faultstring)
        return self._issuesToItems(issues)

    
    def finalize(self):
        self.trackerInstance_.logout(self.authentication_)
        self.trackerInstance_ = None
        pass
    
    def update(self, item):
        super(JiraTracker, self).update(item)
        if (item.Id() is None):
            issue = self.trackerInstance_.createIssue(self.authentication_, item.asRemoteItem())
        else:
            issue = self.trackerInstance_.updateIssue(self.authentication_, item.Id(), item.piecesToUpdate())
        updatedItem = JiraTrackerItem(issue).withNewComments(item.newComments())
        self.updateCommentsFor(updatedItem)
    
    def _deleteById(self, itemId):
        self.trackerInstance_.deleteIssue(self.authentication_, itemId)
        pass
    
    def _issuesToItems(self, issues):
        return self._convertToItems(JiraTrackerItem, issues)
    
    def updateItemWithComments(self, item):
        comments = self.trackerInstance_.getComments(self.authentication_, item.Id())
        for comment in comments:
            item.addComment(comment)
        return item

    def updateCommentsFor(self, item):
        for comment in item.newComments():
            self.trackerInstance_.addComment(self.authentication_, item.Id(), {"body":comment})
    
    
    
    
