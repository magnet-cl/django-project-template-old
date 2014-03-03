# -*- coding: utf-8 -*-
""" Image operations. """

from PIL import Image, ImageFile
from PIL.ImageOps import fit

# standard library
import os


def generate_thumbnail(file_path, size, bounds=None, force=False, img=None):
    """ Fits image to the given size in order to generate its thumbnail.

    Keyword arguments:
    file_path -- absolute path of file
    size -- int tuple, for example (200, 200)

    """
    (thumbnail_path, thumbnail_name) = os.path.split(file_path)
    thumbnail_folder = '{}/{}x{}/'.format(thumbnail_path, size[0], size[1])

    thumbnail_path = '{}{}'.format(thumbnail_folder, thumbnail_name)

    if not os.path.exists(thumbnail_path) or force:
        # allow truncated images
        ImageFile.LOAD_TRUNCATED_IMAGES = True

        if img is None:
            img = Image.open(file_path)

        if bounds:
            img = img.crop(bounds)

        thumbnail = fit(img, size, Image.ANTIALIAS)

        if not os.path.exists(thumbnail_folder):
            os.makedirs(thumbnail_folder)

        thumbnail.save(thumbnail_path)
