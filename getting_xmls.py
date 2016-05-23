# -*- coding: utf-8 -*-
import urllib
import time

fpath = 'D:/program_backup/python-sources/data/board_pages/xmls_last/'

url_prefix = 'http://zlo.rt.mipt.ru:7500/xmlfp/xmlfp.jsp?xmlfp=messages&site=0'
fromm = 8996001
too = fromm + 999

num_of_to_get = 313
i = 0
extimes = list()

while i < num_of_to_get :
    act_from = fromm + i*1000
    act_to = too + i*1000
    url = url_prefix + '&from=' + str(act_from) + '&to=' + str(act_to)
    t_bef = time.time()
    try: xml = urllib.urlopen(url).read()
    except:
        print "connection error! Waiting 1 minute."
        time.sleep(60)
        xml = urllib.urlopen(url).read()
    exe_time = time.time() - t_bef
    
    print '%s xml received in %s sec.\n' % (i, exe_time)
    #extimes.append(exe_time)

    fname = fpath + 'xmlfp.jsp' + str(act_to/1000) + '.xml'
    fh = open(fname, 'w')
    fh.write(xml)
    fh.close()
    print 'File has written --- %s\n\n' % i
    
    fname_times = fpath + 'new_times.txt'
    with open(fname_times, "a") as myfile:
        myfile.write("i=%s\t%s\n" % (act_from, exe_time))
        
    i += 1
    time.sleep(12)

print 'Done!'

