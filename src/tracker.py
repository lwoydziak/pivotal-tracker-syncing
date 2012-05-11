'''
Created on Mar 29, 2012

@author: lwoydziak
'''

class Tracker(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.user_ = "None"
        self.password_ = "None"
        self.project_ = None
        self.trackerInstance_ = None
        self.apiObject_ = None
        self.authentication_ = None
   
    def loginAs(self, user):
        self.user_ = user
        return self     

    def user(self):
        return self.user_
    
    def withCredential(self, password):
        self.password_ = password
    
    def password(self):
        return self.password_
    
    def project(self):
        return self.project_
    
    def selectProject(self, myProject):
        self.project_ = myProject
    
    def valid(self):
        if (not self.trackerInstance_ ):
            return False
        return True
    
    def apiObject(self, apiObject):
        self.apiObject_ = apiObject
 
    def items(self):
        itemsToReturn = self._getItems()
        for index, item in enumerate(itemsToReturn):
            itemsToReturn[index] = self._setExtraFieldsFor(item)
        return itemsToReturn
    
    def _setExtraFieldsFor(self, item):
        return self.updateItemWithComments(item)
    
    def _getItems(self):
        return []

    def update(self, item):
        if not self.valid(): 
            raise ValueError()
    
    def delete(self, item):
        if not self.valid():
            raise ValueError()
        self._deleteById(item.Id())
        
    def deleteAllItems(self):
        items = self.items()
        for item in items:
            self._deleteById(item.Id())

    def _deleteById(self, itemId):
        pass
 
    def _convertToItem(self, typeName, contents):
        return typeName(contents)
      
    def _convertToItems(self, typeName, listOfItemContents):
        for index, contentsForItem in enumerate(listOfItemContents):
            listOfItemContents[index] = self._convertToItem(typeName, contentsForItem)
        return listOfItemContents    
        
    
    
    
    
    
    
    
    
    
    
    
