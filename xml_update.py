# -*- coding: utf-8 -*-

import urllib
from lxml import etree
from init_vars import *

a = 4
used_parser = etree.XMLParser(recover=True)

def xmlDatabaseUpdate():
    # init on starting server
    # check xml-files on hard and download new xml-files 
    return True

def GetLastMessageId():
    url_request = 'http://zlo.rt.mipt.ru:7500/xmlfp/xmlfp.jsp?xmlfp=lastMessageNumber&site=0'

    lastnum_xmlstr = urllib.urlopen(url_request).read() # add exception for url non-availability
    xmltree = etree.fromstring(lastnum_xmlstr, parser=used_parser)

    lastId = int(xmltree.text)
    return lastId
    
#last_Id = GetLastMessageId()
#print last_Id

def CheckForNewMessage(old_Id):
    new_Id = GetLastMessageId()
    if new_Id == old_Id:
        return False
    elif new_Id > old_Id:
        return True

#is_board_updated = CheckForNewMessage(last_Id)
#print is_board_updated

#exit()

def DownloadNewMessages(firstId,lastId):
    url_prefix = 'http://zlo.rt.mipt.ru:7500/xmlfp/xmlfp.jsp?xmlfp=messages&site=0'
    url_request = url_prefix + '&from=' + str(firstId) + '&to=' + str(lastId) # no more than 1000 messages at once
    xmlstr = urllib.urlopen(url_request).read() # add exception for url non-availability
    return(xmlstr)

def UpdateDicts(xmlstr):
    xmltree = etree.fromstring(xmlstr, parser=used_parser)
    
    for idx, message in enumerate(xmltree):   
        
        # check if message is deleted from xml-database
        del_status = message.find('status')
        if (del_status is not None) and del_status.text == 'deleted' :
            #flog.write('message deleted, id = ' + str(firstId + idx) + '\n')
            continue        
        
        mesId = int(message.get('id'))
        #print 'id:', mesId
        
        parId = int(message.find('info/parentId').text)
        #print 'ParId:', int(parId)
        
        user = message.find('author/name').text
        # check if <name> tag is absent
        if user is None :
            #print 'USER is NONE!!!', mesId
            #flog.write('The name is ABSENT, html/xml corruption? MesId:' + str(mesId) + '\n')
            user = '_NoneType_'#str(mesId)
        
        # adding TS username to Dict.
        if parId == 0 : topstIds[mesId] = [user]
        # check if message removed from the xml-post-tree (common value = -10)
        elif parId < 0 :
            #print 'Message removed from xml-post-tree! parentId = %d! messaga # %d' % (parId, mesId)
            continue
        # main proccess
        elif parId > 0 :
            # check if commentator is of 1st level
            if parId in topstIds :
                # append username to values of -TS message Id- key
                topstIds[parId].append(user)
                # 1st level commentator is getting to know its parent (TS user)
                commIds[mesId] = parId
            # check if commentator is of 2st or more level
            elif parId in commIds :
                # find out more than 1st level commentator's progenitor (TS user)
                TSId = commIds[parId]
                # append username to values of -TS message Id- = TSId key
                topstIds[TSId].append(user)
                # more than 1st level commentator is getting to know its progenitor (TS user)
                commIds[mesId] = TSId
            else :
                #print 'old TS message is commented. Retrieving early xmls..' # add this functionality
                continue
        
    