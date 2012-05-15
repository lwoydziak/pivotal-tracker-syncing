'''
Created on May 15, 2012

@author: lwoydziak
'''
import unittest
from singletonbase import Singleton

class TestSingleton(object, metaclass=Singleton):
    def __init__(self):
        pass

class SingletonTest(unittest.TestCase):
    def test_OnlyOneInstanceIsReturned(self):
        self.assertEqual(TestSingleton(), TestSingleton())


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()