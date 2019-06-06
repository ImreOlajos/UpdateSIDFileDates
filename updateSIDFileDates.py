import os
import sys
import struct
import time
import datetime
import argparse
import logging

# List of valid magicIDs for SID files.
SID_MagicIDs = ["PSID","RSID"]

logging.basicConfig(level=logging.INFO, format="%(message)s")

parser = argparse.ArgumentParser(description="Changes file modification times of SID files to match their release dates.")
parser.add_argument("hvscDir",
                    help="Directory name to process")

args = parser.parse_args()

hvsc_dir = args.hvscDir

if not os.path.isdir(hvsc_dir):
    parser.error("Not a directory: " + hvsc_dir)

logging.info("Updating SID files in directory: " + hvsc_dir)

for root, subdirs, files in os.walk(hvsc_dir):
    logging.info("Processing " + root)
    
    for filename in files:
        # Only files with SID extensions are handled.
        if filename.endswith(".sid"):
            file_path = os.path.join(root, filename)
            logging.debug("\nFile: " + file_path)
            
            with open(file_path, 'rb') as file:
                (magicID) = struct.unpack(">4s", file.read(4))

                if (magicID[0].decode("ascii") in SID_MagicIDs):
                    # It's a valid SID file.
                    
                    # Technically, we don't need to unpack the entire basic SID
                    # header, but why not...
                    (SIDheader) = struct.unpack(">HHHHHHHI32s32s32s", file.read(114))
                    logging.debug("Type: " + magicID[0].decode("ascii"))
                    logging.debug("Version: " + str(SIDheader[0]))
                    logging.debug("DataOffset: 0x%04X" % SIDheader[1])
                    logging.debug("LoadAddress: 0x%04X" % SIDheader[2])
                    logging.debug("InitAddress: 0x%04X" % SIDheader[3])
                    logging.debug("PlayAddress: 0x%04X" % SIDheader[4])
                    logging.debug("Songs: " + str(SIDheader[5]))
                    logging.debug("StartSong: " + str(SIDheader[6]))
                    logging.debug("Speed: 0x%04X" % SIDheader[7])
                    logging.debug("Name: " + str(SIDheader[8].decode("windows-1252")))
                    logging.debug("Author: " + str(SIDheader[9].decode("windows-1252")))
                    logging.debug("Released: " + str(SIDheader[10].decode("windows-1252")))
                    
                    # The ASCII fields in SID headers are actually extended ASCII
                    # using the Western encoding.
                    released = SIDheader[10].decode("windows-1252")
                    
                    # Extract just the year from the Released field.
                    # Luckily, in HVSC files this is always the first 4 chars.
                    released_components = released.split()
                    year = released_components[0][:4]

                    # Ignore files with unknown release dates.
                    if "?" not in year:
                        logging.debug("Changing year to: " + year)
                        
                        # Set the modification time to Jan 1 of that year.
                        date = datetime.datetime(year=int(year), month=1, day=1)
                        modTime = time.mktime(date.timetuple())
                        os.utime(file_path, (modTime, modTime))                   