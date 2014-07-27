#! /usr/bin/env python

import pafy
import logging
import os
import glob as g
import cv
from math import floor

def convertToPngs(movieName, frameOutName, wdir='', \
					startFrame=0, endFrame=499, maxDim = 128):
	"""
	Converts a saved movie into a collection of png frames

		movieName: name of movie file

		frameOutName: prefix of each frame to be written out
						should not have image type at the end

		wdir: working directory (i.e. where the movie is and
				where the frames will be written). In general
				this should be its own directory for each movie,
				since there are many frames in a given movie.

		startFrame: first frame # to be written out

		endFrame: last frame # to be written out

		maxDim: the maximum number of elements in any one dimension
				of the output image. This should be an integer, but
				if maxDim = False, then it will save the frames
				in their original size.
	"""
	# change to working directory
	os.chdir(wdir)

	# strip frame prefix of unnecessary suffixes
	frameOutName = frameOutName.replace(".png", '')
	frameOutName = frameOutName.replace(".jpeg", '')

	# initiate movie stream
	capture = cv.CaptureFromFile(movieName)

	# extract frame size
	nCols = int(cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH))
	nRows = int(cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_HEIGHT))
	size = (nRows, nCols)
	maxFrameDim = max(size)

	# compute rescaling required based upon input
	scale =float(maxFrameDim)/float(maxDim)
	newSize = (int(floor(size[0]/scale + .5)), int(floor(size[1]/scale + .5)) )

	# extract number of frames in video
	NframesTot = int(cv.GetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_COUNT))

	# loop over frames, writing out those in desired range.
	for k in xrange(NframesTot):
		# i assume that there is no way to start at a particular frame
		# and that we have to loop over all of them sequentially
		frame = cv.QueryFrame(capture)

		if k >= startFrame:
			# TODO: we could put this in a try, except condition,
			# but I'm happy to just let it fail naturally if there is a problem
			# since it is writing out the frames as it progresses, we won't
			# lose anything.
			if maxDim:
				smallFrame = cv.CreateImage(newSize,frame.depth,frame.nChannels)
				cv.Resize(frame, smallFrame)
				frame = smallFrame
			cv.SaveImage(frameOutName + "{0:04d}.png".format(k), frame)

		if k >= endFrame:
			break
		k += 1
	print '\n\nConverted {0} frames'.format(k)
	return 0

def toCamelCase(preOutName, maxWords = 5):
	"""crude function to convert a youtube video name into Camel Case"""
	try:
		preOutName = ''.join([str(u) for u in preOutName if ord(u) < 128])
	except Exception as e:
		raise e
	lenName = len(preOutName)
	if lenName == 0:
		raise ValueError('Given name to format has length 0')
	preOutName = ''.join([u for u in preOutName.title() if u.isalnum() or\
									u.isspace()])
	preOutName = ''.join(preOutName.split(' ')[:min(maxWords,lenName)])
	return preOutName.replace(' ', '')

def main():
	"""
	Downloads movie, creates a directory from the movie's title, 
		and converts the first 500 frames of the movie to pngs in
		the new directory (the frames will be at low resolution).
	
	Note logging feature is experimental and not necessary.

	If you want more frames, you should import this module and call the
		converter from a separate script.
	"""

	logging.basicConfig(filename='log_yframe.log', level=logging.DEBUG,\
			format='%(asctime)s %(message)s')

	#Enter video url to be downloaded
	videoURL = raw_input('Enter url: ')
	response = raw_input('Write frames (y/n)?: ')
	if response[0].lower() == 'y':
		response = raw_input('How many frames?: ')
		try:
			nFrames = int(response)
		except:
			print 'Input not understood.\nExiting\n'
			raise SystemExit
	else:
		print 'No frames to be converted.\n'
		nFrames = 0


	logging.info("received user input: {0}".format(videoURL))
	logging.info("# frames to be converted: {0}".format(nFrames))

	try:
		video = pafy.new(videoURL)
		best = video.getbest(preftype="mp4")
	except Exception as e:
		logging.exception(e)
		print(e)
		raise SystemExit
	if best == None:
		logging.exception("pafy could not connect. Exiting.")
		print 'Could not connect. Exiting'
		raise SystemExit

	logging.info("Successfully instantiated Pafy object from video URL")

	# Name & directory formating.
	cwd = os.getcwd()
	preName = toCamelCase(best.title)
	dirName = "/" + preName + "/"
	wdir = cwd + dirName
	movieName = preName + "." + best.extension
	outName = cwd + dirName + movieName
	msg = "Video Name converted to: {0}".format(preName)
	logging.info(msg)
	print msg

	# see if directory exists
	# TODO: since we only have the first 5 words, there could
	# be two different videos with the same initial 5 words
	# should have a method of dealing with this.
	files = [x.replace(cwd, '').strip('/') for x in g.glob(cwd + "/*")]
	if preName not in files:
		os.system("mkdir {0}".format(wdir))
		logging.info("Created directory {0}".format(wdir))

	# see if movie exists in directory - if not create it
	# TODO: really, we don't need to do this if we just made the directory.
	files = [x.replace(cwd + dirName, "") for x in g.glob(cwd + dirName + "*")]
	if movieName not in files:
		logging.info("Naming video: {0}".format(outName))
		logging.info("Attempting to download video.")
		child = best.download(quiet=False, filepath=outName )
		logging.info("Successful download.")
	else:
		logging.info("File exists; skipping to download.")


	files = [x.replace(cwd + dirName, "") for x in g.glob(cwd+dirName+"*.png")]
	if len(files) == 0 and nFrames > 0:
		logging.info("Attempting to convert movie to pngs.")
		convertToPngs(movieName, preName, wdir=wdir)
		logging.info("converted movie to pngs.")
	elif nFrames != 0:
		logging.info("Exiting - pngs exist.")
		print "Some pngs already exist. This code is only for demos.\nExiting."
		logging.info("Exited due to pre-existing pngs.")
		raise SystemExit
	logging.info("Success!\n\n")
	print "\nSuccess!\n"

if __name__ == '__main__':
	main()
