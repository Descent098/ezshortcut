![shortcut logo](https://raw.githubusercontent.com/Descent098/ezshortcut/master/.github/logo.png)

# EZ Shortcut

*Generate shortcuts to executables and/or folders*

## Table of Contents
- [What does ezshortcut do?](#what-does-ezshortcut-do)
- [Features & Roadmap](#features--roadmap)
- [Why should I use ezshortcut?](#why-should-i-use-ezshortcut)
- [Quick-start](#quick-start)
    - [Installation](#installation)
      - [From source](#from-source)
      - [From PyPi](#from-pypi)
      - [Examples](#examples)
- [Additional Documentation](#additional-documentation)

## What does ezshortcut do?

Ez shortcut is a simple API with one primary function that lets you setup shortcuts to executables, or to folders.

## Features & Roadmap

The primary features include:
- Cross platform shortcut generation
- Creting folder shortcuts
- Creating executable shortcuts

The full roadmap can be found [here](https://github.com/Descent098/ezshortcut/projects).

## Why should I use ezshortcut?

Ez shortcut is definately the simplest way to setup shortcuts to generic binaries, and/or folder links in python. If however you are looking to make a shortcut to a python script, then checkout [pyshortcuts](https://github.com/newville/pyshortcuts).

## Quick-start

### Installation

#### From source

1. Clone this repo: https://github.com/Descent098/ezshortcut
2. Run ```pip install .``` or ```sudo pip3 install .```in the root directory

#### From PyPi

1. Run ```pip install ezshortcut```

#### Examples

*Creating a folder shortcut to the Documets folder on the desktop with the minimum necessary fields*
```python
import os
from ezshortcut import create_shortcut

# Get the documents folder dependent on OS
DOCUMENTS_FOLDER = f"{os.getenv('USERPROFILE')}\\Documents" if os.name == 'nt' else f"{os.getenv('HOME')}/Documents"

create_shortcut("Documents", DOCUMENTS_FOLDER) # Create shortcut on desktop called Documents
```

*Creating an executable shortcut to blender 2.82 on windows with minimum necessary fields*
```python
import os
from ezshortcut import create_shortcut

# The directory you want to open the executable from
WORKING_DIR = f"{os.getenv('USERPROFILE')}\\Documents"

# Get the blender path dependent on windows
BLENDER_PATH = f"{os.getenv('ProgramFiles')}\\Blender Foundation\\Blender 2.82\\blender.exe"

create_shortcut("Blender", WORKING_DIR, executable=BLENDER_PATH) # Create shortcut on desktop called Blender
```

*Creating an executable shortcut on the desktop with all fields possible*

```python
import os
from ezshortcut import create_shortcut

# The directory you want to open the executable from
WORKING_DIR = f"{os.getenv('USERPROFILE')}\\Documents"

# Get the blender path dependent on windows
BLENDER_PATH = f"{os.getenv('ProgramFiles')}\\Blender Foundation\\Blender 2.82\\blender.exe"

# The folder to put the shortcut in 
SHORTCUT_PATH = f"{os.getenv('USERPROFILE')}\\Desktop"

# The path to a custom icon file (.ico on win/linux, .icns on MacOS)
ICON_PATH = "path\\to\\icon.ico"

create_shortcut("Blender", WORKING_DIR, SHORTCUT_PATH, BLENDER_PATH, ICON_PATH) # Create shortcut on desktop called Documents
```

## Additional Documentation

Full API docs can be found at [https://kieranwood.ca/ezshortcut](https://kieranwood.ca/ezshortcut)
