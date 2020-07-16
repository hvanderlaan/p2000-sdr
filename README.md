# p2000-sdr

P2000 is the ducth emergancy services messaging system for pagers. The system works on the 169,650 MHz FM band. These messages can be viewed with a FM receiver and the FLEX decoder. This script make yse of a sdr dongle and a FLEX decoder to show the messages.

## Requirements

    - RTL SDR Dongle (DBV-T, FM, DAB usb) based on a RTL chipset (820T2)
    - python 3
    - librtlsdr
    - multimon-ng

## Installation

The installation guid is for MacOS, but should be the same for any other  linux/unix system.

```bash
# Installing requirements with homebrew. More info about homebrew
# visitL https://brew.sh
brew install rtl-sdr cmake pkg-config

# downloading, building and installing multimon-ng FLEX decoder
git clone https://github.com/Zanoroy/multimon-ng.git
cd multimon-ng

mkdir build
cd build
cmake ..
make
sudo make install
cd

# Installing p2000-sdr
git clone https://github.com/hvanderlaan/p2000-sdr.git
cd p2000-sdr
```

# Running the script

```bash
cd p2000-sdr
./p2000-sdr.py
```
