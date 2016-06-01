import argparse
from PIL import Image
import pygame
import pygame.mixer
from time import sleep
from StringIO import StringIO
import math, random

from midiutil.MidiFile import MIDIFile

import january

random.seed()

# Our Constant jawns
# PIXEL_BEATVAL = 1.0/8.0
PIXEL_REPEAT_THRESHOLD = 2

# We gotta parse this ish
parser = argparse.ArgumentParser(description='Take an image and produce a music from it!')
parser.add_argument('input', help='The input image!')

parser.add_argument('--output', help='The output audio file (.midi)')

args = parser.parse_args()


print "Input: {}, Output: {}".format(args.input, args.output)

def mark():

    ############################################################################
    # Setup Constants
    ############################################################################
    RED_CHANNEL = 0
    BLUE_CHANNEL = 1
    GREEN_CHANNEL = 2

    CHANNELS = [RED_CHANNEL,GREEN_CHANNEL,BLUE_CHANNEL]
    # CHANNELS = [RED_CHANNEL]

    MIDI_MIN = 24
    MIDI_MAX = 96
    RANGE = MIDI_MAX - MIDI_MIN

    REST_CHANCE = 0.1

    ############################################################################
    # Image data setup
    ############################################################################
    # Open the image file and read the RGB pixel values into an array
    im = Image.open(args.input, 'r')
    width, height = im.size
    pixel_values = list(im.getdata())
    pixel_values = pixel_values[:1000]


    ############################################################################
    # Setup MIDI Jawns
    ############################################################################
    # Create the MIDIFile Object
    MyMIDI = MIDIFile(1)
    # Add track name and tempo
    track = 0
    time = 0.0
    MyMIDI.addTrackName(track,time,"Music Jawns")
    MyMIDI.addTempo(track,time, 120)


    ############################################################################
    # Calculate the things!
    ############################################################################
    # Initialize our running RGB data values
    prevs = [0,0,0] # Previous R,G, and B values
    prev_lengths = [0,0,0] # Number of previous jawns at those values
    values = [[],[],[]] # When a new value is found, the old value and the count get added here

    # Calculate the running sums for R/G/B
    for pixel in pixel_values:
        for channel in CHANNELS:
            dis_pixel = pixel[channel] % RANGE
            if prevs[channel] == dis_pixel:
                # If this pixel value for the color is equal to
                # the last color, increment the count
                prev_lengths[channel] += 1
            else:
                # Otherwise, store the conut and reset the value
                store = (prevs[channel],prev_lengths[channel])
                values[channel].append(store)
                prevs[channel] = dis_pixel
                prev_lengths[channel] = 0


    # Remove timeless jawns
    for channel in CHANNELS:
        values[channel] = filter(lambda (value,count): count > 0, values[channel])


    # Add a note. addNote expects the following information:
    channel = RED_CHANNEL
    start_pitch = 60
    volume = 100

    for channel in CHANNELS:
        time = 0.0

        #  Get an iterator and skip the first val
        iterator = iter(values[channel])

        # We change these on each loop
        prev_val = next(iterator)[0]
        prev_pitch = start_pitch

        for (value,count) in values[channel]:
            # Find the current pitch
            diff = value - prev_val
            pitch = prev_pitch + diff

            if pitch < MIDI_MIN or pitch > MIDI_MAX:
                pitch = 60

            # Update the previous vars
            prev_pitch = pitch
            prev_val = value

            duration = count
            time = time + math.log(duration, random.randint(2,10))

            # If we didn't randomize to a rest, add the note
            if random.random() > REST_CHANCE:
                print "P: {}, T: {}, D: {}, V: {}".format(pitch,time,duration,volume)

                MyMIDI.addNote(track,
                    channel,
                    pitch,
                    time,
                    duration,
                    volume)


    # print values
    # import ipdb; ipdb.set_trace()

    # Also write it to memory
    memFile = StringIO()
    MyMIDI.writeFile(memFile)

    # Use pygame to play the midi that we stored in memory (in memFile)
    pygame.init()
    pygame.mixer.init()
    memFile.seek(0)  # THIS IS CRITICAL, OTHERWISE YOU GET THAT ERROR!
    pygame.mixer.music.load(memFile)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        sleep(1)



def ethan():
    # Ethan do your shit here
    print "I am Ethan"


mark()
