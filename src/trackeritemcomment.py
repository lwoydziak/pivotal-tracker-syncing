'''
Created on Nov 19, 2012

@author: lwoydziak
'''

class TrackerItemComment(object):
    '''
    classdocs
    '''


    def __init__(self, text, author=None, identifier=None):
        '''
        Constructor
        '''
        self.text_ = text
        self.author_ = author
        self.identifier_ = identifier
        
    def text(self):
        return self.text_
    
    def forJira(self):
        return {'body':self.text()}
    
    def forPivotal(self):
        return None
    
    def __len__(self):
        return len(self.text_)
    
    def __eq__(self, other):
        if other is self:
            return True
        if isinstance(other, TrackerItemComment):
            if self.text() == other.text():
                return True
        return False

    def __ne__(self, other):
        return not self.__eq__(other)
    
#    def author(self):
#        return self.author_
#    
#    def identifier(self):
#        return self.identifier_
        
class JiraComment(TrackerItemComment):
    def __init__(self, remoteComment):
        if isinstance(remoteComment, TrackerItemComment):
            remoteCommentDictionary = remoteComment.__dict__
            super(JiraComment, self).__init__(remoteCommentDictionary['text_'], remoteCommentDictionary['author_'], remoteCommentDictionary['identifier_'])
            return
        remoteCommentDictionary = remoteComment.__dict__
        super(JiraComment, self).__init__(remoteCommentDictionary['body'], remoteCommentDictionary['author'], remoteCommentDictionary['id'])
    
class PivotalComment(TrackerItemComment):
    def __init__(self, remoteComment):
        if isinstance(remoteComment, TrackerItemComment):
            remoteCommentDictionary = remoteComment.__dict__
            super(PivotalComment, self).__init__(remoteCommentDictionary['text_'], remoteCommentDictionary['author_'], remoteCommentDictionary['identifier_'])
            return 
        super(PivotalComment, self).__init__(remoteComment.GetText(), remoteComment.GetAuthor(), remoteComment.GetId())