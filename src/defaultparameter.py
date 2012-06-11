'''
Created on May 22, 2012

@author: lwoydziak
'''

def defaultParameter(typeName, parameter):
    if parameter is None:
        return typeName()
    return parameter
