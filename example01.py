#!/usr/bin/python

#a file path will be given with a line and offset which we will:
#create a tab for it if it is not open,
#then switch active tabs to the document and jump to the line+offset.

from gi.repository import GObject, Gtk, Gedit, Gio

class ExamplePlugin03(GObject.Object, Gedit.WindowActivatable):
    __gtype_name__ = "ExamplePlugin03"
    window = GObject.property(type=Gedit.Window)
    #tab = GObject.property(type=Gedit.Tab)
    

    def __init__(self):
        GObject.Object.__init__(self)
        self.flag = 0

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
            #get the active tab, then get the document, then goto line 41 (unless non-existent), 
            #offset 3 (0 if non-existent) (line 41 = 40 the lines start at 0)
            
            #self.window.create_tab(True)  #view_new(Gedit.Document.document_new()) 
            #self.window.get_active_tab().get_document().goto_line_offset(40,3)#.goto_line(9) 
            #self.window.get_active_view().scroll_to_cursor()
            #self.jump_to_declaration("/home/ad/.local/share/gedit/plugins/orig_example01.py",57,19) #in gedit: Ln 57, Col 19
            self.jump_to_declaration("/home/ad/own_bash_scripts/set_up_initial_workspace.sh",94,22) #in gedit: Ln 57, Col 19
            
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
                document.goto_line_offset(line-1,offset-1) #must subtract 1
                ix = True
        if ix == False:
            #create Gio.File from file_path
            location = Gio.file_parse_name(file_path)
            self.window.create_tab_from_location(location, None, line, offset, False, True)
        #scroll to line
        self.window.get_active_view().scroll_to_cursor()
        
        
        
    def input_for_search(self):
        #must check file extension for language
        document = self.window.get_active_tab().get_document()
        document_name = document.get_short_name_for_display()
        extension = document_name.split('.')[-1] #splits string at each '.' into an array and returns last element
        print "document extension : '%s'" % extension
        
  
            
                     
                             
            #print document paths
            #print "document path: %s" % document.get_uri_for_display()
               
