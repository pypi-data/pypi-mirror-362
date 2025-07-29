from __future__ import print_function
import io
import os
import platform
import socket
import sys

from eel import chrome
from cx_Freeze import __version__ as cxfreeze_version_string


class ForwardToFunctionStream(io.TextIOBase):
    def __init__(self, output_function=print):
        self.output_function = output_function

    def write(self, string):
        self.output_function(string)
        return len(string)


def can_use_chrome():
    """ Identify if Chrome is available for Eel to use """
    chrome_instance_path = chrome.find_path()
    return chrome_instance_path is not None and os.path.exists(chrome_instance_path)


def open_output_folder(folder):
    """ Open a folder in the local file explorer """
    folder_directory = os.path.abspath(folder)
    if platform.system() == 'Windows':
        os.startfile(folder_directory, 'explore')
    elif platform.system() == 'Linux':
        os.system('xdg-open "' + folder_directory + '"')
    elif platform.system() == 'Darwin':
        os.system('open "' + folder_directory + '"')
    else:
        return False
    return True


def get_warnings():
    warnings = []

    try:
        cxfreeze_version = parse_version_tuple(cxfreeze_version_string)
    except ValueError:
        message = 'Unable to parse cx_Freeze version - this may be because you aren\'t using an official release.'
        message += '\nYou are currently using cx_Freeze {cxfreeze_version}.'.format(cxfreeze_version=cxfreeze_version_string)
        message += '\nIf this is an official release, please report this issue on GitHub.'
        warnings.append({
            'message': message,
            'link': None
        })
        return warnings

    # Make sure cx_Freeze 6.9 or above is being used with Python 3.10+
    try:
        if sys.version_info >= (3, 10) and cxfreeze_version < (6, 9):
            message = 'You will need cx_Freeze 6.9 or above to use this tool with Python 3.10+.'
            message += '\nYou are currently using cx_Freeze {cxfreeze_version}.'.format(cxfreeze_version=cxfreeze_version_string)
            message += '\nPlease upgrade cx_Freeze: python -m pip install cx-Freeze --upgrade'
            warnings.append({
                'message': message,
                'link': None
            })
    except ValueError:
        pass  # Dev branches will have cxfreeze_version as a string in the form X.Y.devZ+HASH. Ignore it if this is the case.

    # Make sure cx_Freeze 6.4 above is being used with Python 3.9.
    try:
        if sys.version_info == (3, 9) and cxfreeze_version < (6, 4):
            message = 'You will need cx_Freeze 6.4 or above to use this tool with Python 3.9.'
            message += '\nYou are currently using cx_Freeze {cxfreeze_version}.'.format(cxfreeze_version=cxfreeze_version_string)
            message += '\nIt is highly recommended to update your version of cx_Freeze using: python -m pip install cx-Freeze --upgrade'
            warnings.append({
                'message': message,
                'link': None
            })
    except ValueError:
        pass  # Dev branches will have cxfreeze_version as a string in the form X.Y.devZ+HASH. Ignore it if this is the case.

    # Make sure cx_Freeze 6.1 or above is being used with Python 3.8
    try:
        if sys.version_info == (3, 8) and cxfreeze_version < (6, 1):
            message = 'You will need cx_Freeze 6.1 or above to use this tool with Python 3.8.'
            message += '\nYou are currently using cx_Freeze {cxfreeze_version}.'.format(cxfreeze_version=cxfreeze_version_string)
            message += '\nPlease upgrade cx_Freeze: python -m pip install cx-Freeze --upgrade'
            warnings.append({
                'message': message,
                'link': None
            })
    except ValueError:
        pass  # Dev branches will have cxfreeze_version as a string in the form X.Y.devZ+HASH. Ignore it if this is the case.

    # Make sure cx_Freeze 6.0 or above is being used with Python 3.6, 3.7
    try:
        if (3, 6) <= sys.version_info <= (3, 7) and cxfreeze_version < (6, 0):
            message = 'You will need cx_Freeze 6.0 or above to use this tool with Python 3.6, 3.7.'
            message += '\nYou are currently using cx_Freeze {cxfreeze_version}.'.format(cxfreeze_version=cxfreeze_version_string)
            message += '\nPlease upgrade cx_Freeze: python -m pip install cx-Freeze --upgrade'
            warnings.append({
                'message': message,
                'link': None
            })
    except ValueError:
        pass  # Dev branches will have cxfreeze_version as a string in the form X.Y.devZ+HASH. Ignore it if this is the case.

    # Make sure cx_Freeze 6.0 to 6.3 is being used with Python 3.5.
    try:
        if sys.version_info == (3, 5) and (cxfreeze_version < (6, 0) or cxfreeze_version > (6, 3)):
            message = 'You will need cx_Freeze 6.0 to 6.3 to use this tool with Python 3.5.'
            message += '\nYou are currently using cx_Freeze {cxfreeze_version}.'.format(
                cxfreeze_version=cxfreeze_version_string)
            message += '\nPlease upgrade cx_Freeze: python -m pip install cx-Freeze --upgrade'
            warnings.append({
                'message': message,
                'link': None
            })
    except ValueError:
        pass  # Dev branches will have cxfreeze_version as a string in the form X.Y.devZ+HASH. Ignore it if this is the case.

    # Make sure cx_Freeze 5.1.1 is being used with Python 2.7.
    try:
        if sys.version_info <= (2, 7) and cxfreeze_version != (5, 1, 1):
            message = 'You will need cx_Freeze 5.1.1 to use this tool with Python 2.7.'
            message += '\nYou are currently using cx_Freeze {cxfreeze_version}.'.format(
                cxfreeze_version=cxfreeze_version_string)
            message += '\nPlease upgrade cx_Freeze: python -m pip install cx-Freeze --upgrade'
            warnings.append({
                'message': message,
                'link': None
            })
    except ValueError:
        pass  # Dev branches will have cxfreeze_version as a string in the form X.Y.devZ+HASH. Ignore it if this is the case.

    # Make sure we are not using Python from the Windows Store
    if r"Packages\PythonSoftwareFoundation.Python." in sys.executable:
        message = 'It looks like you may be using Python from the Windows Store, the Python binary you are currently using is at:'
        message += '"' + sys.executable + '"'
        message += '\n\nPython from the Windows Store is not supported by cx_Freeze, you may receive some error.'
        message += '\nTo fix this, use a distribution of Python from python.org.'
        warnings.append({
            'message': message,
            'link': None
        })

    return warnings


def get_port():
    """ Get an available port by starting a new server, stopping and and returning the port """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 0))
    port = sock.getsockname()[1]
    sock.close()
    return port


def parse_version_tuple(version_string):
    """ Turn a version string into a tuple of integers e.g. "1.2.3" -> (1, 2, 3) """
    return tuple(map(int, (version_string.split("."))))
