<!--
SPDX-FileCopyrightText: © 2025 Corn

SPDX-License-Identifier: GFDL-1.3-or-later
-->

# PyRom

A set of tools for checking if the ROMs in your collection match the entries in a DAT file.

PyRom can:

- verify that correctly named ROMs match respective checksums (and do so in parallel - drastically speeding up the process)
- report missing or incorrectly named ROMs
- modify DAT files to include or exclude certain hash algorithms (including ones not originally present in the file)

## Installation

Pyrom supports Python version 3.12 and above.
The only hard dependency is python-rich.

Install with pip:

> pip install pyrom

### Extra dependencies

For non-standard hash algorithms, install with the corresponding extra package.
An optional dependency on lxml is also included for faster XML parsing.

You can install pyrom with all dependencies like so:

> pip install pyrom[lxml, xxhash, blake3]

## Typical usage

(See the \-\-help output and/or man pages for more details. The '--' is not necessary but can help prevent mistaking file names for options.)

Parse DAT files and check all ROMs in a directory, showing a summary and all failed files:

> `pyrom -d romfiles -Sf -- datfiles/*dat`

Check to make sure all your files are correctly named:

> `pyrom-resolve -d datfiles/*.dat -f romfiles/*`

Trim down your DATs to only include games you have stored and only store the blake3 checksum:

> `pyrom-morph -d romfiles --trim --select-checks blake3 -- datfiles/*dat`
