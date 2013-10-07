#!/usr/bin/env python

import random
import string
import re
from bs4 import BeautifulSoup
from urlparse import urlparse
import requests
import unicodedata

host = "d.pr"
dir = u'downloads/'

def rnd():
    lst = [random.choice(string.ascii_letters + string.digits) for n in xrange(4)]
    ret = "".join(lst)
    return ret
def writelog(txt):
    l=open('log.txt','wb')
    l.write(txt + "\n")
    l.close()

def chk():
    path = u'http://' + host + "/f/" + rnd()
    status = requests.head(path).status_code
    if status == 200:
        content = requests.get(path).content
        if content.find('<section class="image">') > 0:
            page = BeautifulSoup(''.join(content))
            imgalt = page.findAll('section', {'class':"image"})[0].img['alt']
            print imgalt
            imgsrc = page.findAll('section', {'class':"image"})[0].img['src']
            h = urlparse(imgsrc)
            o=open(dir + unicodedata.normalize('NFKD', imgalt.replace(":","_").replace("\\","_").replace("/","_")).encode('ascii','ignore'), 'wb')
            o.write(requests.get(imgsrc).content)
            o.close()
        elif content.find('<section class="text note">') > 0:
            print path + ' - text note'
            writelog(path + u' - text note')
        else:
            print path + ' - file'
            writelog( path + u' - file')
    return status


while 1:
    chk()
