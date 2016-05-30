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
