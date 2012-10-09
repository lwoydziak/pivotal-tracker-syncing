'''
Created on Aug 29, 2012

@author: lwoydziak
'''

def matchingAJiraTicket(jiraTicket):
    print (jiraTicket.jiraKey())
    return "\"" + jiraTicket.jiraKey() + "\"" + " includedone:true"

def JiraIssue(item):
    pivotalMirrioredIssue = "issuekey = \"" + str(item.jiraKey()) + "\""
    return pivotalMirrioredIssue
    
def andDontFilterComments(item):
    print (item.jiraKey())
    
def PivotalIssue(jiraTicket):
    pivotalSearch = matchingAJiraTicket(jiraTicket)
    return pivotalSearch

def andOmitPivotalTrackerCreatedComments(item):
    comments = item.comments("new")
#    print (item.jiraKey())
    for comment in comments[:]:
        if "A Pivotal Tracker story" in comment:
            comments.remove(comment)

def dateFilterGenerator():
    afterDateFor = {'jira':" and updatedDate > \"2012/10/08 00:00\"", 'pivotal':"modified_since:10/08/2012 includedone:true"}
    return afterDateFor        