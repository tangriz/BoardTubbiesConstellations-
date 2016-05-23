# -*- coding: utf-8 -*-
import urllib
import xml.etree.ElementTree as ET
from lxml import etree

import win_unicode_console
win_unicode_console.enable()
parser = etree.XMLParser(recover=True)

tpostIds = dict()
commIds = dict()

# input xml files path
fin_path = 'D:/program_backup/python-sources/data/board_pages/xmls/'

# init output data files path
fout_path = 'D:/program_backup/python-sources/data/output/'
flog = open(fout_path+'log'+'.txt','a')

# input first and last xml to proccessing
first_def = 1
last_def = 9309
inp = raw_input('Enter START thousand XML to proccessing: ')
if len(inp) < 1 : first = first_def
try: first = int(inp)
except: first = first_def

inp = raw_input('Enter FINISH thousand XML to proccessing: ')
if len(inp) < 1 : last = last_def
try: last = int(inp)
except: last = last_def

for i in range(first,last+1) :
    fname0 = i#'8999'
    fname = fin_path + 'xmlfp.jsp' + str(fname0) + '.xml' #str(act_to/1000) + '.xml'

    with open(fname,'r') as fin :
        xmlstring = fin.read()
        
    xmltree = etree.fromstring(xmlstring, parser=parser)
    root = xmltree#.getroot()
    #usernames = dict()

    for message in root[0:999]:
        
        del_status = message.find('status')
        if (del_status is not None) and del_status.text == 'deleted' :
            flog.write('message deleted' + '\n')
            continue        
        
        mesId = int(message.get('id'))
        #print 'id:', mesId
        
        try: parId = int(message.find('info/parentId').text)
        except:
            print 'non-numeric parent id!'
            flog.write(str(mesId) + ' - non-numeric parent id!' + '\n')
            exit()
        #print 'ParId:', int(parId)
        
        user = message.find('author/name').text
        if user is None :
            print 'USER is NONE!!!', mesId
            flog.write('The name is ABSENT, html/xml corruption? MesId:' + str(mesId) + '\n')
            user = '_NoneType_'
        # try: print 'Name:', user
        # except:
            # print 'The name is bad, printing message ID:', mesId
            # flog.write('The name is bad, mesID:' + str(mesId) + '\n')
            # exit()
        
        if parId == 0 : tpostIds[mesId] = [user]
        elif parId < 0 :
            #print 'Fuck OFF the data! parentId = %d! messaga # %d' % (parId, mesId)
            continue
        elif parId > 0 :
            if parId in tpostIds :
                tpostIds[parId].append(user)
                commIds[mesId] = parId            
            elif parId in commIds :
                tpId = commIds[parId]
                #print tpId
                tpostIds[tpId].append(user)
                commIds[mesId] = tpId
            else : continue
    
# for kee, vaals in tpostIds.items():
    # if kee == 7501527 :
        # vaal = repr(vaals).decode('utf-8')
        #print vaal
    # try: print vaal
    # except:
        # print '=====shit happens..====='
        # repr(kee)
        # repr(vaal)
        # exit()

fout = open(fout_path+'all'+'.txt','a')
tu = tpostIds.items()
tu.sort()
#print tu
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
fout.close()
flog.close()
win_unicode_console.disable()
#encode_error_mId = 7501947
