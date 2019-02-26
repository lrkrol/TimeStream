#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
TimeStream 0.1.0

Copyright 2019 Laurens R Krol

    Team PhyPA, Biological Psychology and Neuroergonomics,
    Technische Universitaet Berlin

    lrkrol.com

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

"""
Broadcasts an LSL stream of time stamps, in two channels.

Channel 1: Time in seconds taken from Python's time.time().
Channel 2: Calculated time in seconds between the current and
           previous submitted sample.

Usage:
Make sure to have pylsl installed; execute 'pip install pylsl' or see:
https://github.com/labstreaminglayer/liblsl-Python

Run TimeStream.py and enter the requested sampling rate and chunk size.
Alternatively, run timestream.py with additional arguments --rate and/or
--chunksize to skip manual input, e.g.

    python .\TimeStream.py --rate 100

starts a stream at 100 Hz, using default chunk size 32.
"""


from pylsl import StreamOutlet, StreamInfo
from random import choice
from string import ascii_lowercase
from sys import argv
from time import clock, time


def main(ratehz, chunksize):
    # setting up stream info and metadata
    id = 'TimeStamps-' + ''.join(choice(ascii_lowercase) for _ in range(8))
    info = StreamInfo('Time Stamps', 'Time', 2, ratehz, 'double64', id)

    channels = info.desc().append_child('channels')
    channels.append_child('channel') \
        .append_child_value('label', 'Time') \
        .append_child_value('unit', 'seconds') \
        .append_child_value('type', 'Time')
    channels.append_child('channel') \
        .append_child_value('label', 'Delay') \
        .append_child_value('unit', 'seconds') \
        .append_child_value('type', 'Time')

    outlet = StreamOutlet(info, chunksize, 360)

    try:
        print 'Broadcasting time stamps at', ratehz, 'Hz in chunks of', chunksize

        delta = (1.0/ratehz)
        previoustime = clock()
        while True:
            # awaiting next point in time to send data
            nexttime = previoustime + delta
            while clock() < nexttime: pass
            delay = clock() - previoustime
            previoustime = nexttime

            # sending data
            outlet.push_sample([time(), delay])
    except KeyboardInterrupt:
        print 'Interrupted'


if __name__ == "__main__":
    # defaults
    rate = 100
    chunksize = 32

    # requesting settings only if nothing has been preset
    if len(argv) == 1:
        print 'Sampling rate in Hz:'
        rate = int(raw_input('> ') or rate)

        print 'Chunk size:'
        chunksize = int(raw_input('> ') or chunksize)
    else:
        if('--rate' in argv):
            rate = int(argv[argv.index('--rate') + 1])

        if('--chunksize' in argv):
            chunksize = int(argv[argv.index('--chunksize') + 1])

    main(rate, chunksize)