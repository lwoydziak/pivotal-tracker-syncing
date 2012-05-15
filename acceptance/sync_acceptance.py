'''
Created on Apr 18, 2012

@author: lwoydziak
'''
import unittest
import sys
from config import Env
sys.path.insert(0, "src")
from jiratracker import JiraTracker
from pivotaltracker import PivotalTrackerFor
from jiraitemfactory import jiraItemFactory
from pivotaltrackeritem import PivotalTrackerItem
from unit_test_support import Testing



class SyncAcceptanceTest(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        jira = JiraTracker(Env().jiraUrl)
        jira.loginAs(Env().jiraUsername).withCredential(Env().jiraPassword)
        jira.selectProject([Env().jiraProject, Env().jiraJql])
        self.jira_ = jira
        pivotal = PivotalTrackerFor(Env().pivotalTrackerProject)
        pivotal.loginAs(Env().pivotalTrackerUsername).withCredential(Env().pivotalTrackerPassword)
        self.pivotal_ = pivotal
        pass


    def tearDown(self):
        self.jira_.deleteAllItems()
        self.jira_.finalize()
        self.pivotal_.deleteAllItems()
        unittest.TestCase.tearDown(self)

    def syncNewItemToPivotal(self, newJiraItem, jira, pivotal):
        jira.update(newJiraItem)
        jiraItem = next(jira.items())
        pivotalItem = PivotalTrackerItem()
        pivotalItem.syncWith(jiraItem)
        pivotal.update(pivotalItem)
    
    def test_newissueinjiraiscopiedtopivotal(self):
        jira = self.jira_
        pivotal = self.pivotal_
        summary = "test_newissueinjiraiscopiedtopivotal"
        newjiraitem = jiraitemfactory(env().jiraproject, summary, "a test description")
        self.syncnewitemtopivotal(newjiraitem, jira, pivotal)
        pivotalitem = next(pivotal.items())
        self.assertequal(pivotalitem.summary(), summary)
    
    def syncexistingitemfromjiratopivotal(self, newjiraitem, jira, pivotal):
        jira.update(newjiraitem)
        jiraitem = next(jira.items())
        pivotalitem = next(pivotal.items())
        pivotalitem.syncwith(jiraitem)
        pivotal.update(pivotalitem)
    
    def test_existingissueinjiraissyncedwithexistingissueinpivotal(self):
        jira = self.jira_
        pivotal = self.pivotal_
        newpivotalitem = pivotaltrackeritem().withsummary("to be overwritten").withdescription("a test description to be overwritten")
        pivotal.update(newpivotalitem)
        desiredsummary = "test_existingissueinjiraissyncedwithexistingissueinpivotal"
        desireddescription = "overwritten!"
        newjiraitem = jiraitemfactory(env().jiraproject, desiredsummary, desireddescription )
        self.syncexistingitemfromjiratopivotal(newjiraitem, jira, pivotal)
        updatedpivotalitem = next(pivotal.items())
        self.assertequal(updatedpivotalitem.summary(), desiredsummary)
        self.assertequal(updatedpivotalitem.description(), desireddescription)
        pass
    
    def test_commentonissueinjiraissyncedtopivotal(self):
        jira = self.jira_
        pivotal = self.pivotal_
        newpivotalitem = pivotaltrackeritem().withsummary("to test comments").withdescription("description")
        pivotal.update(newpivotalitem)
        newjiraitem = jiraitemfactory(env().jiraproject, "to test comments", "blah")
        commentonjira = "this commentonjira can be synced"
        newjiraitem.addcomment(commentonjira)
        self.syncexistingitemfromjiratopivotal(newjiraitem, jira, pivotal)
        updatedpivotalitem = next(pivotal.items())
        self.assertequal(updatedpivotalitem.comments()[0], commentonjira)
        pass
    
    def test_commentonissueinpivotalissyncedtojira(self):
        jira = self.jira_
        pivotal = self.pivotal_
        newpivotalitem = pivotaltrackeritem().withsummary("to test comments").withdescription("description")
        newjiraitem = jiraitemfactory(env().jiraproject, "to test comments", "blah")
        commentonpivotal = "this commentonpivotal can be synced"
        newpivotalitem.addcomment(commentonpivotal)
        pivotal.update(newpivotalitem)
        jira.update(newjiraitem)
        jiraitem = next(jira.items())
        pivotalitem = next(pivotal.items())
        jiraitem.syncwith(pivotalitem)
        jira.update(jiraitem)
        updatedjiraitem = next(jira.items())
        self.assertequal(updatedjiraitem.comments()[0], commentonpivotal)
        pass
    
    def test_issueinjiraandinpivotalaresyncable(self):
        jira = self.jira_
        pivotal = self.pivotal_
        newjiraitem = jiraitemfactory(env().jiraproject, "test_issueinjiraandinpivotalareequal", "a test description")
        newpivotalitem = pivotaltrackeritem().withsummary("test_issueinjiraandinpivotalareequal-2").withdescription("description")
        pivotal.update(newpivotalitem)
        self.syncexistingitemfromjiratopivotal(newjiraitem, jira, pivotal)
        jiraitem = next(jira.items())
        pivotalitem = next(pivotal.items())
        self.asserttrue(pivotalitem.canbesyncedwith(jiraitem))
        pass

    
    def test_20000PlusCharacterCommentsAreNotSyned(self):
        jira = self.jira_
        pivotal = self.pivotal_
        newJiraItem = jiraItemFactory(Env().jiraProject, "test_20000PlusCharacterCommentsAreNotSyned", "blah")
        commentOnJira = Testing.stringOfAsOfSize(20002)
        newJiraItem.addComment(commentOnJira)
        self.syncNewItemToPivotal(newJiraItem, jira, pivotal)
        pivotalItem = next(pivotal.items())
        self.assertEqual(len(pivotalItem.comments()), 0)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()