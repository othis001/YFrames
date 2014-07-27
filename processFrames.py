#!/usr/bin/env python

import os
import numpy as np
import matplotlib.pyplot as plt
import Image
import glob as g
import cv
from math import floor
import time


preName = 'whatsABitcoinShortAnd'
frameStep = 2

# maxDim is the size of the reduced image that we use.
maxDim = 32

#----------------------------------------------------------
movieName = preName + '.mp4'
cdir = os.getcwd()
wdir = cdir + '/' + preName
fileName = movieName

frameOutName = "frame"
os.chdir(wdir)


# initiate movie stream
capture = cv.CaptureFromFile(movieName)
NframesTot = 400
#NframesTot = int(cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_COUNT))

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
                        eigVec[:,0] /= np.linalg.norm(eigVec[:,0])
                        framesArray[j,:] =  1. - eigVec[:,0]
                        j += 1

#Create and populate array to store dot product of the eigenvectors of the frames 
eigArray = np.zeros(int(Nframes)) 
eigArray = np.array([np.linalg.norm(np.dot(framesArray[k,:],framesArray[100,:]))\
					 for k in xrange(int(Nframes)) if k != int(Nframes) - 1])

eigArray = np.gradient(eigArray)

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

ax.plot(X, np.log1p(Yeig),'r',linewidth = 2, alpha = 0.7)
ax.set_xlabel("Magnitude (logscale)")
ax.set_ylabel("Number of frames")
ax.set_title("Distribution of gradient of eigenvector direction")
ax.legend()
ax.grid(True)


#Width of bars
width = 0.001

ax = fig.add_subplot(212)
ax.bar(range(len(eigArray)), eigArray, width)
ax.set_xlabel("frame number")
ax.set_ylabel("Magnitude")
ax.set_title("Gradient of eigenvector direction")
ax.grid(True)
plt.tight_layout()
plt.show()
