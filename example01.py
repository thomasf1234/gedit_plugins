#!/usr/bin/python

#a file path will be given with a line and offset which we will:
#create a tab for it if it is not open,
#then switch active tabs to the document and jump to the line+offset.
#must implement generic intellisense
#must implement automatic do..end , and module/class/method...end for ruby.

#see:
#https://developer.gnome.org/gedit/3.0/index.html
#https://developer.gnome.org/pygtk/stable/

#use same popup display that word_completion plugin utilises

#I want my thread to:
#1) begin when
#2) need a database of all possible generic routes and definitions at each point in code. changes on the fly
#each route must know what vars affect it for the change.
#3) use regex for situation finder, pass the line through a series of regex and find which column is related to which regex
#i.e   var = Module::Class.method_a.method_b*3
#if we click in the range method_a (i.e. anywhere between the two dots Class.|here|.method_b)
#then we will pass the whole line 'var = Module::Class.method_a.method_b*3' through a series of regex, i.e.
#we will find the following patterns:
# varaiable 'var'
# module 'Module'
#method 'method_b'
#class 'Module::Class'
#method 'Module::Class.method_a'
#look for the pattern that our column number is contained within, i.e. th last one.
#exclude reserved words BY THEMSELVES!, keywords etc
#classes must begin with capital letter.
#methods must begin with ascii end with . ? ! = space (


#dictionary={
#"Resque::Jobs::GenerateXml.perform" => ["/home/ad/rails_root/app/jobs/generate_xml.rb", 23, 5] #jump to def perform 
#"ActiveRecord::Base" = 
#
#input_for_search returns '.method_name', => return all dictionary['.method_name']  


#need plugin to move between spec and document Ctrl+Shift+t

import os, glob, re, shlex
from subprocess import Popen, PIPE
from gi.repository import GObject, Gtk, Gedit, Gio

class ExamplePlugin03(GObject.Object, Gedit.WindowActivatable):
    __gtype_name__ = "ExamplePlugin03"
    window = GObject.property(type=Gedit.Window)
    #tab = GObject.property(type=Gedit.Tab)
    

    def __init__(self):
        GObject.Object.__init__(self)
        
        #used for keyboard shortcut
        self.flag = 0
        
        #used to find input
        self.array_regex = [
        #___'Module::Class.method_a'___
        "([A-Z][a-zA-Z0-9_]*::)*[A-Z][a-zA-Z0-9_]*\.[a-zA-Z][a-zA-Z0-9_]+[?=!]?",  
        #___'.method_a'___
        "\.[a-zA-Z][a-zA-Z0-9_]+[?=!]?"
        ]
        
        #used for building diictionary
        self.array_regex_search = [
        #___module___
        "module [A-Z][a-zA-z0-9]*",
        #___class___
        "class [A-Z][a-zA-z0-9]*",
        #___instance_method___
        "def [a-zA-Z][a-zA-Z0-9_]*[.?=! (]", 
        #___class_method___
        "def self\.[a-zA-Z][a-zA-Z0-9_]*[.?=! (]",
        #___attr_accessor___
        "attr_accessor[ ]+:[a-zA-Z][a-zA-Z0-9_]*"
        ]
        
        self.build_dictionary() #must change to do when file opens from rails app.

    def do_activate(self):
        print "Activating plugin..."
        handlers = []
        
        #self.window.connect(<message>, method)   #method can be defined on this class              
        handler_id = self.window.connect('key-press-event', self.on_key_press_event)
        print "Connected handler %s" % handler_id
        handlers.append(handler_id)
        handler_id = self.window.connect('key-release-event', self.on_key_release_event)
        print "Connected handler %s" % handler_id
        handlers.append(handler_id)
        
        self.window.set_data("ExamplePlugin03Handlers", handlers)

    def do_deactivate(self):
        print "Deactivating plugin..."
        handlers = self.window.get_data("ExamplePlugin03Handlers")
        for handler_id in handlers:
            self.window.disconnect(handler_id)
            print "Disconnected handler %s" % handler_id

    def do_update_state(self):
        pass
         
    def on_key_press_event(self, window, event):
        #print "key pressed : %s" % event.keyval #works
        if event.keyval == 65507: #if 'Ctrl' key is pressed down
            self.flag = 1
            #print "key pressed : %s" % dir(event)
        
    def on_key_release_event(self, window, event):
        #print "key released : %s" % event.keyval #works
        #print self.flag
        #if 'b' key is released while 'Ctrl' is held down
        if event.keyval == 98 and self.flag == 1: 
            print "Ctrl+b has been pressed"
            self.flag = 0

            input_string = self.input_for_search()
            print "input string is : '%s'" % input_string
            declaration_details = self.declaration_search(input_string).split(':')
            self.jump_to_declaration(declaration_details[0],int(declaration_details[1]),int(declaration_details[2]))
            #self.jump_to_declaration(declaration_details.path, declaration_details.line, declaration_details.column)
            #self.jump_to_declaration("/home/ad/.local/share/gedit/plugins/orig_example01.py",57,17) #in gedit: Ln 57, Col 19
            
            #self.jump_to_declaration("/home/ad/own_bash_scripts/set_up_initial_workspace.sh",94,22) #in gedit: Ln 57, Col 19
            
        #if 'Ctrl' key is released
        elif event.keyval == 65507:
            self.flag = 0
            
            
    #pass in file_path, line, offset (line, offset are bottom right values as seen in gedit Ln X, Col Y)
    #i.e. self.jump_to_declaration("/home/ad/own_bash_scripts/set_up_initial_workspace.sh",94,22)
    def jump_to_declaration(self, file_path, line, offset):
        #check if document is open
        documents = self.window.get_documents()
        ix = False;
        for document in documents:
            if document.get_uri_for_display() == file_path:
                #print document.get_location().get_parse_name()
                tab = Gedit.Tab.get_from_document(document)
                self.window.set_active_tab(tab)
                #iter = document.get_iter_at_mark(document.get_insert())
                #print "line: %s" % iter.get_line()
                #print "line: %s" % iter.get_line_offset()
                document.goto_line_offset(line-1,offset-1) #must subtract 1
                ix = True
        if ix == False:
            #create Gio.File from file_path to be passed in next method
            location = Gio.file_parse_name(file_path)
            self.window.create_tab_from_location(location, None, line, offset, False, True)
        #scroll to line
        self.window.get_active_view().scroll_to_cursor()
        
        
        
    #returns the input_string used for the search through the library of declaration locations    
    def input_for_search(self): #need to optimise, pass in  more than self
        #must check file extension for language
        document = self.window.get_active_tab().get_document()
        document_name = document.get_short_name_for_display()
        extension = document_name.split('.')[-1] #splits string at each '.' into an array and returns last element
        print "document extension : '%s'" % extension
        
        if extension == "rb": #must change to "rb"
            cursor_mark = document.get_insert()
            
            iter_start_line = document.get_iter_at_mark(cursor_mark)
            
            line_offset = iter_start_line.get_line_offset()#+1
            print "line offset: %s" % line_offset
            
            iter_start_line.set_line_offset(0)
            print "start_line %s" % iter_start_line.get_line_offset()
            
            iter_end_line = document.get_iter_at_mark(cursor_mark) #see https://developer.gnome.org/pygtk/stable/class-gtktextiter.html
           # print "line: %s" % iter_end_line.get_line()#+1
            iter_end_line.forward_to_line_end()
            print "end_line %s" % iter_end_line.get_line_offset()
            line_string = document.get_text(iter_start_line, iter_end_line, False)
            print "line_string: %s" % line_string
            return self.find_all_regex_matches(line_string, line_offset)

    #iterate through all regex and execute find_span                 
    def find_all_regex_matches(self, line_string, column): 
        for element in self.array_regex:
            word = self.find_span(element, line_string, column)
            if word:
                return word
                
                   
    #returns True if input pattern was matched in the string and the substring found contains the column passed.
    def find_span(self, regex, string, column):
        for m in re.finditer(regex, string):
            print '%02d-%02d: %s %s' % (m.start(), m.end(), m.group(0), regex) 
            if self.in_range(m.start(), m.end(), column) == True: #if we know what we are looking for, then ...
                return m.group(0)                
                       
     
    #scandirs('/home/ad/workspace/order_service')  prints all file names recursively.   
    def scandirs(self, path):
        for currentFile in glob.glob( os.path.join(path, '*') ):
            if os.path.isdir(currentFile):
                print 'got a directory: ' + currentFile
                scandirs(currentFile)
                print "processing file: " + currentFile
                
    #returns True if current is in range (start, end) excluding boundaries                
    def in_range(self, start, end, current):
        if current > start and current < (end+1):
            return True
        else:
            return False
    
    #build arrays representing locations of declarations
    #TODO: run in another thread  
    def build_dictionary(self):  
        cmd = "egrep -inor 'def [a-zA-Z][a-zA-Z0-9_]*[.?=! (]?' /home/ad/workspace/orders_service"
        (stdout, stderr) = Popen(shlex.split(cmd), stdout=PIPE).communicate() #creates string from egrep output
        self.instance_methods_locations = stdout.split('\n')
    
    #search the library for the correct item and return its location
    def declaration_search(self, input_string):
        for i in self.instance_methods_locations:
            #print '___%s_______%s___' % (input_string[1:], i.split(':')[-1])
            for m in re.finditer(input_string[1:], i.split(':')[-1]): #careful because of the dot 
                print 'matched: %s, input_string: %s, file_path: %s, line: %s' % (m.group(0), input_string, i.split(':')[0], i.split(':')[1])
                return '%s:%s:%s' % (i.split(':')[0], i.split(':')[1], 0)  
                
                
                         
