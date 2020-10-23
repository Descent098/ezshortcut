# Standard Library Dependencies
import os                             # Used for path validation
import sys                            # Used to access info about system
import logging                        # Used for optional logging details
import traceback                      # Used to log error details on raise
from typing import Union
from shutil import copyfile           # Used to copy files between directories

# Third-Party Dependencies
import winshell                       # Allows execution of winshell functions
from win32com.client import Dispatch  # Instantiate COM objects to dispatch any tasks through

# Setting up Constants

#  OS name booleans
mac = True if sys.platform == "darwin" else False
windows = True if os.name == "nt" else False
linux = True if sys.platform == "linux" or sys.platform == "linux2" else False

# Instalation and download folders
DOWNLOAD_FOLDER = f"{os.getenv('USERPROFILE')}\\Downloads" if windows else f"{os.getenv('HOME')}/Downloads"
DESKTOP_FOLDER = f"{os.getenv('USERPROFILE')}\\Desktop" if windows else f"{os.getenv('HOME')}/Desktop"

def _generate_shortcut_windows(working_dir:str, path:str, executable:Union[str,bool] = False, icon:Union[str,bool] = False):
    """The steps to generate an icon for windows

    Parameters
    ----------
    working_dir : str
        The path to the directory to execute the executable from, or create folder shortcut to
    path : Union[str,bool], optional
        The path where you want to put the shortcut, by default False
    executable : Union[str,bool], optional
        The path to the executable you want to create a shortcut for, by default False
    icon : Union[str,bool], optional
        The path to a custom icon to use for the shortcut, by default False
    """
    logging.debug("Grabbing windows shell scripts")
    shell = Dispatch('WScript.Shell')  # Grab the WScript shell function to build shortcuts

    logging.debug("Creating shortcut template")
    if not path: # TODO: Setup proper default
        path = os.path.join(DESKTOP_FOLDER, "Ignite.lnk")  # Setup path for shortcut
    shortcut = shell.CreateShortCut(path)  # Begin creating shortcut objects
    # Add previously built variables to shortcut object

    logging.debug("Writing shortcut attributes to object")
    if executable:
        shortcut.Targetpath = executable
    if icon:
        shortcut.IconLocation = icon
    shortcut.WorkingDirectory = os.path.realpath(working_dir)

    logging.debug("Flushing shortcut")
    shortcut.save() # Flush shortcut to the desktop


def _generate_shortcut_linux():
    ...


def _generate_shortcut_macos():
    ...


def create_shortcut(working_dir:str, path:Union[str,bool] = False, executable:Union[str,bool] = False, icon:Union[str,bool] = False):
    """Primary entrypoint to generate a shortcut across platform

    Parameters
    ----------
    working_dir : str
        The path to the directory to execute the executable from, or create folder shortcut to
    path : Union[str,bool], optional
        The path where you want to put the shortcut, by default False
    executable : Union[str,bool], optional
        The path to the executable you want to create a shortcut for, by default False
    icon : Union[str,bool], optional
        The path to a custom icon to use for the shortcut, by default False
    """

    #TODO: preprocess parameters

    logging.debug("Setting up shortcut attributes")

    if windows:
        _generate_shortcut_windows(working_dir, path, executable, icon)
    elif linux:
        _generate_shortcut_linux()
    elif mac:
        _generate_shortcut_macos()
