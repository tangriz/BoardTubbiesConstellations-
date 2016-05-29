# -*- coding: utf-8 -*-
import xml_update as xu
import init_vars as iv

# patch to print unicode into console
# import win_unicode_console
# win_unicode_console.enable()

lastId = xu.GetLastMessageId()
firstId = lastId - 200
new_xmlstr = xu.DownloadNewMessages(firstId,lastId)
xu.UpdateDicts(new_xmlstr)

# for kee, vaals in iv.topstIds.items():
    # for usr in vaals :
        # print usr.encode('utf-8')
    # except:
        # print '=====shit happens..====='
        # repr(kee)
        # repr(vaals)
        # exit()


fout_path = 'D:/program_backup/python-sources/data/output/'
fout = open(fout_path+'test'+'.txt','a')
tu = iv.topstIds.items()
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

