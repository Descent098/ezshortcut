"""![shortcut logo](https://raw.githubusercontent.com/Descent098/ezshortcut/master/.github/logo.png)

Generate shortcuts to executables and/or folders

Installation
------------
### From source

1. Clone this repo: https://github.com/Descent098/ezshortcut
2. Run ```pip install .``` or ```sudo pip3 install .```in the root directory

### From PyPi

1. Run ```pip install ezshortcut```

Examples
--------
See documentation for [create_shortcut()](#ezshortcut.create_shortcut) function for examples
"""

# Standard Library Dependencies
import os                             # Used for path validation
import sys                            # Used to access info about system
import logging                        # Used for optional logging details
import plistlib                       # Used to write plist files for macos
from typing import Union              # Used in multi-type type hint signatures
from shutil import copyfile           # Used to copy files between different directories

# Third-Party Dependencies
import winshell                       # Allows execution of winshell functions
from win32com.client import Dispatch  # Instantiate COM objects to dispatch any tasks through

# Setting up Constants

#  OS name booleans
mac = True if sys.platform == "darwin" else False
windows = True if os.name == "nt" else False
linux = True if sys.platform == "linux" or sys.platform == "linux2" else False

# Instalation and download folders
DESKTOP_FOLDER = f"{os.getenv('USERPROFILE')}\\Desktop" if windows else f"{os.getenv('HOME')}/Desktop"

def _generate_shortcut_windows(name:str, working_dir:str, path:str, executable:Union[str,bool], icon:str):
    """The steps to generate an icon for windows

    Parameters
    ----------
    working_dir : str
        The path to the directory to execute the executable from, or create folder shortcut to

    path : str
        The path where you want to put the shortcut

    executable : str or bool,
        The path to the executable you want to create a shortcut for, set to False if you want folder shortcut

    icon : str
        The path to a custom icon to use for the shortcut

    References
    ----------
    - WScript shell shortcut examples: https://support.microsoft.com/en-ca/help/244677/how-to-create-a-desktop-shortcut-with-the-windows-script-host
    - ss64  createshortcut docs: https://ss64.com/vb/shortcut.html
    """
    logging.debug("Grabbing windows shell scripts")
    shell = Dispatch('WScript.Shell')  # Grab the WScript shell function to build shortcuts

    logging.debug("Creating shortcut template")
    if not path: # TODO: Setup proper default
        path = os.path.join(DESKTOP_FOLDER, f"{name}.lnk")  # Setup path for shortcut
    shortcut = shell.CreateShortCut(path)  # Begin creating shortcut objects
    # Add previously built variables to shortcut object

    logging.debug("Writing shortcut attributes to object")
    if executable:
        shortcut.Targetpath = executable
        shortcut.WorkingDirectory = os.path.realpath(working_dir)
    else:
        shortcut.Targetpath = os.path.realpath(working_dir)
    shortcut.IconLocation = icon

    logging.debug("Flushing shortcut")
    shortcut.save() # Flush shortcut to the desktop


def _generate_shortcut_linux(name : str, working_dir:str, path:str, executable:Union[str,bool], icon:str) -> str:
    """The steps to generate an icon for windows

    Parameters
    ----------
    name : str;
        The name of the shortcut

    working_dir : str
        The path to the directory to execute the executable from, or create folder shortcut to

    path : str
        The path where you want to put the shortcut

    executable : str or bool,
        The path to the executable you want to create a shortcut for, set to False if you want folder shortcut

    icon : str
        The path to a custom icon to use for the shortcut

    Notes
    -----
    - The function creates a .desktop file in the specified path, and returns it's content

    References
    ----------
    - Desktop entry specification: https://developer.gnome.org/desktop-entry-spec/
    """

    if not executable:
        shortcut_type = "Directory"
        executable_string = f""
    else: # If executable is specified
        shortcut_type = "Application"
        executable_string = f"\nExec='cd {working_dir} && {executable}'"

    # Generate the .desktop file Content
    data = f"""[Desktop Entry]
Encoding=UTF-8
Version=1.0
Type={shortcut_type}
Terminal=false{executable_string}
Path='{path}'
Name={name}
Icon='{icon}'
"""
    return data


def _generate_shortcut_macos(name:str, working_dir:str, path:str, executable:Union[str,bool], icon:str) -> str:
    """The steps to generate an icon for windows

    Parameters
    ----------
    name : str;
        The name of the shortcut

    working_dir : str
        The path to the directory to execute the executable from, or create folder shortcut to

    path : str
        The path where you want to put the shortcut

    executable : str or bool,
        The path to the executable you want to create a shortcut for, set to False if you want folder shortcut

    icon : str
        The path to a custom icon to use for the shortcut

    References
    ----------
    - Introduction to Property List files: https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/PropertyLists/Introduction/Introduction.html
    - Quick Start for property list files: https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/PropertyLists/QuickStartPlist/QuickStartPlist.html#//apple_ref/doc/uid/10000048i-CH4-SW5
    """
    if executable:
        data = {"CFBundleGetInfoString":"An icon generated by ezshortcut",
        "CFBundleName":"Name",
        "CFBundleExecutable":executable,
        "CFBundleIconFile":icon,
        "CFBundlePackageType":"APPL"
        }
    else: # TODO: Figure out folder shortcut .plist files
        data = {"CFBundleGetInfoString":"An icon generated by ezshortcut",
            "CFBundleName":"Name",
            "CFBundleIconFile":icon,
            "CFBundlePackageType":"APPL"
        }
    with open("yeet.plist", "wb") as output:
        plistlib.dump(data, output, skipkeys=True)
    return str(plistlib.dumps(data))


def create_shortcut(name:str, working_dir:str, path:Union[str,bool] = False, executable:Union[str,bool] = False, icon:Union[str,bool] = False):
    """Primary entrypoint to generate a shortcut across platforms

    Parameters
    ----------
    name : str;
        The name of the shortcut

    working_dir : str;
        The path to the directory to execute the executable from, or create folder shortcut to

    path : str or bool, optional;
        The path where you want to put the shortcut, by default False

    executable : str or bool, optional;
        The path to the executable you want to create a shortcut for, by default False

    icon : str or bool, optional;
        The path to a custom icon to use for the shortcut, by default False

    Notes
    -----
    - icon must be the path to:
        - a .ico or .exe on Windows 
        - a .ico Linux
        - a .icns on MacOS
    - executable must be the path to:
        - a .exe, .bat, or .psl on Windows
        - a regular binary or .sh script, on Linux/MacOS
        - a .app also works on MacOS
    
    Raises
    ------
    NotADirectoryError:
        Raised when working_dir or path is/are not an existing directory

    FileNotFoundError:
        Raised when executable or icon is/are not a valid path to an appropriate binary/icon file
    
    Examples
    --------
    ### Creating a folder shortcut to the Documets folder on the desktop with the minimum necessary fields
    ```python
    import os
    from ezshortcut import create_shortcut

    # Get the documents folder dependent on OS
    DOCUMENTS_FOLDER = f"{os.getenv('USERPROFILE')}\\Documents" if os.name == 'nt' else f"{os.getenv('HOME')}/Documents"

    create_shortcut("Documents", DOCUMENTS_FOLDER) # Create shortcut on desktop called Documents
    ```

    ### Creating an executable shortcut to blender 2.82 on windows with minimum necessary fields
    ```python
    import os
    from ezshortcut import create_shortcut

    # The directory you want to open the executable from
    WORKING_DIR = f"{os.getenv('USERPROFILE')}\\Documents"

    # Get the blender path dependent on windows
    BLENDER_PATH = f"{os.getenv('ProgramFiles')}\\Blender Foundation\\Blender 2.82\\blender.exe"

    create_shortcut("Blender", WORKING_DIR, executable=BLENDER_PATH) # Create shortcut on desktop called Blender
    ```

    ### Creating an executable shortcut on the desktop with all fields possible

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
    """

    #TODO: preprocess parameters

    logging.debug("Validating working directory")
    if not os.path.exists(working_dir):
        raise NotADirectoryError(f"Provided directory {working_dir} is not a valid directory")

    logging.debug("Validating icon")
    if icon:
        logging.debug(f"Validating icon file {icon} exists")
        icon = os.path.realpath(icon)
        if not os.path.exists(icon):
            raise FileNotFoundError(f"The provided icon {icon} does not exist")

        # Validate icon is correct filetype
        if mac:
            if not icon.endswith(".icns"):
                raise ValueError(f"Provided icon {icon} is not a valid .icns file")
        else:
            if not icon.endswith(".ico"):
                if windows: # Check if icon can be grabbed from .exe
                    if not icon.endswith(".exe"):
                        raise ValueError(f"Provided icon {icon} is not a valid .ico file")
                else:
                    raise ValueError(f"Provided icon {icon} is not a valid .ico file")
            
            else: # is a .ico file
                #Copy provided icon to OS specific location and then use the new path
                logging.debug(f"Copying provided icon file to permenant directory")
                icon_file_name = icon.split(os.sep)[-1]
                new_icon_path = f"{os.path.abspath(__file__)}{os.sep}{icon_file_name}"
                copyfile(icon, new_icon_path)
                icon = new_icon_path

    else: # If no valid icon is provided use package default
        logging.debug(f"No valid icon provided using default")
        if mac:
            icon = os.path.realpath(f"{os.path.dirname(os.path.abspath(__file__))}{os.sep}default_icon.icns")
        else:
            icon = os.path.realpath(f"{os.path.dirname(os.path.abspath(__file__))}{os.sep}default_icon.ico")

    logging.debug("Setting up shortcut attributes")

    if windows:
        _generate_shortcut_windows(name, working_dir, path, executable, icon)

    elif linux:
        _generate_shortcut_linux()

    elif mac:
        _generate_shortcut_macos()

    logging.info("Shortcut icon created")


if __name__ == "__main__":
    create_shortcut("Documents", f"{DESKTOP_FOLDER}\\..\\Documents") # Documents shortcut
    create_shortcut("Blender 2", "C:\\Program Files\\Blender Foundation\\Blender 2.82\\blender.exe",executable="C:\\Program Files\\Blender Foundation\\Blender 2.82\\blender.exe", icon="C:\\Program Files\\Blender Foundation\\Blender 2.82\\blender.exe")