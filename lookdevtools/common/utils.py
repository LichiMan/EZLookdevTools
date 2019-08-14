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

