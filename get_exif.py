#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from fractions import Fraction
from PIL import Image
from PIL import ExifTags

class GetExif:
    def __init__(self, img):
        self.exif_data = {}
        self.img = Image.open(img)
        self.getExif()

    def getExif(self):
        info = self.img._getexif()
        
        if info == None:
            return self.exif_data
        
        for key, val in info.items():
            if key in ExifTags.TAGS:
                self.exif_data[ExifTags.TAGS[key]] = val
                
        return self.exif_data
