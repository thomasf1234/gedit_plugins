#!/usr/bin/python

#import gedit

#class HelloWorldPlugin(gedit.Plugin):
#    def __init__(self):
#        print "Plugin loaded"

#    def activate(self, window):
#        print "Plugin activated"

#    def deactivate(self, window):
#        print "Plugin deactivated"

#    def update_ui(self, window):
#        pass


from gi.repository import GObject, Gtk, Gedit

class ExamplePlugin03(GObject.Object, Gedit.WindowActivatable):
    __gtype_name__ = "ExamplePlugin03"
    window = GObject.property(type=Gedit.Window)
    

    def __init__(self):
        GObject.Object.__init__(self)
        self.flag = 0

    def do_activate(self):
        print "Activating plugin..."
        self.window.connect('key-press-event', self.on_key_press_event)
        self.window.connect('key-release-event', self.on_key_release_event)
        handlers = []
        #self.window.connect(<message>, method)   #method can be defined on this class
        handler_id = self.window.connect("tab-added", self.tab_added_ppp)
        
        handlers.append(handler_id)
        print "Connected handler %s" % handler_id

        handler_id = self.window.connect("tab-removed", self.on_tab_removed)
        handlers.append(handler_id)
        print "Connected handler %s" % handler_id

        self.window.set_data("ExamplePlugin03Handlers", handlers)

    def do_deactivate(self):
        print "Deactivating plugin..."
        handlers = self.window.get_data("ExamplePlugin03Handlers")
        for handler_id in handlers:
            self.window.disconnect(handler_id)
            print "Disconnected handler %s" % handler_id

    def do_update_state(self):
        pass

    def tab_added_ppp(self, window, tab, data=None):
        document = tab.get_document()
        print "'%s' has been added." % document.get_short_name_for_display()
        active_view = self.window.get_active_view() 
        active_buffer = active_view.get_buffer() #gets the Document Obj that inherits from Gtk.TextBuffer
        print active_buffer.get_line_count()#__class__.__name__
        #views = self.window.get_views()
        #for view in views:
          #Gedit.View.paste_clipboard(view)
          
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
            self.window.get_active_tab().get_document().goto_line_offset(40,3)#.goto_line(9) 
            self.window.get_active_view().scroll_to_cursor()
            self.window.create_tab(True)  #view_new(Gedit.Document.document_new()) 
        #if 'Ctrl' key is released
        elif event.keyval == 65507:
            self.flag = 0       
        
           
    def on_tab_removed(self, window, tab, data=None):
        document = tab.get_document()
        print "'%s' has been removed." % document.get_short_name_for_display()
