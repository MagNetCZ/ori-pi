#!/usr/bin/env python

import urllib
import threading
import time
import json
import opc

settings_url = "http://localhost:80/ori/settings.json"

program = 0
program_dirty = True

update_delay = 5

class SetupThread( threading.Thread ):
    def run( self ):
        while (True):
            global program, program_dirty
            
            response = urllib.urlopen( settings_url )
            json_obj = json.loads(response.read())

            last_program = program
            program = json_obj['program']
            if (program != last_program):
                program_dirty = True
                print 'Program changed to ' + str(program)

            threading.Event().wait(update_delay)

def led_strobe(delay):
    numLEDs = 50
    client = opc.Client('192.168.222.130:7890')

    black = [ (0,0,0) ] * numLEDs
    white = [ (255,255,255) ] * numLEDs

    global program_dirty

    while not program_dirty:
        client.put_pixels(white)
        time.sleep(delay)
        client.put_pixels(black)
        time.sleep(delay)

def led_strobe_slow():
    led_strobe(0.3)

def led_strobe_fast():
    led_strobe(0.05)

class LEDThread( threading.Thread ):
    def run( self ):
        global program_dirty, program
        programs = [ led_strobe_slow, led_strobe_fast ]

        while True:
            program_dirty = False
            programs[program % len(programs)]()

setupThread = SetupThread()
setupThread.daemon = True

ledThread = LEDThread()
ledThread.daemon = True
                        
#setupThread.start()
ledThread.start()
