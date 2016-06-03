# -*- coding: utf-8 -*-
import time
import xml_update_2_0 as xu

#old_lastId = -1

#patch to print unicode into console
#import win_unicode_console
#win_unicode_console.enable()

#AwesomeInitOfDatabase()
# ^^^ We truly needs this function
xu.BadInit()
old_lastId = xu.GetLastMessageId()
while True:
    time.sleep(10)

    if xu.CheckForNewMessage(old_lastId):
        lastId = xu.GetLastMessageId()        
        new_xmlstr = xu.DownloadNewXMLs(old_lastId,lastId)
        old_lastId = lastId
        
        # gets message data and updates myDicts
        xu.XMLstrProcessing(new_xmlstr)
        print "Message accepted: ", old_lastId
    else: print "Waiting messages, last processid message id:", old_lastId
    # update list of usernames
    new_list = xu.UpdateListOfUserNames(1)
    print "Updating Model with:", new_list, '\n'
    xu.DebugSaveToFile(new_list)
