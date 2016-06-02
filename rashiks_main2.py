# -*- coding: utf-8 -*-
import time
import xml_update_2_0 as xu

#old_lastId = -1

#patch to print unicode into console
import win_unicode_console
win_unicode_console.enable()

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
    

# for kee, vaals in iv.topstIds.items():
    # for usr in vaals :
        # print usr.encode('utf-8')
    # except:
        # print '=====shit happens..====='
        # repr(kee)
        # repr(vaals)
        # exit()

# save topstIds.items to the file on hrad disk
fout_path = 'D:/program_backup/python-sources/data/output/'
fout = open(fout_path+'test'+'.txt','a')
tu = xu.topstIds.items()
tu.sort()
for kee, vaals in tu :
    fout.write(str(kee) + ': ')
    for usr in vaals :
        try:
            fout.write('[' + usr.encode('utf-8') + ']')
        except:
            print '=== shit in writing user to file ===', kee, usr
            print 'user_name type:', type(usr), 'user_name:', str(usr)
            fout.close()
            raise
           # print usr            
            exit()
    fout.write('\n')
fout.write('='*20 + '\n')
stck = xu.topicIdStack
for mId, mTi in stck :
    print mTi.encode('utf-8')
    fout.write(str(mId) + ': ' + mTi.encode('utf-8') + '\n')

fout.close()


