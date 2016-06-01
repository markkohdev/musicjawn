import argparse
from PIL import Image

# Our Constant jawns
# PIXEL_BEATVAL = 1.0/8.0
PIXEL_REPEAT_THRESHOLD = 2

# We gotta parse this ish
parser = argparse.ArgumentParser(description='Take an image and produce a music from it!')
parser.add_argument('image', help='The input image!')

parser.add_argument('output_file', help='The output audio file (.wav)')

args = parser.parse_args()


print "Input: {}, Output: {}".format(args.image, args.output_file)

# Open the image file and read the RGB pixel values into an array
im = Image.open(args.image, 'r')
width, height = im.size
pixel_values = list(im.getdata())


def mark():
    prevs = [0,0,0] # Previous R,G, and B values
    prev_lengths = [0,0,0] # Number of previous jawns at those values
    values = [[],[],[]] # When a new value is found, the old value and the count get added here

    for pixel in pixel_values:
        for v in range(0,3):
            if prevs[v] == pixel[v]:
                # If this pixel value for the color is equal to
                # the last color, increment the count
                prev_lengths[v] += 1
            else:
                # Otherwise, store the conut and reset the value
                store = (prevs[v],prev_lengths[v])
                values[v].append(store)
                prevs[v] = pixel[v]
                prev_lengths[v] = 0


    # print values
    import ipdb; ipdb.set_trace()


def ethan():
    # Ethan do your shit here
    print "I am Ethan"
