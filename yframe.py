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

	# loop over frames, writing out those in desired range.
	frame = True
	k = 0
	while frame:
		frame = cv.QueryFrame(capture)
		if k >= startFrame:
			# TODO: we could put this in a try, except condition,
			# but I'm happy to just let it fail naturally if there is a problem
			# since it is writing out the frames as it progresses, we won't
			# lose anything.
			size = cv.GetSize(frame)
			if maxDim:
				maxFrameDim = max(size)
				scale =float(maxFrameDim)/float(maxDim)
				newSize = (int(floor(size[0]/scale + .5)), \
							int(floor(size[1]/scale + .5)) )
				smallFrame = cv.CreateImage(newSize,frame.depth,frame.nChannels)
				cv.Resize(frame, smallFrame)
				frame = smallFrame
			cv.SaveImage(frameOutName + "{0:04d}.png".format(k), frame)

		if k >= endFrame:
			break
		k += 1
	print '\n\nConverted {0} frames'.format(k)
	return 0

def toCamelCase(preOutName):
	"""crude function to convert a youtube video name into Camel Case"""
	outName = ''
	space = False
	nWords = 0
	for s in preOutName:
		if s == ' ':
			space = True
			nWords += 1
			if nWords == 5:
				break
		if s.isalnum():
			if space:
				s = s.upper()
				space = False
			else:
				s = s.lower()
			outName += s
	return outName

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
	choice = raw_input('Enter url: ')
	logging.info("received user input: {0}".format(choice))

	video = pafy.new(choice)
	try:
		best = video.getbest()
	except Exception as e:
		logging.exception(e)
		print 'Could not connect. Exiting'
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
	logging.info("Video Name: {0}".format(best.title))
	logging.info("Video Name converted to: {0}".format(preName))

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
	if len(files) == 0:
		logging.info("Attempting to convert movie to pngs.")
		convertToPngs(movieName, preName, wdir=wdir)
		logging.info("converted movie to pngs.")
	else:
		logging.info("Exiting - pngs exist.")
		print "Some pngs already exist. This code is only for demos.\nExiting."
		logging.info("Exited due to pre-existing pngs.")
		raise SystemExit
	logging.info("Success!\n\n")
	print "\nSuccess!\n"

if __name__ == '__main__':
	main()
