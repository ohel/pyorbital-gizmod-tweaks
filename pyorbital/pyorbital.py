#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, socket, select, time
from unidecode import unidecode

SOCKET_PATH = "/dev/shm/pyorbital"
LCD_DEVICE = "/dev/serial/matrix_orbital"
UPDATE_INTERVAL = 0.15

if os.path.exists(SOCKET_PATH):
    os.remove(SOCKET_PATH)
receivesocket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
receivesocket.bind(SOCKET_PATH)
receivesocket.setblocking(1)
fo_receivesocket = receivesocket.makefile('r', 1)

lcdout = open(LCD_DEVICE, 'w')
# ready horizontal bars, empty screen and reset position
lcdout.write("\xFE\x68\xFEX\xFE\x48\n")

wait_time = 0
last_time = 0
np_artist = ""
np_title = ""
np_album = ""
np_track = ""
np_disc = ""
last_command = ""
scroll_counter_artist = 0
scroll_counter_title = 0
stopped = True
phase = 0

while True:

    incoming = select.select([receivesocket], [], [], UPDATE_INTERVAL)
    if incoming[0]:
        data = fo_receivesocket.readline()
        last_time = time.time()
        command = data.split()[0]
        data = data[len(command)+1:]

        if command == "paused":
            stopped = True
            lcdout.write("\xFEX\xFE\x48\xFE\x47\x06\x01Quod Libet\xFE\x47\x06\x02* paused *\n")
        elif command == "stop":
            stopped = True
            lcdout.write("\xFEX\xFE\x48\xFE\x47\x06\x01Quod Libet\xFE\x47\x06\x02* stopped *\n")
        elif command == "quit":
            stopped = True
            # backlight off
            lcdout.write("\xFEX\xFE\x48\xFE\x46\n")
        elif command == "unpaused":
            stopped = False
            wait_time = 0
            # backlight on
            lcdout.write("\xFE\x42\x00\n")
        elif command == "seek" and not stopped:
            if last_command == "seek":
                lcdout.write("\xFE\x7C\x01\x02\x00" + chr(int(round (100*float(data)))) + "\n")
            else:
                lcdout.write("\xFEH     Seeking...     \xFE\x7C\x01\x02\x00" + chr(int(round (100*float(data)))) + "\n")
            wait_time = 0.5
        elif command == "volume":
            if last_command == "volume":
                lcdout.write("\xFE\x7C\x01\x02\x00" + chr(int(round (100*float(data[:-1])))) + "\n")
            else:
                lcdout.write("\xFEH       Volume:       \xFE\x7C\x01\x02\x00" + chr(int(round (100*float(data[:-1])))) + "\n")
#            if last_command == "volume":
#                lcdout.write("\xFE\x47\x0e\x02" + data[:-1] + "\n")
#            else:
#                lcdout.write("\xFEX\xFE\x48\xFE\x47\x06\x01Quod Libet\xFE\x47\x04\x02* volume: " + data[:-1] + " *\n")
            wait_time = 0.5
        elif command == "artist":
            stopped = False
#            np_artist = data.replace("ö","\xEF").replace("ä","\xE1")[:-1] + "".ljust(19)
            np_artist = unidecode(unicode(data[:-1],'utf-8')).encode('ascii') + "".ljust(19)
            scroll_counter_artist = len(np_artist) < 40
        elif command == "title":
            stopped = False
#            np_title = data.replace("ö","\xEF").replace("ä","\xE1")[:-1] + "".ljust(19)
            np_title = unidecode(unicode(data[:-1],'utf-8')).encode('ascii') + "".ljust(19)
            scroll_counter_title = len(np_title) < 40
            lcdout.write("\xFE\x42\x00\n")
            wait_time = 0
            phase = 0
        elif command == "album":
            np_album = unidecode(unicode(data[:-1],'utf-8')).encode('ascii')
        elif command == "track":
            np_track = data[:-1]
        elif command == "disc":
            np_disc = data[:-1]
        elif command == "ralbum":
            lcdout.write("\xFEX\xFE\x48\xFE\x47\x06\x01Quod Libet\xFE\x47\x03\x02* random album *\n")
            wait_time = 0.5
        elif command == "order":
            if data[:-1] == "0":
                lcdout.write("\xFEX\xFE\x48\xFE\x47\x06\x01Quod Libet\xFE\x47\x02\x02* order: default *\n")
            else:
                lcdout.write("\xFEX\xFE\x48\xFE\x47\x06\x01Quod Libet\xFE\x47\x02\x02* order: shuffle *\n")
            wait_time = 0.5
        elif command == "jumpto":
            lcdout.write("\xFEX\xFE\x48\xFE\x47\x06\x01Quod Libet\xFE\x47\x02\x02* jump to playing *\n")
            wait_time = 0.5
        elif command == "visible":
            lcdout.write("\xFEX\xFE\x48\xFE\x47\x06\x01Quod Libet\xFE\x47\x02\x02* toggle visible *\n")
            wait_time = 0.5
        elif command == "clearf":
            lcdout.write("\xFEX\xFE\x48\xFE\x47\x06\x01Quod Libet\xFE\x47\x03\x02* clear filter *\n")
            wait_time = 0.5
        last_command = command

    if time.time() - last_time > wait_time and not stopped:

        last_command = ""
        if phase < 2:

            if not len(np_artist) < 40 and scroll_counter_artist < len(np_artist) + 1:
                scroll_counter_artist += 1;
            if not len(np_title) < 40 and scroll_counter_title < len(np_title) + 1:
                scroll_counter_title += 1;
            if (scroll_counter_artist == len(np_artist) + 1 or scroll_counter_artist == 1) and (scroll_counter_title == len(np_title) + 1 or scroll_counter_title == 1):
                scroll_counter_artist = 1
                scroll_counter_title = 1
                last_time = time.time()
                wait_time = 3
                phase += 1

            upper_row = np_artist[scroll_counter_artist - 1 : scroll_counter_artist + 19]
            upper_row = upper_row + np_artist[0 : 20 - len(upper_row)]
            lower_row = np_title[scroll_counter_title - 1 : scroll_counter_title + 19]
            lower_row = lower_row + np_title[0 : 20 - len(lower_row)]
            lcdout.write("\xFEH" + upper_row + "\n" + lower_row + "\n")

        elif phase == 2:

            if len(np_album) < 21:
                upper_row = np_album
            else:
                upper_row = (np_album[0:17] + "...")
            if len(np_disc) > 0 and len(np_track) > 0:
                lower_row = "Disc " + np_disc + ", Track " + np_track
            elif len(np_track) > 0:
                lower_row = "Track " + np_track
            else:
                lower_row = ""
            # Indexing with 0:20 doesn't cause errors even if string is shorter.
            lcdout.write("\xFEX\xFE\x48" + upper_row + "\n" + lower_row[0:20] + "\n")
            last_time = time.time()
            wait_time = 3
            phase = 0

