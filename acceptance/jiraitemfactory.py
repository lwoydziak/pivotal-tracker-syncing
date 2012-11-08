'''
Created on Apr 18, 2012

@author: lwoydziak
'''
import sys
sys.path.insert(0, "src")
from jiratrackeritem import JiraTrackerItem

def jiraItemFactory(project, summary, description):
    item = JiraTrackerItem().withSummary(summary).withDescription(description)
    item.underlying().details_.project = project
    item.underlying().details_.type = "2"
    testRemoteVersion = {"id" : "10000"}
    testRemoteComponent = {"id" : "10000"}
    item.underlying().details_.affectsVersions = [testRemoteVersion,]
    item.underlying().details_.components = [testRemoteComponent,]
    item.underlying().details_.priority = "3"
    return item