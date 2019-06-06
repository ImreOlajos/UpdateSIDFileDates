# UpdateSIDFileDates

Changes file modification times of SID files (Commodore-64 music files) in the
given directory to match their actual release dates.

It reads the release date of a SID file from the SID file's metadata, and if
it's a known year (no question mark in the year), it sets the given SID file's
modification time to Jan 1 of that year. Some release dates are given with a
range (e.g. 1996-1987), in this case the first year will be set as the
modification time.

This way when you use your favorite file browser's "sort by date" option, the
SID files will sort by their actual release dates!

__NOTE__: Since HVSC updates touch several SID files and since HVSC updates may
update release dates within SID files, you should run this script on your HVSC
directory after every update to keep the file modification times in sync with
the release dates.

# Requirements

- [Python 3](https://www.python.org/downloads/)
- A directory containing SID files. For example, the [High Voltage SID Collection (HVSC)](http://www.hvsc.de) installed on your local drive.

# Usage
`py updateSIDFileDates.py [-h] dir`

Positional arguments:
- `dir` Directory name to process

Optional arguments:
- `-h, --help`  show help message and exit