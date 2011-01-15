#!/usr/bin/env python

"""
This program assists with cutting down large images into square tiles.  It can
take an image of arbitrary size and create tiles of any size.

python tilemaker.py -s256 -Q9 -t"tile-%d-%d-%d.png" -bFFFFFF -v canvas.png

Copyright, 2005-2006: Michal Migurski, Serge Wroclawski
License: Apache 2.0
"""

import math
from os.path import split, splitext
from PIL import Image

chatty_default = False
background_default = "FFFFFF"
efficient_default = True
scaling_filter = Image.BICUBIC

from sys import exit

def main():
    """Main method"""
    from optparse import OptionParser
    
    parser = OptionParser(usage = "usage: %prog [options] filename")
    # Now, Dan wants tile height and width.
    parser.add_option('-s', '--tile-size', dest = "size", type="int",
                      default=512, help = 'The tile height/width')
    parser.add_option('-t', '--template', dest = "template",
                      default = None,
                      help = "Template filename pattern")
    parser.add_option('-v', '--verbose', dest = "verbosity",
                      action = "store_true", default = False,
                      help = "Increase verbosity")
    parser.add_option('-Q', '--quality', dest="quality", type="int",
                      help = 'Set the quality level of the image')
    parser.add_option('-b', '--background', dest="background",
                      help = 'Set the background color')
    
    # Location based arguments are always a pain
    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("incorrect number of arguments")
    filename = args[0]
    if not options.template:
        fname, extension = splitext(split(filename)[1])
        options.template = fname + '-%d-%d-%d' + extension
    if not options.background:
        options.background = background_default

    verbosity = options.verbosity
    size = options.size
    quality = options.quality
    template = options.template
    background = options.background
    
    # Split the image up into "squares"
    img = prepare(filename, bgcolor = background, chatty = verbosity)

    subdivide(img, size = (size, size),
              quality = quality, filename = template, chatty = verbosity)


def prepare(filename, bgcolor = background_default, chatty = chatty_default):
    """
    Prepare a large image for tiling.
    
    Load an image from a file. Resize the image so that it is square,
    with dimensions that are an even power of two in length (e.g. 512,
    1024, 2048, ...). Then, return it.
    """

    src = Image.open(filename)

    if chatty:
        print "original size: %s" % str(src.size)
    
    full_size = (1, 1)

    while full_size[0] < src.size[0] or full_size[1] < src.size[1]:
        full_size = (full_size[0] * 2, full_size[1] * 2)
    
    img = Image.new('RGBA', full_size)
    img.paste("#" + bgcolor)
    
    src.thumbnail(full_size, scaling_filter)
    img.paste(src, (int((full_size[0] - src.size[0]) / 2),
                    int((full_size[1] - src.size[1]) / 2)))
    
    if chatty:
        print "full size: %s" % str(full_size)
        
    return img



def tile(im, level, quadrant=(0, 0), size=(512, 512),
         efficient=efficient_default, chatty=chatty_default):
    """
    Extract a single tile from a larger image.
    
    Given an image, a zoom level (int), a quadrant (column, row tuple;
    ints), and an output size, crop and size a portion of the larger
    image. If the given zoom level would result in scaling the image up,
    throw an error - no need to create information where none exists.
    """

    scale = int(math.pow(2, level))
    
    if efficient:
        #efficient: crop out the area of interest first, then scale and copy it

        inverse_size    = (float(im.size[0]) / float(size[0] * scale),
                           float(im.size[1]) / float(size[1] * scale))
        top_left        = (int(quadrant[0] *  size[0] * inverse_size[0]),
                           int(quadrant[1] *  size[1] * inverse_size[1]))
        bottom_right    = (int(top_left[0] + (size[0] * inverse_size[0])),
                           int(top_left[1] + (size[1] * inverse_size[1])))
    
        if inverse_size[0] < 1.0 or inverse_size[1] < 1.0:
            raise Exception('Requested zoom level (%d) is too high' % level)
    
        if chatty:
            print "crop(%s).resize(%s)" % (str(top_left + bottom_right),
                                           str(size))

        zoomed = im.crop(top_left + bottom_right).resize(size, scaling_filter).copy()
        return zoomed

    else:
        # inefficient: copy the whole image, scale it and then crop
        # out the area of interest

        new_size        = (size[0] * scale,         size[1] * scale)
        top_left        = (quadrant[0] * size[0],   quadrant[1] * size[1])
        bottom_right    = (top_left[0] + size[0],   top_left[1] + size[1])
        
        if new_size[0] > im.size[0] or new_size[1] > im.size[1]:
            raise Exception('Requested zoom level (%d) is too high' % level)
    
        if chatty:
            print "resize(%s).crop(%s)" % (str(new_size),
                                           str(top_left + bottom_right))

        zoomed = im.copy().resize(new_size, scaling_filter).crop(top_left + bottom_right).copy()
        return zoomed



def subdivide(img, level=0, quadrant=(0, 0), size=(512, 512),
              filename='tile-%d-%d-%d.jpg',
              quality = None, chatty = chatty_default):
    """
    Recursively subdivide a large image into small tiles.

    Given an image, a zoom level (int), a quadrant (column, row tuple;
    ints), and an output size, cut the image into even quarters and
    recursively subdivide each, then generate a combined tile from the
    resulting subdivisions. If further subdivision would result in
    scaling the image up, use tile() to turn the image itself into a
    tile.
    """

    if img.size[0] <= size[0] * math.pow(2, level):

        # looks like we've reached the bottom - the image can't be
        # subdivided further. # extract a tile from the passed image.
        out_img = tile(img, level, quadrant=quadrant, size=size)
        out_img.save(filename % (level, quadrant[0], quadrant[1]))

        if chatty:
            print '.', '  ' * level, filename % (level, quadrant[0], quadrant[1])
        return out_img

    # haven't reach the bottom.
    # subdivide deeper, construct the current image out of deeper images.
    out_img = Image.new('RGBA', (size[0] * 2, size[1] * 2))
    out_img.paste(subdivide(img = img,
                            level = (level + 1),
                            quadrant=((quadrant[0] * 2) + 0,
                                      (quadrant[1] * 2) + 0),
                            size = size,
                            filename=filename, chatty=chatty), (0,0))
    out_img.paste(subdivide(img = img,
                            level=(level + 1),
                            quadrant=((quadrant[0] * 2) + 0,
                                      (quadrant[1] * 2) + 1),
                            size = size,
                            filename=filename, chatty=chatty), (0,size[1]))
    out_img.paste(subdivide(img = img,
                            level=(level + 1),
                            quadrant=((quadrant[0] * 2) + 1,
                                      (quadrant[1] * 2) + 0),
                            size = size,
                            filename=filename, chatty=chatty), (size[0], 0))
    out_img.paste(subdivide(img,
                            level=(level + 1),
                            quadrant=((quadrant[0] * 2) + 1,
                                      (quadrant[1] * 2) + 1),
                            size = size,
                            filename=filename, chatty=chatty), (size[0], size[1]))

    out_img = out_img.resize(size, scaling_filter)

    # In the future, we may want to verify the quality. Right now we let
    # the underlying code handle bad values (other than a non-int)
    if not quality:
        out_img.save(filename % (level, quadrant[0], quadrant[1]))
    else:
        out_img.save(filename % (level, quadrant[0], quadrant[1]),
                     quality=quality)
    if chatty:
        print '-', '  ' * level, filename % (level, quadrant[0], quadrant[1])
    return out_img



if __name__ == '__main__':
    exit(main())
