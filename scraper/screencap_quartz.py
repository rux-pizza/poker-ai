import time
import struct
import numpy as np

import Quartz.CoreGraphics as CG


class ScreenCapture ( object ):
    """Screen Capture using Mac OS Quartz CoreGraphics
    """

    def capture ( self, region = None ):
        """region should be a CGRect, something like:

        >>> import Quartz.CoreGraphics as CG
        >>> region = CG.CGRectMake(0, 0, 100, 100)
        >>> sp = ScreenPixel()
        >>> sp.capture(region=region)

        The default region is CG.CGRectInfinite (captures the full screen)
        """

        if region is None:
            region = CG.CGRectInfinite
        else:
            # TODO: Odd widths cause the image to warp. This is likely
            # caused by offset calculation in ScreenPixel.pixel, and
            # could could modified to allow odd-widths
            if region.size.width % 2 > 0:
                emsg = "Capture region width should be even (was %s)" % (
                    region.size.width)
                raise ValueError(emsg)

        # Create screenshot as CGImage
        image = CG.CGWindowListCreateImage(
            region,
            CG.kCGWindowListOptionOnScreenOnly,
            CG.kCGNullWindowID,
            CG.kCGWindowImageDefault)

        # Intermediate step, get pixel data as CGDataProvider
        prov = CG.CGImageGetDataProvider(image)

        # Copy data out of CGDataProvider, becomes string of bytes
        self._data = CG.CGDataProviderCopyData(prov)

        # Get width/height of image
        self.width = CG.CGImageGetWidth(image)
        self.height = CG.CGImageGetHeight(image)

        array = np.frombuffer(self._data,'B')
        array = array.reshape([self.height, self.width, -1])
        array = array[:,:,0:3]
        array = array.copy() # DEBUG ?
        self.array = array
        
        return array

    def get_region ( self, coords ):
        (x0, y0, x1, y1) = coords
        return self.array[x0:x1, y0:y1]
        
    def pixel ( self, x, y ):
        data_format = "BBBB"
        offset = 4 * ((self.width*int(round(y))) + int(round(x)))
        b, g, r, a = struct.unpack_from(data_format, self._data, offset=offset)
        return (r, g, b, a)

    
if __name__ == '__main__':
    import cv2
    
    sc = ScreenCapture()
    a = sc.capture()
    cv2.imwrite('screenshot.tiff', a)
