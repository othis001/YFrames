#!/usr/bin/env python

import os
import numpy as np
import matplotlib.pyplot as plt
import Image
import glob as g
import cv
from math import floor

# put the name of the directory that holds the mp4 in preName.
# there should be a file preName.mp4 in that directory.
preName = 'wildNothingParadiseOfficial'
# Nsummary is the number of summary frames that you desire.
Nsummary = 50

#----------------------------------------------------------
movieName = preName + '.mp4'
cdir = os.getcwd()
wdir = cdir + '/' + preName
fileName = movieName

frameOutName = "frame"
os.chdir(wdir)

frameStep = 20
maxDim = 64

# initiate movie stream
capture = cv.CaptureFromFile(movieName)
NframesTot = int(cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_COUNT))
Nframes = floor(float(NframesTot)/float(frameStep) + 1.5)

frame = True
change = np.zeros( Nframes )
k = 0
j= 0
for k in xrange(NframesTot):
	frame = cv.QueryFrame(capture)
	if k % frameStep == 0:
		if maxDim:
			size = cv.GetSize(frame)
			maxFrameDim = max(size)
			scale =float(maxFrameDim)/float(maxDim)
			newSize = (int(floor(size[0]/scale + .5)), \
						int(floor(size[1]/scale + .5)) )
			smallFrame = cv.CreateImage(newSize,frame.depth,frame.nChannels)
			cv.Resize(frame, smallFrame)
			frame = smallFrame
		if j == 0:
			imOld = np.sum( np.asarray( frame[:,:], dtype=np.float), axis=2)
		else:
			imOld = imNew

		imNew = np.sum( np.asarray( frame[:,:] , dtype=np.float), axis=2)
		change[j] = np.linalg.norm( np.abs( imOld - imNew) )
		j+= 1

suspect = np.argsort( change )[::-1][:Nsummary]

suspectFrames = [j*frameStep for j in suspect]
capture = cv.CaptureFromFile(movieName)
frame = True

s = 0
for k in xrange(NframesTot):
	frame = cv.QueryFrame(capture)
	if k in suspectFrames:
		cv.SaveImage("SummaryFrames{0:03d}.png".format(s), frame)
		s += 1

print '\nSuccess!\n'
