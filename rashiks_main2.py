# -*- coding: utf-8 -*-
'''
Realization of board-xml-database loading, real-time updating;
topicstarter's/commentator's messages's attributies processing;
obtaining list of all users who posted in the topicstarter's message with specific id
'''
import time
import xml_update_2_0 as xu

#patch requicked to print unicode strings to console
#import win_unicode_console
#win_unicode_console.enable()

#AwesomeInitOfDatabase()
# ^^^ We truly needs this function (need further discussion)

# download and processing last 1000 messages from online-board-xml-database, updating Model, MyDicts using this data
old_lastId = xu.BadInit()

# real-time Model and myDicts update
while True:
    # waiting some time between checking the forum for new messages
    time.sleep(10)
    
    # check forum for new message and process it if it's available
    if xu.CheckForNewMessage(old_lastId):
        lastId = xu.GetLastMessageId()
        
        # download new xmls appeared in time of sleep
        new_xmlstr = xu.DownloadNewXMLs(old_lastId,lastId)
        old_lastId = lastId
        
        # gets message data and updates topstIds, commIds, topicIdStack
        xu.XMLstrProcessing(new_xmlstr)
        print "Message accepted: ", old_lastId
    
    else: print "....... waiting messages ....... last mesid:", old_lastId
    
    # update list of usernames
    new_list = xu.UpdateListOfUserNames(1)
    print "Updating Model with:", new_list, '\n'
    
    M.modelUpdate(new_list)
    xu.DebugSaveToFile(new_list)
