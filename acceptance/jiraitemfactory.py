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
    item.underlying().details_.type = "3"
    testRemoteVersion = {"id" : "11639"}
    testRemoteComponent = {"id" : "12032"}
    item.underlying().details_.affectsVersions = [testRemoteVersion,]
    item.underlying().details_.components = [testRemoteComponent,]
    item.underlying().details_.priority = "3"
    return item