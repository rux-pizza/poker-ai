import sys, os, cPickle, copy
import cv2
import cv2.cv as cv
import numpy as np
from pattern import Pattern


class ScraperConfig ( object ):
	def __init__ ( self ):
		self.list_markers = {}
		self.filename = None
		self.imagename = None

	def save ( self, fn=None ):
		if not fn:
			fn = self.filename
		#
		tosave = copy.deepcopy(self)
		tosave.img_cv2 = None
		#
		f = open(fn, 'wb')
		cPickle.dump(tosave, f)
		f.close()

	@staticmethod
	def load ( fn ):
		f = open(fn, 'rb')
		o = cPickle.load(f)
		f.close()
		return o
	
	def set_image_file ( self, f ):
		self.imagename = f
		self.img_cv2 = cv2.imread(f)

	def new_pattern ( self ):
		self.pattern = Pattern()

	def get_pattern ( self ):
		return self.pattern

	def select_rect ( self, rect ):
		self.pattern.rect = rect
	
	def get_list_markers ( self ):
		return list(self.list_markers)

	def add_marker ( self, marker_name ):
		self.pattern.name = marker_name
		self.create_pattern_image()
		self.list_markers[marker_name] = self.pattern
		
	def switch_marker ( self, marker_name ):
		self.pattern = self.list_markers[marker_name]
		return self.pattern

	def rename_marker ( self, old, new ):
		marker = self.list_markers[old]
		marker.name = new
		self.list_markers[new] = marker
		self.list_markers[old]

	def create_pattern_image ( self ):
		(x0, y0, x1, y1) = self.pattern.rect
		sub = self.img_cv2[y0:y1, x0:x1, :]
		self.pattern.img_cv2 = sub
		return sub
	
		
