import argparse
from PIL import Image
import pygame
import pygame.mixer
from time import sleep
from StringIO import StringIO

from midiutil.MidiFile import MIDIFile

# Our Constant jawns
# PIXEL_BEATVAL = 1.0/8.0
PIXEL_REPEAT_THRESHOLD = 2

# We gotta parse this ish
parser = argparse.ArgumentParser(description='Take an image and produce a music from it!')
parser.add_argument('image', help='The input image!')

parser.add_argument('output', help='The output audio file (.wav)')

args = parser.parse_args()


print "Input: {}, Output: {}".format(args.image, args.output)

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



# Create the MIDIFile Object
memFile = StringIO()
MyMIDI = MIDIFile(1)
# Add track name and tempo. The first argument to addTrackName and
# addTempo is the time to write the event.
track = 0
time = 0
MyMIDI.addTrackName(track,time,"Sample Track")
MyMIDI.addTempo(track,time, 120)

# Add a note. addNote expects the following information:
channel = 0
base = 60
duration = 3
volume = 100


# Now add the note.
# for pitch in range(0,3):
MyMIDI.addNote(track,channel,60,0,duration,volume)
MyMIDI.addNote(track,channel,64,0,duration,volume)
MyMIDI.addNote(track,channel,67,0,duration,volume)


MyMIDI.addNote(track,channel,60,3,duration,volume)
MyMIDI.addNote(track,channel,65,3,duration,volume)
MyMIDI.addNote(track,channel,69,3,duration,volume)


# And write it to disk (so we can save it if we wanna)
binfile = open(args.output, 'wb')
MyMIDI.writeFile(binfile)
binfile.close()

# Also write it to memory
MyMIDI.writeFile(memFile)


# Use pygame to play the midi that we stored in memory (in memFile)
pygame.init()
pygame.mixer.init()
memFile.seek(0)  # THIS IS CRITICAL, OTHERWISE YOU GET THAT ERROR!
pygame.mixer.music.load(memFile)
pygame.mixer.music.play()
while pygame.mixer.music.get_busy():
    sleep(1)
