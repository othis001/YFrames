#! /usr/bin/env python

from subprocess import *
import sys
import time

#Function to convert videos to frames
def convert(name):
    try:
        process = ['avconv', '-i', 'name', '-vsync', '1', '-r', '1', '-an', '-y', '/home/sophos/workspace/Y_Frames/frames%d.jpg'] 
    except Exception, e:
        print e
        print 'Did not convert video'


#Enter video url to be downloaded
choice = raw_input('Enter url: ')
child = Popen('youtube-dl "%s"' %choice, shell=True, stderr=PIPE)

#Call function to convert video to png/jpeg frames
convert(child)



