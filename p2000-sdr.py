#!/usr/bin/env python3

""" p2000-sdr.py - small python script to view dutch emergancy messages that
    are sended over the FM radio band. """

# =========================================================================== #
# File   : p2000-sdr.py                                                       #
# Purpose: Display p2000 messages from the ether (FM band)                    #
#                                                                             #
# Author : Harald van der Laan                                                #
# Date   : 2020-07-16                                                         #
# Version: v1.0.2                                                             #
# =========================================================================== #
# Changelog:                                                                  #
# - v1.0.2: Small display changes                       (Harald van der Laan) #
# - v1.0.1: Fixed minor typos                           (Harald van der Laan) #
# - v1.0.0: Initial version                             (Harald van der Laan) #
# =========================================================================== #
# Copyright © 2020 Harald van der Laan                                        #
#                                                                             #
# Permission is hereby granted, free of charge, to any person obtaining       #
# a copy of this software and associated documentation files (the "Software"),#
# to deal in the Software without restriction, including without limitation   #
# the rights to use, copy, modify, merge, publish, distribute, sublicense,    #
# and/or sell copies of the Software, and to permit persons to whom the       #
# Software is furnished to do so, subject to the following conditions:        #
#                                                                             #
# The above copyright notice and this permission notice shall be included     #
# in all copies or substantial portions of the Software.                      #
#                                                                             #
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,             #
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES             #
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.   #
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, #
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,               #
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE  #
# OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.                               #
# =========================================================================== #

import sys
import os
import time
import re
from subprocess import Popen, PIPE


def coloriz(capcode):
    """ colorizing text output according to capcode """
    lfl = '000120901|000923993|001420059|MMT|Traumaheli'
    fdp = '00[0-9][0-9]0[0-9]{4}|^[Pp]\s?[12]|.*[Pp][Rr][Ii][Oo].*'
    ems = '00[0-9][0-9]2[0-9]{4}|^A[12]|^B[12]'
    pdp = '00[0-9][0-9]3[0-9]{4}|.*[Pp][Oo][Ll][Ii][Tt][Ii][Ee].*'

    if re.match(lfl, capcode):
        color = '\033[92m'
    elif re.match(fdp, capcode):
        color = '\033[91m'
    elif re.match(ems, capcode):
        color = '\033[93m'
    elif re.match(pdp, capcode):
        color = '\033[94m'
    else:
        color = '\033[0m'

    return color


def main():
    """ Main python function """
    command = 'rtl_fm -f 169.65M -M fm -s 22050 -p 45 -g 30 | multimon-ng -a FLEX -t raw -'
    sdr = Popen(command, stdout=PIPE, stderr=PIPE, shell=True)
    caplist = {}

    with open('capcodes.dict', 'r') as fdh:
        for line in fdh:
            key, value = line.strip().split(' = ')
            caplist[key] = value

    try:
        while True:
            p2000 = sdr.stdout.readline().decode('utf-8')
            sdr.poll()

            if p2000.__contains__('ALN'):
                if p2000.startswith('FLEX'):
                    message = p2000.strip().split('ALN|')[1]
                    capcodes = p2000[43:].split('|ALN|')[0].split()
                    date = time.strftime('%Y/%m/%d %H:%M:%S')

                    print(f'\n\033[0mMelding van: {date}')
                    print(f'{coloriz(message)}{message}\033[0m')

                    for capcode in capcodes:
                        try:
                            capdesc = caplist[capcode]
                        except KeyError:
                            capdesc = 'Onbekende of persoonlijke capcode'

                        print(f'{coloriz(capcode)}[{capcode}]: {capdesc}')

    except KeyboardInterrupt:
        os.kill(sdr.pid, 9)
        sys.exit(0)


if __name__ == "__main__":
    main()
