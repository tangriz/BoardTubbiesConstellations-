# -*- coding: utf-8 -*-
'''
I hate you, KVasya! This is fucking bullshit!!!!
I fucking haven't understand!! My try:
The program uses these functions in the order of appareance:
1. xu.BadInit() - download last N=1000 posted messages, extract data,
                  updates Model with it and return last processed message
                  
Then in the while cycle real-time part starts to operate -->
2. time.sleep(T) - waiting T seconds between checks of the forum for new messages

3. xu.CheckForNewMessage(lastProcId) - in the if-else clause we check
                                      for new messages available on forum
                
4. xu.GetLastMessageId() - get last message index available on forum (not processed yet)

5. xu.DownloadNewXMLs(lastProcId,lastId) - get new forum messages in range (lastProcId,lastId),
                                            (those ones that are not processed yet)
                                            
6. xu.XMLstrProcessing(new_xmlstr) - process the xml string: get message data, etc.
                                    See xu module for details.
7. xu.UpdateListOfUserNames(X) - get new list of users, which commented in the TS post X days ago.
8. M.modelUpdate(new_list) - updates model with new list of users
'''
import time
# this module contains all functions and classes requied to achieve the purpose
import xml_update_2_0 as xu

# download and processing last 1000 messages, updating Model with them
lastProcId = xu.BadInit() # get last _processed_ message index

# real-time Model update
while True:
    # waiting 10 seconds between checks of the forum for new messages
    time.sleep(10)
    
    # check forum for new message and process it if it's available
    if xu.CheckForNewMessage(lastProcId):
        lastId = xu.GetLastMessageId() # get last message index available on forum (not processed yet)
        
        # download new xmls appeared in the wait time and convert it to a string
        new_xmlstr = xu.DownloadNewXMLs(lastProcId,lastId) # may be bug here. Should be (lastProcId+1,lastId)
        
        # gets message data from xml_string and process it
        # Wanna know what does "process" mean? That is - br-bla-blm-grr-uhm (my guts moving around).
        # or may look in xu module. I hate you, KVasya!!!
        xu.XMLstrProcessing(new_xmlstr)
        lastProcId = lastId # new messages processed. By now last processed message is the last on forum.
        print "Last message accepted: ", lastProcId
    
    else: print "....... waiting messages ....... last processed MesId:", lastProcId
    
    # get new list of usernames
    new_list = xu.UpdateListOfUserNames(1)
    print "Updating Model with:", new_list, '\n'
    
    # Updating Model with new_list
    M.modelUpdate(new_list)
    
    #xu.DebugSaveToFile(new_list)
