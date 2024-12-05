'''Simple string to morse code converter'''
import sys
from morse_dictionary import MORSE_TRANSLATOR

if len(sys.argv) != 2:
    print('ERROR. This program expects a single argument containing the text to be converted.')
    sys.exit(1)

INPUT_TEXT = sys.argv[1]

MORSE_CODE = [MORSE_TRANSLATOR[c] for c in INPUT_TEXT.upper() if c in MORSE_TRANSLATOR]
print(' '.join(MORSE_CODE))
