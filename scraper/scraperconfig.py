import sys, os
import cv2
import cv2.cv as cv
import numpy as np


class ScraperConfig ( object ):
	def __init__ ( self ):
		pass

	def set_image_file ( self, f ):
		self.img_cv2 = cv2.imread(f)

	def set_selected_rect ( self, rect ):
		self.selected_rect = rect

	def get_selected_region ( self ):
		(x0, y0, x1, y1) = self.selected_rect
		sub = self.img_cv2[y0:y1, x0:x1, :]
		return sub
