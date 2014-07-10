#! /usr/bin/env python

from subprocess import *
import sys
import time

#Function to convert videos to frames
def convert(name):
    try:
        process = ['avconv', '-i', 'name', '-vsync', '1', '-r', '1', '-an', '-y', 'cwd/frames%d.jpg'] 
        output = Popen(process, shell=True, stderr=PIPE)
    except Exception, e:
        print e
        print 'Did not convert video'


#Enter video url to be downloaded
choice = raw_input('Enter url: ')
child = Popen('youtube-dl "%s"' %choice, shell=True, stderr=PIPE)
child.wait()
#Call function to convert video to png/jpeg frames
convert(child)



