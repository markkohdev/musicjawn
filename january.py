# MUSIC THINGSS!!!
# This is the January.cc library translated into python
# Rich Vreeland is a dope music-man!  Mark Koh is a dope college kid who likes
# catching snowflakes on his tounge!
#
# This code was originally written in ActionScript (Flash - blech!)
# It is now in parseltounge (Python)
#
# Actionjawns at
# https://github.com/richvreeland/january
#

################################################################################
# Some Constants
################################################################################

# IONIAN LOGIC
IONIAN =    [
                ["two1", "thr1", "fiv1", "two2", "thr2"],
                ["fiv1", "sev1"],
                ["fiv1", "sev1", "one1"],
                ["thr1", "fiv1", "one2"],
                ["one1", "thr1", "for1", "six1", "sev1", "one2", "two2", "thr2"],
                ["one1", "fiv1", "sev1", "one2", "thr2", "for2"],
                ["fiv1", "one2", "thr2"],
                ["one1", "thr1", "two2", "thr2", "fiv2", "thr3", "sev2", "sev1", "six1"],
                ["one2", "thr2", "fiv2", "sev2"],
                ["two2", "for2", "fiv2", "sev2", "one3", "one2", "six1", "fiv1"],
                ["thr2", "fiv2", "one3", "six1"],
                ["one2", "thr2", "for2", "six2", "sev2", "thr3", "sev2", "sev3", "two3"],
                ["one2", "fiv2", "sev2", "one3"],
                ["fiv2", "one3"],
                ["one2", "two3", "thr3", "fiv3", "thr2", "for2", "sev2", "six2"],
                ["one3", "thr3", "fiv3", "sev3"],
                ["fiv2", "two3", "for3", "fiv3", "sev3", "one3"],
                ["thr3", "fiv3", "one4"],
                ["one3", "thr3", "for3", "six3", "sev3", "one4"],
                ["one3", "fiv3", "sev3", "one4"],
                ["fiv3", "one4"],
                ["one2", "thr3", "for3", "fiv3", "sev3", "one3"],
                ["one2", "one3"]
            ]

IONIAN_CHORDS = [
                    ["one1", "thr1", "fiv1"], ["one1", "thr1", "sev1"], ["one1", "fiv1", "one2"], ["one1", "fiv1", "thr2"],
                    ["one1", "fiv1", "fiv2"], ["one1", "thr2", "sev2"], ["thr1", "one2", "fiv2"], ["thr1", "fiv1", "one2"],
                    ["fiv1", "one2", "thr2"], ["one2", "two2", "sev2"], ["one1", "two2", "sev2"], ["one1", "fiv1", "thr2", "sev2"]
                ]

DATABASE = ["one1", "two1", "thr1", "for1", "fiv1", "six1", "sev1", "one2", "two2", "thr2", "for2", "fiv2", "six2", "sev2", "one3", "two3", "thr3", "for3", "fiv3", "six3", "sev3", "one4"]
INVERSE_DATABASE = {string: index for (index, string) in enumerate(["one1", "two1", "thr1", "for1", "fiv1", "six1", "sev1", "one2", "two2", "thr2", "for2", "fiv2", "six2", "sev2", "one3", "two3", "thr3", "for3", "fiv3", "six3", "sev3", "one4"]) }


MAJOR_POS = 1
MINOR_POS = 3

KEY_CUTOFF = 48



################################################################################
# Intervals
# https://github.com/richvreeland/january/blob/master/src/january/music/Intervals.as
################################################################################

class Intervals:

    # A list of shorthand lookups so Rich could write things out naturally?
    

    # Whether the Intervals.loadout object is up to date or not.
    updated = False

    # The intervals object, populated with the notes of the current key, ordered by the current mode.
    loadout = {}

    @staticmethod
    def populate():
        if  not updated:
            if Key.current == "C Minor":
                modeOffset = Mode.DATABASE[Mode.index].minorPos
            else:
                modeOffset = Mode.DATABASE[Mode.index].majorPos

        for i in range(0, len(DATABASE)):
            loudout[DATABASE[i]] = Key.DATABASE[Key.index][i + modeOffset]

        updated = True


