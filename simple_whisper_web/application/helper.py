import os
import glob
from application import logger

def remove_files_in_relative_directory(relative_path):
    # Construct the full path to the directory
    full_path = os.path.abspath(os.path.join(os.getcwd(), relative_path))

    # Ensure that the directory exists
    if not os.path.exists(full_path) or not os.path.isdir(full_path):
        logger.warning(f"Directory not found: {full_path}")
        return

    # Use glob to get a list of all files in the directory
    files_to_remove = glob.glob(os.path.join(full_path, '*'))

    if len(files_to_remove) == 0:
        logger.info(f"No files found in {full_path}")

    # Remove each file
    for file_path in files_to_remove:
        try:
            os.remove(file_path)
            logger.info(f"Removed: {file_path}")
        except Exception as e:
            logger.warning(f"Error removing file {file_path}: {e}")

import threading

def is_thread_running(thread_name):
    """
    Check if a thread with a given name is already running.
    """
    for thread in threading.enumerate():
        if thread.getName() == thread_name:
            return True
    return False
