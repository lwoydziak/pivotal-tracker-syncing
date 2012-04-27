'''
Created on Mar 29, 2012

@author: lwoydziak
'''
import unittest
from tracker import Tracker
from mockito.mocking import mock
from mockito.mockito import verify


class Test(unittest.TestCase):
    def test_canSetLoginUsername(self):
        user = "lukewoydziak"
        tracker = Tracker()
        tracker.loginAs(user)
        self.assertEqual(tracker.user(), user)
        pass

    def test_canSetPassword(self):
        tracker = Tracker()
        password = "pass"
        tracker.withCredential(password)
        self.assertEqual(tracker.password(), password)
        
    def test_canGetProject(self):
        tracker = Tracker()
        myProject = 12345
        tracker.selectProject(myProject)
        self.assertEqual(tracker.project(), myProject)
        
    def test_trackerNotValidAtConstruction(self):
        tracker = Tracker()
        self.assertFalse(tracker.valid())
    
    def test_canSetApiObject(self):
        tracker = Tracker()
        apiObject = mock()
        tracker.apiObject(apiObject)
        self.assertEqual(tracker.apiObject_, apiObject)
        
    def test_itemsReturnsNone(self):
        tracker = Tracker()
        items = tracker.items()
        self.assertEqual(len(items), 0)
    
    def test_cantUpdateIfNotValid(self):
        tracker = Tracker()
        item = mock()
        self.assertRaises(ValueError, tracker.update, (item))
        
    def test_cantDeleteIfNotValid(self):
        tracker = Tracker()
        item = mock()
        self.assertRaises(ValueError, tracker.delete, (item))
        
    def test_canDeleteIfValid(self):
        tracker = Tracker()
        tracker.trackerInstance_ = mock()
        item = mock()
        tracker.delete(item)
        verify(item).Id()        
        
    def test_canDeleteAllItems(self):
        tracker = Tracker()
        tracker.deleteAllItems()
        self.assertEqual(len(tracker.items()), 0)
    
    def test_canConvertItemToType(self):
        tracker = Tracker()
        contents = mock()
        item = tracker._convertToItem(testType, contents)
        self.assertEqual(item.contains(), contents)
        
    def test_canConvertToItemsOfType(self):
        tracker = Tracker()
        contents1 = mock()
        contents2 = mock()        
        items = tracker._convertToItems(testType, [contents1, contents2])
        self.assertEqual(items[1].contains(), contents2)

class testType(object):
    def __init__(self, item):
        self.item = item
    
    def contains(self):
        return self.item
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()