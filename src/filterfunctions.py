'''
Created on Aug 29, 2012

@author: lwoydziak
'''
from datetime import date

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

def dateFilterGenerator(date = date.today()):
    afterDateFor = {'jira':" and updatedDate > \""+ date.strftime('%Y/%m/%d') + " 00:00\"",
                    'pivotal':"modified_since:"+ date.strftime('%m/%d/%Y') + " includedone:true"}
    return afterDateFor        