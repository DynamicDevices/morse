import sys
import time
import winsound

CODE = {'A': '.-',     'B': '-...',   'C': '-.-.', 
        'D': '-..',    'E': '.',      'F': '..-.',
        'G': '--.',    'H': '....',   'I': '..',
        'J': '.---',   'K': '-.-',    'L': '.-..',
        'M': '--',     'N': '-.',     'O': '---',
        'P': '.--.',   'Q': '--.-',   'R': '.-.',
        'S': '...',    'T': '-',      'U': '..-',
        'V': '...-',   'W': '.--',    'X': '-..-',
        'Y': '-.--',   'Z': '--..',
        
        '0': '-----',  '1': '.----',  '2': '..---',
        '3': '...--',  '4': '....-',  '5': '.....',
        '6': '-....',  '7': '--...',  '8': '---..',
        '9': '----.' 
        }

FILENAME = "test.txt"

DOT_LENGTH_MS = 50
DASH_LENGTH_MS = 3*DOT_LENGTH_MS
ELEMENT_PAUSE_LENGTH_MS = DOT_LENGTH_MS
CHARACTER_PAUSE_LENGTH_MS = 3*DOT_LENGTH_MS
WORD_PAUSE_LENGTH_MS = 7*DOT_LENGTH_MS

BEEP_DOT_LENGTH_MS = 150
BEEP_DASH_LENGTH_MS = 3*BEEP_DOT_LENGTH_MS

MORSE_FREQUENCY = 750

#
# Finds the appropriate character for a morse string of dots and dashes
# 
def char_for_morse( morse ):
    for k,v in CODE.items():
        if(morse == v):
            return k
    return ""

#
# Writes out a message to a file as a timed sequence of 1 and 0 values corresponding to start of dot/dash
# and end of dot/dash. Timing is hardcoded based on values above
# 
def write_morse( message ):

    time = 1234;
    
    # Open the file
    fwrite = open(FILENAME, "w")
    for char in message:
        # Inter character delay
        time += CHARACTER_PAUSE_LENGTH_MS
        sys.stdout.write(char)
        sys.stdout.flush()
        if char == ' ':           
            time += WORD_PAUSE_LENGTH_MS
        else:
            morse = CODE[char]
#            print(morse)
            for char2 in morse:
                # Write ON
                fwrite.write(str(time) + ",1\n")
                # Do DOT or DASH
                if(char2 == '.'):
               	    winsound.Beep(MORSE_FREQUENCY, BEEP_DOT_LENGTH_MS)
                    time += DOT_LENGTH_MS
                if(char2 == '-'):
               	    winsound.Beep(MORSE_FREQUENCY, BEEP_DASH_LENGTH_MS)
                    time += DASH_LENGTH_MS
                # Write OFF
                fwrite.write(str(time) + ",0\n")
    # All done                
    fwrite.close()

#
# Reads in a series of timed lines 1's and zeroes corresponding to starts and ends of dots and dashes
# Converts each morse string to a letter to recreate a message
#
# note: Need to look at how to deal with different timings on input...
#
def read_morse():
    tstart = -1;
    morsein = ""
    with open(FILENAME) as f:
      for line in f:
        el = line.split(',')
        t = int(el[0])

        # Work out delta
        if(tstart < 0):
            tstart = t
        tdelta = t - tstart;
        tstart = t
        
        v = int(el[1])

#        print(str(tdelta) + "," + str(v))
        
        if(v == 1):
            # Are we 
            # - starting off
            # - after a character
            # - after a word
            if(tdelta >= WORD_PAUSE_LENGTH_MS):
                sys.stdout.write(char_for_morse(morsein))
                sys.stdout.flush()
                morsein = ""
                sys.stdout.write(' ')
                sys.stdout.flush()
            elif(tdelta >= CHARACTER_PAUSE_LENGTH_MS):
                sys.stdout.write(char_for_morse(morsein))
                sys.stdout.flush()
                morsein = ""
#            else:
#                print('*')
        else:
            # Finished a dot or a dash
            if(tdelta >= DASH_LENGTH_MS):
                # Dash
#                print('-')
		winsound.Beep(MORSE_FREQUENCY, BEEP_DASH_LENGTH_MS)
                morsein += '-'
            else:
#                print('.')
		winsound.Beep(MORSE_FREQUENCY, BEEP_DOT_LENGTH_MS)
                morsein += '.'
    sys.stdout.write(char_for_morse(morsein))
    sys.stdout.flush()
    f.close()

print("Morse Encoding/Decoding Test")
print("")

message = "PARIS"
if(len(sys.argv) > 1):
    message = sys.argv[1].upper()

sys.stdout.write("Writing: ")
write_morse(message)

print("")

sys.stdout.write("Reading: ")
read_morse()