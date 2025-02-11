# `targets/` Directory

This directory contains the targets file to be used by the tool.

## File Format
Each target should be listed on a separate line within the text file located in this directory. Example structure:

```
192.168.1.1
example.com
sub.example.com
10.0.0.1
http://example.com
https://example.com/
```

## Usage
The tool will process this file line by line, treating each entry as a target for analysis.

Ensure the file is correctly formatted and does not contain unnecessary blank lines.