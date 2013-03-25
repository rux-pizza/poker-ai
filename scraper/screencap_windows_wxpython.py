import wx #Requieres wxPython
import numpy as np

#Burf c'est tout moche : on blit un tableau on convertie en bmp puis on reconvertie en bmp
#il y a une global toute moche aussi

app = None

def wxImagetoNumpyArray ( Iwx, is_rgb=True ):
    w, h = Iwx.GetSize()
    Inp_flat = np.frombuffer(Iwx.GetDataBuffer(), dtype='uint8')
    if is_rgb:
        Inp = Inp_flat.reshape(h,w,3)
    else:
        Inp = Inp_flat.reshape(h,w)
    return Inp

def wxBitmap2np(wxBmp, is_rgb=True):
    """ Converts wxBitmap to numpy array """
    # TODO: I believe all wxBitmaps are implicitly RGB, so, the
    #       IS_RGB argument may be unnecessary (it currently isn't even
    #       handled right now...)
    w, h = wxBmp.GetSize()
    npimg = np.zeros(h*w*3, dtype='uint8')
    wxBmp.CopyToBuffer(npimg, format=wx.BitmapBufferFormat_RGB)
    npimg = npimg.reshape(h,w,3)
    return npimg
	
class ScreenCapture ( ):
	def __init__ ( self ):
		global app
		if not app:
			app = wx.App(False)
	
	def capture ( self, region = None ):
		#Some init : we need the app to be alive for the script to work
		
		# A wx.ScreenDC provides access to the entire Desktop.
		scrDC = wx.ScreenDC()
		scrDcSize = scrDC.Size
		scrDcSizeX, scrDcSizeY = scrDcSize
		
		scrDcBmap = scrDC.GetAsBitmap()
		scrDcBmapSize = scrDcBmap.GetSize()
		
		# Check if scrDC.GetAsBitmap() method has been implemented on this platform.
		if not scrDcBmap.IsOk() : # Not implemented :  Get the screen bitmap the long way.
			
			# Create a new empty (black) destination bitmap the size of the scrDC.
			scrDcBmap = wx.EmptyBitmap(*scrDcSize)    # Overwrire the invalid original assignment.
			scrDcBmapSizeX, scrDcBmapSizeY = scrDcSize
			
			# Create a DC tool that is associated with scrDcBmap.
			memDC = wx.MemoryDC(scrDcBmap)
			
			# Copy (blit, "Block Level Transfer") a portion of the screen bitmap
			#   into the returned capture bitmap.
			# The bitmap associated with memDC (scrDcBmap) is the blit destination.
			
			memDC.Blit(0, 0,# Copy to this start coordinate.
				scrDcBmapSizeX, scrDcBmapSizeY,# Copy an area this size.
				scrDC,# Copy from this DC's bitmap.
				0, 0)# Copy from this start coordinate.
			
			memDC.SelectObject(wx.NullBitmap)     # Finish using this wx.MemoryDC.
			
		else : # This platform has scrDC.GetAsBitmap() implemented.
			scrDcBmap = scrDC.GetAsBitmap()
		
		return wxBitmap2np(scrDcBmap)

#Some awfullstuff to save the image
def savePNG ( img, path ):
	img.SaveFile(path, wx.BITMAP_TYPE_PNG)

	
if __name__ == "__main__":
	savePNG(getImgFromScreenshot(),"test.png")