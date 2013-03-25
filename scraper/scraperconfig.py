import sys, os
import cv2.cv as cv
import numpy as np


class ScraperConfig ( object ):
	def __init__ ( self ):
		pass

	def set_image ( self, f ):
		self.img = cv.LoadImage(f, cv.CV_LOAD_IMAGE_GRAYSCALE)
		
	def set_region ( self, coords ):
		self.coords = coords

	def get_region ( self ):
		(x0, y0, x1, y1) = self.coords
		rect = (int(x0), int(y0), int(x1-x0), int(y1-y0))
		return cv.GetSubRect(self.img, rect)
