# `dependencies/` Directory

This directory contains external dependencies required by different modules of the tool.

## Structure
```
dependencies/
 ├── ffuf/
 │   ├── allinone.txt
 │   ├── wordlist2.txt
 ├── webanalyze/
 │   ├── technologies.json
```

## Description
- **`ffuf/`**: Contains wordlists used by FFUF for fuzzing.
- **`webanalyze/`**: Stores `technologies.json`, which is required by Webanalyze to identify technologies on web targets.