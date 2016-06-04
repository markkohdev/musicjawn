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

parser.add_argument('--channels', help='The channels to include (r - Red, g - Green, b - Blue)')

parser.add_argument('--algo', help='Who\'s algorithm to use (m - Mark, e- Ethan)')

args = parser.parse_args()


print "Input: {}, Output: {}".format(args.input, args.output)

def major_chord(root):
    return [root, root+4, root+7]

def minor_chord(root):
    return [root, root+3, root+7]

def mark():

    ############################################################################
    # Setup Constants
    ############################################################################
    RED_CHANNEL = 0
    GREEN_CHANNEL = 1
    BLUE_CHANNEL = 2

    if args.channels is None:
        CHANNELS = [RED_CHANNEL,GREEN_CHANNEL,BLUE_CHANNEL]
    else:
        CHANNEL_CODES = {'r': RED_CHANNEL, 'g': GREEN_CHANNEL, 'b': BLUE_CHANNEL}
        CHANNELS = [CHANNEL_CODES[code] for code in args.channels]
    # # CHANNELS = [RED_CHANNEL]
    # CHANNELS = [BLUE_CHANNEL]
    # # CHANNELS = [GREEN_CHANNEL]

    ROOT_NOTE = 60
    MIDI_MIN = 24
    MIDI_MAX = 108
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
    MyMIDI.addTempo(track,time, 113)
    MyMIDI.addTrackName(track,time,"Music Jawns")

    # RED: Chromatic Procussion
    MyMIDI.addProgramChange(track,RED_CHANNEL,time, 10)

    # GREEN: Brass
    MyMIDI.addProgramChange(track,GREEN_CHANNEL,time, 60)

    # BLUE: Brass
    MyMIDI.addProgramChange(track,BLUE_CHANNEL,time, 1)


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
    start_pitch = ROOT_NOTE
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
                pitch = random.randint(MIDI_MIN,MIDI_MAX)

            # Update the previous vars
            prev_pitch = pitch
            prev_val = value

            # duration = math.log(count, random.randint(2,10))
            duration = count
            time = time + 1

            # If we didn't randomize to a rest, add the note
            if random.random() > REST_CHANCE:
                print "P: {}, T: {}, D: {}, V: {}".format(pitch,time,duration,volume)

                # Depending how big the value jump was, use a major chord, minor
                # chord, or single note
                if diff > 5:
                    pitch_set = major_chord(pitch)
                elif diff > 2:
                    pitch_set = minor_chord(pitch)
                else:
                    pitch_set = [pitch]

                for pitch in pitch_set:
                    MyMIDI.addNote(track,
                        channel,
                        pitch,
                        time,
                        duration,
                        volume)
            else:
                print "Resting - {}".format(channel)


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
    ############################################################################
    # Setup Constants
    ############################################################################
    RED_CHANNEL = 0
    BLUE_CHANNEL = 1
    GREEN_CHANNEL = 2

    CHANNELS = [RED_CHANNEL,GREEN_CHANNEL,BLUE_CHANNEL]

    MIDI_MIN = 60
    MIDI_MAX = 96
    RANGE = MIDI_MAX - MIDI_MIN

    MAX_DURATION = 4

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
    MyMIDI.addTrackName(track,time,"Ethan is Better than Mark") #Disclaimer: This is entirely Ethan's opinion
    MyMIDI.addTempo(track,time, 360)


    # MyMIDI.addProgramChange(track,0,time, 65)


    ############################################################################
    # Calculate the things!
    ############################################################################
    # Initialize our time values
    time_values = [0,0,0]
    volume = 100

    # Calculate the running sums for R/G/B
    for pixel in pixel_values:
        for channel in CHANNELS:
            pitch = (pixel[channel] % RANGE) + MIDI_MIN
            duration = pixel[(channel + 1) % 3] % MAX_DURATION

            #Add Note
            print "C: {}, P: {}, T: {}, D: {}, V: {}".format(channel,pitch,time_values[channel],duration,volume)

            MyMIDI.addNote(track,channel,pitch,time_values[channel],duration,volume)

            #Increment Time
            time_values[channel] = time_values[channel] + duration

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


if args.algo is None:
    mark()
    ethan()
elif args.algo.lower() == 'm':
    mark()
elif args.algo.lower() == 'e':
    ethan()