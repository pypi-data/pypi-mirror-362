from __future__ import print_function

import argparse
import logging
import os
import shlex
import shutil
import sys
import traceback

from . import config
from . import __version__ as version
from . import log as logging
from cx_Freeze.cli import main as run_cxfreeze

logger = logging.getLogger(__name__)


def __get_cxfreeze_argument_parser():
    from cx_Freeze.cli import prepare_parser
    parser = prepare_parser()
    return parser


def get_cxfreeze_options():
    parser = __get_cxfreeze_argument_parser()

    options = []
    for action in parser._actions:
        # Clean out what we can't send over to the ui
        # Here is what we currently have: https://github.com/python/cpython/blob/master/Lib/argparse.py#L771
        del action.container
        options.append(action)

    return [o.__dict__ for o in options]


def will_packaging_overwrite_existing(file_path, output_folder, target_name):
    """ Checks if there is a possibility of a previous output being overwritten. """
    if not os.path.exists(output_folder):
        return False
    suffix = '.exe' if sys.platform == 'win32' else ''
    no_extension = '.'.join(os.path.basename(file_path).split('.')[:-1]) + suffix if target_name=='' else target_name + suffix
    if no_extension in os.listdir(output_folder):
        return True
    else:
        return False


def __move_package(src, dst):
    """ Move the output package to the desired path (default is output/ - set in script.js) """
    # Make sure the destination exists
    if not os.path.exists(dst):
        os.makedirs(dst)

    # Move all files/folders in dist/
    for file_or_folder in os.listdir(src):
        _dst = os.path.join(dst, file_or_folder)
        # If this already exists in the destination, delete it
        if os.path.exists(_dst):
            if os.path.isfile(_dst):
                os.remove(_dst)
            else:
                shutil.rmtree(_dst)
        # Move file
        shutil.move(os.path.join(src, file_or_folder), dst)


def package(cxfreeze_command, options):
    """
    Call PyInstaller to package a script using provided arguments and options.
    :param cxfreeze_command: Command to supply to cx_Freeze
    :param options: auto-py-to-app specific options for setup and cleaning up
    :return: Whether packaging was successful
    """

    # Show current version
    logger.info("Running auto-py-to-app v" + version)

    # Notify the user of the workspace and setup building to it
    logger.info("Building directory: {}".format(config.temporary_directory))

    # Override arguments
    dist_path = os.path.join(config.temporary_directory, 'application')
    extra_args = ['--target-dir', dist_path]

    logger.info('Provided command: {}'.format(cxfreeze_command))

    # Setup options
    increase_recursion_limit = options['increaseRecursionLimit']
    output_directory = os.path.abspath(options['outputDirectory'])

    if increase_recursion_limit:
        sys.setrecursionlimit(5000)
        logger.info("Recursion Limit is set to 5000")
    else:
        sys.setrecursionlimit(config.DEFAULT_RECURSION_LIMIT)

    # Run cx_Freeze
    fail = False
    try:
        # Since we allow manual argument input, we cannot pass arguments to cx_Freeze as a list as we can't
        # guarantee that the arguments will be parsed correctly. To get around this, we can set sys.argv here with our
        # command to trick cx_Freeze to reading the command as if we are using the cli tool.
        sys.argv = shlex.split(cxfreeze_command) + extra_args # Put command into sys.argv

        # Display the command we are using and leave a space to separate out cx_Freeze logs
        logger.info('Executing: {}'.format(' '.join(sys.argv)))
        logger.info('')

        with logging.Logger('cx_Freeze'):
            run_cxfreeze()
    except:
        fail = True
        logger.exception("An error occurred while packaging")

    # Move project if there was no failure
    logger.info("")
    if not fail:
        logger.info("Moving project to: {0}".format(output_directory))
        try:
            __move_package(dist_path, output_directory)
        except:
            logger.error("Failed to move project")
            logger.exception(traceback.format_exc())
    else:
        logger.info("Project output will not be moved to output folder")
        return False

    # Set complete
    return True
