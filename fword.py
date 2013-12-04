'''
this should be a class where each open document has an instance of.
the instance contains all the ruby information that can be retrieved from the document.
this info will be ordered and accessible via the navigation plugin, possibly intellisense etc 
and word completion.

need a hash of letter starts to keywords
need methods for what to do at each keyword

require/require_relative => replace this line with file (only allow if file isn't already loaded)
include => adding methods to an instance of a class 
extend => adding class methods to a class
load => loads file into memory with every call to load, even if already in memory
http://stackoverflow.com/questions/3170638/how-does-load-differ-from-require-in-ruby
http://www.railstips.org/blog/archives/2009/05/15/include-vs-extend-in-ruby/
'''

#start a the beginning of the string, iterate through and check for a space
#if we find a space return the offset from the start

#"    class   KING   "  would stop at 'c' and return the location relative to start
def find_start_of_a_word(str, str_length, i=0):
    while i < str_length:
        if str[i] != ' ':
            return i
        i+=1
 
#would check the word at location 'start' in the string i.e. for above, would identify class as a keyword 
def q_is_it_a_keyword(str, start):
    if str[start] == 'c':
        if str[start:start+6] == 'class ': 
            return (str[start:start+6], start+6, start) #the next possible char #class_name = get_word(i+6, line_len)
    elif str[start] == 'd':
        if str[start:start+4] == 'def ':
            return str[start:start+4] #get_word(i+4, line_len)

#returns the location of the first char in the word (and the word) at 'start' in the str
#get_word(" class  ", 1, len(" class  ") )
#returns (6, 'class', 1)
#( possible_start_of_next_word , word, start_of_word)
def get_word(str, start, str_length):
    i=start
    while i < str_length:
        if str[i] == ' ' or str[i] == '(':
            return (i, str[start:i], start)
        i+=1

#str = " class    FriendFace   "
#get_class_and_name_and_locations(str):
#yields
#keyword: class , keyword_location: 1
#name: FriendFace, name_location: 10
def get_keyword_and_name_and_locations(str):
    str_length = len(str)
    start = find_start_of_a_word(str, str_length)
    keyword_details = q_is_it_a_keyword(str, start)
    start = find_start_of_a_word(str, str_length,keyword_details[1])
    name = get_word(str, start, str_length)
    print 'keyword: %s, keyword_location: %s' % (keyword_details[0],keyword_details[2])
    print 'name: %s, name_location: %s' % (name[1],name[2])  #currently prints end of name and keyword 
    


'''
must have one main function that acts as a controller, selecting which slave function to go to with
 regards to deepness. each of these slave functions map to a deepness level i.e.
 
 main()
 deepness_0_outside_class() => search for class first, if find then call deepness_1_inside_class etc.
 deepness_1_inside_class() => search for functions first
 deepness_2_inside_function =>
 inside_do_end
 inside parenthesise


'''


