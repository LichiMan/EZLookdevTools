import random
import os
import logging

def get_random_color(seed):
    random.seed(seed + "_r")
    color_red = random.uniform(0, 1)
    random.seed(seed + "_g")
    color_green = random.uniform(0, 1)
    random.seed(seed + "_b")
    color_blue = random.uniform(0, 1)
    return [color_red, color_green, color_blue]

def create_directoy(path):
    try:
        # Create target Directory
        os.mkdir(path)
        logging.info("Directory create: %s" % path)
    except:
        logging.info("Directory alreay exists: %s" % path)

def is_directory(path):
    if os.path.exists(path) and os.path.isdir(path):
        return True
    else:
        return False

def get_files_in_folder (path, recursive = False, pattern = None):
    """Searchs files in a folder, with options for recursive search,
    and matching a pattern, usually used for extensions like '.exr'
    """
    logging.info("Searching for files in: %s" % path)
    logging.info("Search options: Recursive %s, pattern: %s" % (recursive,pattern))
    if os.path.isdir(path):
        for path, subdirs, files in os.walk(path):
            file_list = []
            for file in files:
                if pattern:
                    if pattern in file:
                        file_list.append(os.path.join(path,file))
                        logging.info("File with pattern found, added to the list: %s" % file)
                else:
                    file_list.append(os.path.join(path,file))
                    logging.info("File added to the list: %s" % file)
            if not recursive:
                break
    else:
        raise ValueError("Path not valid")
    return file_list
