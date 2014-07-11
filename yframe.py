#! /usr/bin/env python

from subprocess import *
import sys
import time
import pafy

#Function to convert videos to frames
def convert(name):
    try:
        process = ['avconv', '-i', 'name', '-vsync', '1', '-r', '1', '-an', '-y', 'cwd/frames%d.jpg'] 
        output = call(process)
    except Exception, e:
        print e
        print 'Did not convert video'


#Enter video url to be downloaded
choice = raw_input('Enter url: ')
video = pafy.new(choice)
#print (video.title)

best = video.getbest()
child = best.download(quiet=False)

#time.sleep(555555)


#Call function to convert video to png/jpeg frames
convert(child)



