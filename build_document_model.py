#!/usr/bin/python

import fword

class BuildDocumentModel:

    def __init__(self, document):
        GObject.Object.__init__(self)
        
def load_file(file_path):
    with open (file_path, "r") as myfile: #automatically closes after block
        data=myfile.read()
        print data
        

         



#if is_it_a_keyword returns:
#require
#require_relative
#load 
#extend
#include 
#etc 

#creates the singleton and returns it always        
class AlternateFileLoader(object):
    #flag fr singleton creation
    singleton = None
    def __init__(self, document):
        pass  
          
    #only return the same instance 
    def __new__(cls, *p):
        if cls.singleton == None:
            cls.singleton = object.__new__(cls, *p)
        return cls.singleton #perhaps an exception should be raised.
    
    def callMethod(self, name, *params):
        getattr(self, "_"+self.__class__.__name__+"__"+name)(params) #can hard code name in refactor
    
    def __require(self, file_path): #must replace the line with the file, with correct deepness.
        #self.load_file(file_path)
        
    def load_file(self, file_path):
        with open (file_path, "r") as myfile:
            data=myfile.read()
            return data
            
     def convert_rel_to_abs_path(rel_file_path, document_path): #document.get_uri_for_display() == file_path
             
    
def __require_relative(rel_file_path):

def __load(file_path):

def __include(file_path):



f = Foo()
callMethod(f, "bar1", "arg1", "arg2")


