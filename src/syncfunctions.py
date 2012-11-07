'''
Created on Sep 6, 2012

@author: lwoydziak
'''
from trackersyncby import TrackerSyncBy
from pivotaltrackeritem import PivotalTrackerItem
from filterfunctions import matchingAJiraTicket, JiraIssue, andDontFilterComments, PivotalIssue, andOmitPivotalTrackerCreatedComments, dateFilterGenerator
from datetime import datetime

filterInOnlyNewIssues = " and status != closed and status != \"In Test\""

def addItemsFrom(jira, toTracker, jiraJql, jiraProject, filterInOnlyNewIssues, ItemType, matchingAnIssue):
    syncByAddingItems = TrackerSyncBy.addingItemsOfType(ItemType, matchingAnIssue)
    for jiraQuery in jiraJql:
        jira.selectProject([jiraProject, jiraQuery + filterInOnlyNewIssues])
        syncByAddingItems(jira, toTracker)
    jira.selectProject([jiraProject, ""])

def syncUpdatedItemsInPivotal(toTracker, pivotal, afterDate, obtainedFromFilter, andFilteringComments, jiraUrl):
    syncChangesFor = TrackerSyncBy.syncingItem(obtainedFromFilter, andFilteringComments)
    for pivotalStory in pivotal.items(afterDate):
        aJiraKey = pivotalStory.jiraKey()
        if aJiraKey is not None:
            pivotalStory.withJiraUrl(jiraUrl + aJiraKey)
            syncChangesFor(pivotalStory, toTracker)            

def syncUpdatedItemsInJira(toTracker, jira, jiraJql, afterDate, obtainedFromFilter, andFilteringComments):
    syncChangesFor = TrackerSyncBy.syncingItem(obtainedFromFilter, andFilteringComments)
    for inJiraQuery in jiraJql:
        for ticket in jira.items(inJiraQuery + afterDate):
            syncChangesFor(ticket, toTracker)
            
def syncPivotalAndJira(jira, pivotal, jiraProjects, jiraBaseProject, jiraIssueLink, skipSyncs):
    filterOutOldTicketsFor = dateFilterGenerator() # datetime(2012, 10, 29)
    jiraProjects = list(jiraProjects)
    if not "addFromJira" in skipSyncs:
        print("Try To Add From Jira:")
        addItemsFrom(jira, pivotal, jiraProjects, jiraBaseProject, filterInOnlyNewIssues + filterOutOldTicketsFor['jira'], PivotalTrackerItem, matchingAJiraTicket)
    if not "fromPivotal" in skipSyncs:
        print("Sync Items From Pivotal:")
        syncUpdatedItemsInPivotal(jira, pivotal, filterOutOldTicketsFor['pivotal'], JiraIssue, andDontFilterComments, jiraIssueLink)
    if not "fromJira" in skipSyncs:
        print("Sync Items From Jira:")
        syncUpdatedItemsInJira(pivotal, jira, jiraProjects, filterOutOldTicketsFor['jira'], PivotalIssue, andOmitPivotalTrackerCreatedComments)