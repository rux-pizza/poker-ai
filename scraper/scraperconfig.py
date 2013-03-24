import sys, os
import numpy as np


class ScraperConfig ( object ):
    def __init__ ( self ):
        pass

    def set_region ( self, img, coords ):
        self.coords = coords
        self.img = img

    def get_region ( self ):
        return self.img
