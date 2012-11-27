'''
Created on Apr 11, 2012

@author: lwoydziak
'''
class RemoteVersion(object):
    archived = False
    id = None
    name = ""
    releaseDate = None
    released = False
    sequence = 1

class RemoteComponent(object):
    id = None
    name = ""
    
class RemoteCustomFieldValue(object):
    customfieldId = ""
    key = None
    values = ["",]

class RemoteIssue(object):
    affectsVersions = []
    assignee = None
    attachmentNames = []
    components = []
    created = None
    customFieldValues = []
    description = ""
    duedate = None
    environment = None
    fixVersions = []
    id = None
    key = None
    priority = ""
    project = None 
    reporter = None
    resolution = None
    status = ""
    summary = ""
    type = ""
    updated = None
    votes = 0
    
class RemoteStatus(object):
    description = None
    icon = None
    id = 0
    name = None
    
class RemoteComment(object):
    def __init__(self, body="None", id=0, author=None):
        self.id = id
        self.body=body
        self.author=author
    
    
    
    
    
    
     
    