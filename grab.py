#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import string
import re
from bs4 import BeautifulSoup
from urlparse import urlparse
import requests
import unicodedata
import time

host = u"d.pr"
dir = u'downloads/'

headers = {
    'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3',
    'Referer' : 'http://d.pr'
}

def rnd():
    lst = [random.choice(string.ascii_letters + string.digits) for n in xrange(4)]
    ret = "".join(lst)
    return ret

def writelog(txt):
    l=open(u'log.txt','wb')
    l.write(txt + "\n")
    l.close()
	
def chk():
    path = u'http://' + host + u"/f/" + rnd()
    status = requests.head(path).status_code
    if status == 200:
        content = requests.get(path, headers=headers).content
        if content.find('<section class="image">') > 0:
            page = BeautifulSoup(''.join(content))
            imgalt = page.findAll('section', {'class':"image"})[0].img['alt']
            print imgalt
            imgsrc = page.findAll('section', {'class':"image"})[0].img['src']
            h = urlparse(imgsrc)
            o=open(dir + unicodedata.normalize('NFKD', imgalt.replace(":","_").replace("\\","_").replace("/","_")).encode('utf-8','ignore'), 'wb')
            o.write(requests.get(imgsrc).content)
            o.close()
        elif content.find('<section class="text note">') > 0:
            print path + ' - text note'
            writelog(path + u' - text note')
        else:
            print path + ' - file'
            writelog( path + u' - file')
    time.sleep(5)
    return status
while 1:

    print chk()

