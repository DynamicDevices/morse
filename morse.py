import webrepl
import sys
import utime
import time
import ubinascii
import machine
from umqtt.simple import MQTTClient

CONFIG = {
    "broker": "nodered.dynamicdevices.co.uk",
    "sensor_pin": 0, 
    "client_id": b"esp8266_" + ubinascii.hexlify(machine.unique_id()),
    "topic": "morsetweeter",
}

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

client = None

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

    time = 0;
    
    # Open the file
    fwrite = open(FILENAME, "w")
    for char in message:
        # Inter character delay
        time += CHARACTER_PAUSE_LENGTH_MS
        print(str(time) + " " + char)
        if char == ' ':           
            print(' ')
            time += WORD_PAUSE_LENGTH_MS
        else:
            morse = CODE[char]
            for char2 in morse:
                # Write ON
                fwrite.write(str(time) + ",1\n")
                # Do DOT or DASH
                if(char2 == '.'):
                    time += DOT_LENGTH_MS
                if(char2 == '-'):
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
    message = ""
    morsein = ""
    with open(FILENAME) as f:
      for line in f:
#        print(line)
        el = line.split(',')
        t = int(el[0])
        
        # Work out delta
        if(tstart < 0):
            tstart = t
        tdelta = utime.ticks_diff(t, tstart)
        tstart = t
        
        v = int(el[1])

#        print(str(tdelta) + "," + str(v))
        
        if(v == 1):
            # Are we 
            # - starting off
            # - after a character
            # - after a word
            if(tdelta >= WORD_PAUSE_LENGTH_MS):
                print(char_for_morse(morsein))
                morsein = ""
                print(' ')
                message += ' '
            elif(tdelta >= CHARACTER_PAUSE_LENGTH_MS):
                print(char_for_morse(morsein))
                message += char_for_morse(morsein)
                morsein = ""
        else:
            # Finished a dot or a dash
            if(tdelta >= DASH_LENGTH_MS):
                # Dash
#                print('-')
                morsein += '-'
            else:
#                print('.')
                morsein += '.'
    print(char_for_morse(morsein))
    message += char_for_morse(morsein)
    f.close()
    return message

def main():

    print("Writing")
    write_morse("PARIS")

    print("")

    print("Reading")
    message = read_morse()
    print("Got: " + message)

    print("Connecting")
    client = MQTTClient(CONFIG['client_id'], CONFIG['broker'])
    client.connect()
    print("Connected to {}".format(CONFIG['broker']))
    
    print("Publishing to {}".format(CONFIG['topic']))
    datastr = "ts=" + str(utime.ticks_ms()) + "&val=" + message
    client.publish('{}/{}'.format(CONFIG['topic'],
                                        CONFIG['client_id']),
                                        bytes(datastr, 'utf-8'))
    client.disconnect()

if __name__ == '__main__':
    main()
