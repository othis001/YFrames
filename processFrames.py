#!/usr/bin/env python

import os
import numpy as np
import matplotlib.pyplot as plt
import Image
import glob as g
import cv
from math import floor
import time


# put the name of the directory that holds the mp4 in preName.
# there should be a file preName.mp4 in that directory.
#preName = 'wildNothingParadiseOfficial'
# Nsummary is the number of summary frames that you desire.
Nsummary = 50
# first use yframe to download this file:
# http://www.youtube.com/watch?v=NU7Mj0Ak14A

# then, don't change anything and run this code
preName = 'whatsABitcoinShortAnd'
# frameStep is the frequency of frames that we look at
# we don't look at everyframe since they are typically changing
# slowly. You can set it to 1 if you want to get every frame
# or set it to 5 or 10 or 20 and see the change.
frameStep = 2

# maxDim is the size of the reduced image that we use.
# you can vary it and see the difference. It might be 
# important to set it low on your computer for performance
# reasons (i.e. 64/32/16).
maxDim = 64

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

framesArray = np.zeros( (int(Nframes), maxDim), dtype=complex)
j= 0
for k in xrange(NframesTot):
        frame = cv.QueryFrame(capture)
        if k % frameStep == 0:  
                if maxDim:
                        size = cv.GetSize(frame)
                        maxFrameDim = max(size)
                        scale = float(maxFrameDim)/float(maxDim)
                        newSize = (int(floor(size[0]/scale + .5)), \
                                                int(floor(size[0]/scale + .5)) )
                        smallFrame = cv.CreateImage(newSize,frame.depth,frame.nChannels)
                        cv.Resize(frame, smallFrame)
                        Im = np.array(smallFrame[:]).mean(axis=2)
                        eigVal, eigVec = np.linalg.eig(Im)
                        eigVec[:,0] = eigVec[:,0]/np.linalg.norm(eigVec[:,0])
                        framesArray[j,:] =  eigVec[:,0]
                        j += 1

#Create and populate array to store dot product of the eigenvectors of the frames 
eigArray = np.zeros(int(Nframes)) 
eigArray = np.array([np.linalg.norm(np.dot(framesArray[k,:], framesArray[k+1,:])) for k in xrange(int(Nframes)) if k != int(Nframes) - 1])

print 'The eigArray is: ', eigArray.shape


# don't worry to much about the syntax for the plotting
# but there is plenty of online documentation if you are interested
# stack overflow is your friend.
fig = plt.figure(1)
ax = fig.add_subplot(211)
eigBins, edges = np.histogram(abs(eigArray), 50)
left,right = edges[:-1],edges[1:]
X = np.array([left,right]).T.flatten()
Yeig = np.array([eigBins,eigBins]).T.flatten()


ax.plot(X, np.log(Yeig + 1.),'r',linewidth = 2, alpha = 0.7, label = 'Dot product of eigenvectors')
ax.set_xlabel("Magnitude")
ax.set_ylabel("Number of frames")
ax.set_title("Distribution of dot product")
ax.legend()
ax.grid(True)


#Width of bars
width = 0.001

ax = fig.add_subplot(212)
ax.bar(np.arange(0,1890), eigArray, width, label = 'Dot product of eigenvectors')
ax.legend()
ax.set_xlabel("time")
ax.set_ylabel("Magnitude")
ax.set_title("Plot of metrics")
ax.grid(True)
plt.show()



