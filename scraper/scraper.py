import sys, os
import numpy as np
import cv2, tesseract
import cv2.cv as cv


class Scraper ( object ):
	def __init__ ( self ):
		self.Corr = cv.CV_TM_CCORR_NORMED
		self.MinCorr = 0.97

		path = os.path.join(os.path.dirname(__file__), 'templates')
		self.SuitTemplates = dict()
		for suit in ['h','d','c','s']:
			template = cv2.imread(path+'/suits/'+suit+'.png')
			if template==None:
				raise Exception('Template for suit %s not found\n' % suit)

			self.SuitTemplates[suit] = template

		self.NumTemplates = dict()
		for num in xrange(1,13+1):
			template = cv2.imread(path+'/numbers/%d.png' % num)
			if template==None:
				raise Exception('Template for number %d not found\n' % num)

			self.NumTemplates[num] = template

		# tesseract
		if True:
			self.ocr_api = tesseract.TessBaseAPI()
			self.ocr_api.Init(".","eng",tesseract.OEM_DEFAULT)
			self.ocr_api.SetPageSegMode(tesseract.PSM_AUTO)

	def locate ( self, table, template ):
		corrs = cv2.matchTemplate(table, template, self.Corr)
		_, max_corr, _, loc = cv2.minMaxLoc(corrs)

		if max_corr < self.MinCorr:
			raise Exception('template not found (max coor %f)\n' % max_corr)

		return loc

	def findPlayerLoc ( self, table, pseudo ):
		template = cv2.imread('pseudos/'+pseudo+'.png')
		if template==None:
			raise Exception('template file for pseudo %s non found\n' % pseudo)

		return locate(table, template)

	def findBestMatch ( self, canvas, templates, color=True ):
		bestCorr = 0
		best = -1

		if color:
			source = canvas
		else:
			source = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)

		for (i, templ) in templates.items():
			if color:
				template = templ
			else:
				template = cv2.cvtColor(templ, cv2.COLOR_BGR2GRAY)

			corrs = cv2.matchTemplate(source, template, self.Corr)
			c = corrs.max(axis=None)
			if c > bestCorr:
				bestCorr = c
				best = i

		if bestCorr < self.MinCorr:
			if True: ##debug
				print 'no best match found (best corr %f)\n' % bestCorr
				print templates.keys()
				print 'waiting key on image...\n'
				cv2.imshow('canvas',source)
				cv2.waitKey(0)
				cv2.destroyAllWindows()

			raise Exception('no best match found (best corr %f)\n' % bestCorr)

		return best

			
	def findPlayerCards ( self, table, pseudo ):
		yr = 32 # y range search
		ext = 4 # add padding to be more robust

		# get player location
		pLoc = self.findPlayerLoc(table, pseudo)
		x = pLoc[0]
		y = pLoc[1]

		# boundaries for searching suits and numbers
		s1_x0 = x-ext; s1_x1 = x+32+ext; s1_y0 = y-32-yr-ext; s1_y1 = y+ext;
		s2_x0 = x+96-ext; s2_x1 = x+96+32+ext; s2_y0 = y-32-yr-ext; s2_y1 = y+ext;
		n1_x0 = x-ext; n1_x1 = x+32+ext; n1_y0 = y-64-yr-ext; n1_y1 = y-32+ext;
		n2_x0 = x+96-ext; n2_x1 = x+96+32+ext; n2_y0 = y-64-yr-ext; n2_y1 = y-32+ext;
		
		# search
		suit1 = self.findBestMatch(table[s1_y0:s1_y1, s1_x0:s1_x1, :], self.SuitTemplates)
		suit2 = self.findBestMatch(table[s2_y0:s2_y1, s2_x0:s2_x1, :], self.SuitTemplates)
		num1 = self.findBestMatch(table[n1_y0:n1_y1, n1_x0:n1_x1, :], self.NumTemplates, False)
		num2 = self.findBestMatch(table[n2_y0:n2_y1, n2_x0:n2_x1, :], self.NumTemplates, False)

		return [ (num1,suit1), (num2,suit2) ]
	

	def do_ocr ( self, cv2_img ):
		h, w, c = cv2_img.shape
		cv_img = cv.CreateImageHeader((w,h), cv.IPL_DEPTH_8U, c)
		cv.SetData(cv_img, cv2_img.tostring(), cv2_img.dtype.itemsize * c * w)
		#
		tesseract.SetCvImage(cv_img, self.ocr_api)
		text = self.ocr_api.GetUTF8Text()
		#
		return text
	
if __name__ == '__main__':
	try:
		table = cv2.imread(sys.argv[1])
	except:
		table = cv2.imread('screen1.png')

	s = Scraper()
	c = s.findPlayerCards(table, 'm1lo0u')
	
	print c
