#! /usr/bin/env python

import pafy
import logging
import os
import glob as g
import cv

def convertToPngs(fileName, frameOutName, wdir, startFrame =0, endFrame=99):
	"""Converts a saved move into a collection of png frames"""
	os.chdir(wdir)

	frameOutName = frameOutName.strip(".png")
	frameOutName = frameOutName.strip(".jpeg")

	capture = cv.CaptureFromFile(fileName)

	frame = True
	k = 0
	while frame:
		if k >= startFrame:
			frame = cv.QueryFrame(capture)
			cv.SaveImage(frameOutName + "{0:04d}.png".format(k), frame)
		if k >= endFrame:
			break
		k += 1
	print 'Converted {0} frames'.format(k)

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
			outName += s
	return outName

def main():
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
	logging.info("Attempting to download video.")

	# Name & directory formating.
	cwd = os.getcwd()
	preName = toCamelCase(best.title)
	dirName = "/" + preName + "/"
	wdir = cwd + dirName
	movieName = preName + "." + best.extension
	outName = cwd + dirName + movieName

	# see if directory exists
	# TODO: since we only have the first 5 words, there could
	# be two different videos with the same initial 5 words
	# should have a method of dealing with this.
	files = [x.replace(cwd, '').strip('/') for x in g.glob(cwd + "/*")]
	if preName not in files:
		logging.info("Creating directory {dirName}")
		os.system("mkdir {0}".format(wdir))

	# see if movie exists in directory - if not create it
	# TODO: really, we don't need to do this if we just made the directory.
	files = [x.replace(cwd + dirName, "") for x in g.glob(cwd + dirName + "*")]
	print outName
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
		convertToPngs(movieName, preName, wdir)
		logging.info("converted movie to pngs.")
	else:
		logging.info("Exiting - pngs exist.")
		print "Some pngs already exist. This code is only for demos.\nExiting."
		logging.info("Exited due to pre-existing pngs.")
		raise SystemExit

if __name__ == '__main__':
	main()
