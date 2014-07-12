#!/usr/bin/env python

import os
import numpy as np
import matplotlib.pyplot as plt
import Image
import glob as g
import cv
from math import floor

<<<<<<< HEAD
# put the name of the directory that holds the mp4 in preName.
# there should be a file preName.mp4 in that directory.
preName = 'wildNothingParadiseOfficial'
# Nsummary is the number of summary frames that you desire.
Nsummary = 50
=======
# first use yframe to download this file:
# http://www.youtube.com/watch?v=NU7Mj0Ak14A

# then, don't change anything and run this code
preName = 'whatsABitcoinShortAnd'
# frameStep is the frequency of frames that we look at
# we don't look at everyframe since they are typically changing
# slowly. You can set it to 1 if you want to get every frame
# or set it to 5 or 10 or 20 and see the change.
frameStep = 2
>>>>>>> 8c4c00a61cf482e620bd9c310e2dbaf38c034ae8

# maxDim is the size of the reduced image that we use.
# you can vary it and see the difference. It might be 
# important to set it low on your computer for performance
# reasons (i.e. 64/32/16).
maxDim = 128

# we are not using Nsummary right now.
# Nsummary is the number of summary frames that you desire.
# Nsummary = 50
#----------------------------------------------------------
movieName = preName + '.mp4'
cdir = os.getcwd()
wdir = cdir + '/' + preName
fileName = movieName

frameOutName = "frame"
os.chdir(wdir)


# initiate movie stream
capture = cv.CaptureFromFile(movieName)
NframesTot = int(cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_COUNT))
Nframes = floor(float(NframesTot)/float(frameStep) + 1.5)

change = np.zeros( Nframes )
grad = np.zeros( Nframes )
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
			imRef = np.sum( np.asarray( frame[:,:], dtype=np.float), axis=2)
			imOld = imRef
		else:
			imOld = imNew
			pass

		imNew = np.sum( np.asarray( frame[:,:] , dtype=np.float), axis=2)
		change[j] = np.linalg.norm( np.abs( imRef - imNew) )
		grad[j] = np.linalg.norm( np.abs( imOld - imNew) )
		j+= 1

<<<<<<< HEAD
suspect = np.argsort( change )[::-1][:Nsummary]
=======
refChange = np.abs(np.gradient(change))
gradChange = np.abs(np.gradient(grad))
# set endpoints to zero since there are no data there
gradChange[:2] = 0.
gradChange[-2:] = 0.

refChange[:2] = 0.
refChange[-2:] = 0.

# normalization just to put on the same scale
# just for visualization
gradChange /= np.sum(gradChange)
refChange /= np.sum(refChange)

# don't worry to much about the syntax for the plotting
# but there is plenty of online documentation if you are interested
# stack overflow is your friend.
fig = plt.figure(1)
ax = fig.add_subplot(211)
gradBins, edges = np.histogram(gradChange, 50)
refBins, edges = np.histogram(refChange, 50)
left,right = edges[:-1],edges[1:]
X = np.array([left,right]).T.flatten()
Ygrad = np.array([gradBins,gradBins]).T.flatten()
Yref = np.array([refBins,refBins]).T.flatten()
>>>>>>> 8c4c00a61cf482e620bd9c310e2dbaf38c034ae8

# note that these are on a log scale
ax.plot(X,np.log(1.+Ygrad),'r',linewidth = 2, alpha = 0.7, label = 'gradient')
ax.plot(X,np.log(1.+Yref), 'k', linewidth = 2, alpha = 0.7, label = 'reference')
ax.set_xlabel("Magnitude")
ax.set_ylabel("Log (2) of Number of frames")
ax.set_title("Distribution of metrics")
ax.legend()
ax.grid(True)

ax = fig.add_subplot(212)
ax.plot(gradChange, 'r', linewidth = 2, alpha = 0.7, label = 'gradient')
ax.plot(refChange, 'k', linewidth = 2, alpha = 0.7, label = 'reference')
ax.legend()
ax.set_xlabel("time")
ax.set_ylabel("Magnitude")
ax.set_title("Plot of metrics")
ax.grid(True)
plt.show()


# ignore this part - we're not writing out the summary
# at this moment.
"""
suspect = np.argsort( gradChange )[::-1][:Nsummary]
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
"""


