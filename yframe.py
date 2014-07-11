#! /usr/bin/env python

import pafy
import logging
import os
import glob as g

try:
	import cv
except:
	print "\nYou must install open cv\n"
	raise SystemExit
	
def convertToPngs(fileName, frameOutName, wdir):
	"""Converts a saved move into a collection of png frames"""
	os.chdir(wdir)

	frameOutName = frameOutName.strip(".png")
	frameOutName = frameOutName.strip(".jpeg")

	capture = cv.CaptureFromFile(fileName)

	frame = True
	k = 0
	while frame:
		frame = cv.QueryFrame(capture)
		cv.SaveImage(frameOutName + "{0:04d}.png".format(k), frame)
		if k == 99:
			# for now we have the arbitrary condition of stopping after 100 
			# frames.
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
		print 'Could not connect. Exiting'
		raise SystemExit

	logging.info("Successfully instantiated Pafy object from video URL")
	logging.info("Attempting to download video.")

	cwd = os.getcwd()
	preName = toCamelCase(best.title)
	dirName = "/" + preName + "/"
	wdir = cwd + dirName
	movieName = preName + "." + best.extension
	outName = cwd + dirName[1:] + movieName

	files = [x.replace(cwd, '').strip('/') for x in g.glob(cwd + "/*")]
	if preName not in files:
		os.system("mkdir {0}".format(preName))
	else:
		print 'directory exists\n\n'

	files = [x.replace(cwd + dirName, "") for x in g.glob(cwd + dirName + "*")]
	if movieName not in files:
		child = best.download(quiet=False, filepath=outName )
		raise ValueError
	else:
		print 'file already exists ... skipping to conversion'
	logging.info("Naming video: {0}".format(outName))
	logging.info("Attempting to download video.")
	convertToPngs(movieName, preName, wdir)

if __name__ == '__main__':
	main()
