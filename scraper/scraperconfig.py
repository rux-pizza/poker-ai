import sys, os
import cv2
import numpy as np


class ScraperConfig ( object ):
	def __init__ ( self ):
		pass

	def set_image ( self, f ):
		self.img = cv2.imread(f)
		
	def set_region ( self, coords ):
		self.coords = coords

	def get_region ( self ):
		(x0, y0, x1, y1) = self.coords
		return self.img[x0:x1,y0:y1]
