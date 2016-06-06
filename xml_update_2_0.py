# -*- coding: utf-8 -*-
'''
I don't know how I have to describe this.
It just contains all functions that we need to deal with online-xml-databases (xmlfp board service),
download xml, extracting data, updating list of usernames
'''
import urllib
import datetime
from lxml import etree

# import global data structures
from init_vars import *

# import high-usage function for parsing XML
used_parser = etree.XMLParser(recover=True)

# for future
def xmlDatabaseUpdate():
    # init on starting server
    # check xml-files on hard and download new xml-thousand-files 
    return True

# make url-request to xmlfp board service and get MessageId of the last available message in xml-database
# Attention! The last message on the forum is NOT always the last message available in xml-database. Especially on night..
def GetLastMessageId():
    url_request = 'http://zlo.rt.mipt.ru:7500/xmlfp/xmlfp.jsp?xmlfp=lastMessageNumber&site=0'

    lastnum_xmlstr = urllib.urlopen(url_request).read() # add exception for url non-availability
    xmltree = etree.fromstring(lastnum_xmlstr, parser=used_parser)

    lastId = int(xmltree.text)
    return lastId

# check if new message in xml-database is available
def CheckForNewMessage(old_Id):
    new_Id = GetLastMessageId()
    if new_Id == old_Id:
        return False
    elif new_Id > old_Id:
        return True

#is_board_updated = CheckForNewMessage(last_Id)
#print is_board_updated

# download xml files with a giving message index range
def DownloadNewXMLs(firstId,lastId):
    url_prefix = 'http://zlo.rt.mipt.ru:7500/xmlfp/xmlfp.jsp?xmlfp=messages&site=0'
    url_request = url_prefix + '&from=' + str(firstId) + '&to=' + str(lastId) # no more than 1000 messages at once
    xmlstr = urllib.urlopen(url_request).read() # add exception for url non-availability
    return(xmlstr)

# define a class for parsing xml and extracting message data
class Message:
    
    date = None # date/time of the post
    status = None # = deleted, if message isn't available in xml-database; =None otherwise
    id = None # message index
    parentId = None # index of the message to whom user replies
    name = None # user name
    
    def __init__(self, msg):
        # check if message is deleted from xml-database
        self.status = msg.find('status')
    
    # method to extract all needful tags from <message>
    def fill(self, msg):
        self.date = msg.find('info/date').text
        
        self.id = int(msg.get('id'))
        #print 'id:', self.id
        
        self.parentId = int(msg.find('info/parentId').text)
        #print 'ParId:', self.parentId
        
        self.name = msg.find('author/name').text
        # check if <name> tag is absent        
        if self.name == None:
            self.name == self.id
            #flog.write('The name is ABSENT, html/xml corruption? MesId:' + Msg.id + '\n')

# construct and update dictionaries with structures described in init_vars module
def UpdateDicts(m):
    
    # adding TS username to Dict.            
    if m.parentId == 0 : topstIds[m.id] = [m.name]
        
    # check if message removed from the xml-post-tree (common value = -10)
    elif m.parentId < 0 :
        return -10
        # print 'Message removed from xml-post-tree! parentId = %d! messaga # %d' % (m.parentId, m.id)
        
    # main proccess    
    elif m.parentId > 0 :
        
        # check if commentator is of 1st level
        if m.parentId in topstIds :
            # append username to values of -TS message Id- key
            topstIds[m.parentId].append(m.name)
            # 1st level commentator is getting to know its parent (TS user)
            commIds[m.id] = m.parentId
            
        # check if commentator is of 2st or more level
        elif m.parentId in commIds :
            # find out more than 1st level commentator's progenitor (TS user)
            TSId = commIds[m.parentId]
            # append username to values of -TS message Id- = TSId key
            topstIds[TSId].append(m.name)
            # more than 1st level commentator is getting to know its progenitor (TS user)
            commIds[m.id] = TSId
            
        else :
            return -1
            # print 'old TS message is commented. Retrieving early xmls..' # <-- add this functionality     

# update stack-list with tuples = (TS message id, TS message posting date)
def UpdateStackOfTS(m):
    if m.parentId == 0 : topicIdStack.append((m.id,m.date))        

# process downloaded xml-string: parsing, extracting values, updating my dicts
def XMLstrProcessing(xmlstr):
    xmltree = etree.fromstring(xmlstr, parser=used_parser)
    
    for idx, msgtag in enumerate(xmltree):   
                
        Msg = Message(msgtag)
        
        if Msg.status == 'deleted' :
            print 'deleted message is processed!'
            #flog.write('message deleted, id = ' + str(firstId + idx) + '\n')
            continue        
        
        Msg.fill(msgtag)
        UpdateDicts(Msg)
        UpdateStackOfTS(Msg)

# check if the moment to grab data to the Model has come (waiting for users to stop posting to TS post)
# update list of user names
def UpdateListOfUserNames(days_to_wait):
    tnow = datetime.datetime.now()
    tlag = datetime.timedelta(days=days_to_wait)
    t_load = tnow - tlag
    t_post = topicIdStack[0][1]
    print t_post, ' '*4, t_load.isoformat()
    
    # check if the time's come
    if t_post < t_load.isoformat() :
        # get user names to update model
        LOUN = topstIds[topicIdStack[0][0]]
        del topicIdStack[0]
        return LOUN
    else:
        print "nothing to update", topicIdStack[0]
        return None
        
# saving to file the values that updates the model
# just for gebbuging
def DebugSaveToFile(inp):
    fout_path = 'D:/program_backup/python-sources/data/output/'
    if inp is not None :
        fout = open(fout_path+'model_data'+'.txt','a')
        for usr in inp :
            print usr
            fout.write('[' + usr.encode('utf-8') + ']')
            fout.write('\n')
        fout.close()

# temporal xml-database upload on server start
# do exact thing that whole service do but using 1000 last forum messages
def BadInit():
    last_mes_id = GetLastMessageId()
    xmls = DownloadNewXMLs(last_mes_id-999, last_mes_id)
    XMLstrProcessing(xmls)
    while True:
        LOUN = UpdateListOfUserNames(1)
        print "list o users:", LOUN
        if LOUN is None:
            print "\n", "======= END of BadInit =======", "\n"
            return last_mes_id
            break
        M.modelUpdate(LOUN)
        DebugSaveToFile(LOUN)
    
