import sys, os
import cv2
import cv2.cv as cv
import numpy as np


class ScraperConfig ( object ):
	def __init__ ( self ):
		pass

	def set_image ( self, f ):
		self.img = cv2.imread(f, cv.CV_LOAD_IMAGE_GRAYSCALE)
		
	def set_region ( self, coords ):
		self.coords = coords

	def get_region ( self ):
		(x0, y0, x1, y1) = self.coords
		return self.img[x0:x1,y0:y1]
