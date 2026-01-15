import time
from time import sleep

import bambulabs_api as bl
import os
from dotenv import load_dotenv

load_dotenv()

IP = os.getenv('PRINTER_IP')
SERIAL = os.getenv('PRINTER_SERIAL')
ACCESS_CODE = os.getenv('PRINTER_ACCESS_CODE')

MORSE_CODE = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..', '0': '-----', '1': '.----', '2': '..---',
    '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...',
    '8': '---..', '9': '----.', ' ': ' '
}

# Timing (in seconds) - made very obvious for non-morse readers
DOT_TIME = 0.3  # Short flash
DASH_TIME = 1.0  # Long flash (3x dot)
SYMBOL_GAP = 0.4  # Gap between dots/dashes in same letter
LETTER_GAP = 1.5  # Gap between letters (obvious pause)
WORD_GAP = 3.0  # Gap between words (very obvious pause)

if __name__ == '__main__':
    print('Starting bambulabs_api example')
    print('Connecting to Bambulabs 3D printer')
    print(f'IP: {IP}')
    print(f'Serial: {SERIAL}')
    print(f'Access Code: {ACCESS_CODE}')

    # Create a new instance of the API
    printer = bl.Printer(IP, ACCESS_CODE, SERIAL)

    # Connect to the Bambulabs 3D printer
    printer.connect()
    time.sleep(5)

    def flash_morse(message):
        """Flash a message in morse code with very obvious timing patterns"""

        print(f"Flashing message: '{message}'")
        print("Pattern guide: . = short flash, - = long flash\n")

        message = message.upper()

        for i, char in enumerate(message):
            if char == ' ':
                # Word space - already have letter gap from previous char
                print(f"[WORD SPACE - {WORD_GAP - LETTER_GAP}s pause]")
                time.sleep(WORD_GAP - LETTER_GAP)
                continue

            if char not in MORSE_CODE:
                continue

            morse = MORSE_CODE[char]
            print(f"{char}: {morse}")

            # Flash each symbol in the letter
            for j, symbol in enumerate(morse):
                if symbol == '.':
                    printer.turn_light_on()
                    time.sleep(DOT_TIME)
                    printer.turn_light_off()
                elif symbol == '-':
                    printer.turn_light_on()
                    time.sleep(DASH_TIME)
                    printer.turn_light_off()

                # Gap between symbols in same letter
                if j < len(morse) - 1:
                    time.sleep(SYMBOL_GAP)

            # Gap between letters
            if i < len(message) - 1 and message[i + 1] != ' ':
                time.sleep(LETTER_GAP)
            elif i < len(message) - 1 and message[i + 1] == ' ':
                time.sleep(LETTER_GAP)


    while True:
        flash_morse("SOS")
        sleep(2)