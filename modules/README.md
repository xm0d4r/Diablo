# `modules/` Directory

This directory contains the different modules used by the tool.

## Structure
Each module is responsible for a specific functionality within the tool and should be structured as follows:
```
modules/
 ├── nmap.py
 ├── webanalyze.py
 ├── testssl.py
 ├── ffuf.py
 ├── shcheck.py
```

This directory allows for modular expansion, making it easy to add new functionalities without modifying the core system.

