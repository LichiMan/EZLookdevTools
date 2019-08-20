import random
import os
import logging
import json

from lookdevtools.external import fuzzywuzzy
from lookdevtools.external.fuzzywuzzy import fuzz
from lookdevtools.common import templates
from lookdevtools.common.templates import TEXTURESET_ELEMENT_MATCHING_RATIO
from lookdevtools.common.constants import CONFIG_MATERIALS_JSON

logger = logging.getLogger(__name__)

"""
json format for parsed textures is the following
In this case, the textures files have been condensed by the udim,
And the {udim} pattern matched part of the filepath has been replaced with <udim>
[
    {u'udim': u'1001',
        u'filepath': u'/run/media/ezequielm/misc/wrk/current/cabinPixar/textures/armChair/armchair_all_baseColor_sRGB.<udim>.tif',
        u'surfacing_project': u'armchair',
        u'colorspace': u'sRGB',
        u'surfacing_object': u'all',
        u'textureset_element': u'baseColor',
        u'shader_plug': u'diffuseColor'},
    {u'udim': u'1001',
        u'filepath': u'/run/media/ezequielm/misc/wrk/current/cabinPixar/textures/armChair/armchair_all_Height_raw.<udim>.tif',
        u'surfacing_project': u'armchair',
        u'colorspace': u'raw',
        u'surfacing_object': u'all',
        u'textureset_element': u'Height',
        u'shader_plug': u'None'},
    {u'udim': u'1001',
        u'filepath': u'/run/media/ezequielm/misc/wrk/current/cabinPixar/textures/armChair/armchair_all_Metalness_raw.<udim>.tif',
        u'surfacing_project': u'armchair',
        u'colorspace': u'raw',
        u'surfacing_object': u'all',
        u'textureset_element': u'Metalness',
        u'shader_plug': u'specularExtinctionCoeff'},
    {u'udim': u'1001',
        u'filepath': u'/run/media/ezequielm/misc/wrk/current/cabinPixar/textures/armChair/armchair_all_Normal_raw.<udim>.tif',
        u'surfacing_project': u'armchair',
        u'colorspace': u'raw',
        u'surfacing_object': u'all',
        u'textureset_element': u'Normal',
        u'shader_plug': u'bump'},
    {u'udim': u'1001',
        u'filepath': u'/run/media/ezequielm/misc/wrk/current/cabinPixar/textures/armChair/armchair_all_specularRoughness_raw.<udim>.tif',
        u'surfacing_project': u'armchair',
        u'colorspace': u'raw',
        u'surfacing_object': u'all',
        u'textureset_element': u'specularRoughness',
        u'shader_plug': u'specularRoughness'
    }
]

Non condensed example. Notice the several baseColor entrie, with different udims
[
    {u'udim': u'1001',
        u'filepath': u'/run/media/ezequielm/misc/wrk/current/cabinPixar/textures/armChair/armchair_all_baseColor_sRGB.1001.tif',
        u'surfacing_project': u'armchair',
        u'colorspace': u'sRGB',
        u'surfacing_object': u'all',
        u'textureset_element': u'baseColor',
        u'shader_plug': u'diffuseColor'},
    {u'udim': u'1002',
        u'filepath': u'/run/media/ezequielm/misc/wrk/current/cabinPixar/textures/armChair/armchair_all_baseColor_sRGB.1002.tif',
        u'surfacing_project': u'armchair',
        u'colorspace': u'sRGB',
        u'surfacing_object': u'all',
        u'textureset_element': u'baseColor',
        u'shader_plug': u'diffuseColor'},
    ...
    ...
]
"""

def get_random_color(seed):
    """Returns a random color using a seed. Used by
    all material creating, and viewport color functions
    that do not use textures"""
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
        logger.info("Directory create: %s" % path)
    except:
        logger.info("Directory alreay exists: %s" % path)

def is_directory(path):
    if os.path.exists(path) and os.path.isdir(path):
        return True
    else:
        return False

def get_files_in_folder (path, recursive = False, pattern = None):
    """Searchs files in a folder, with options for recursive search,
    and matching a pattern, usually used for extensions like '.exr'
    """
    logger.info("Searching for files in: %s" % path)
    logger.info("Search options: Recursive %s, pattern: %s" % (recursive,pattern))
    if os.path.isdir(path):
        for path, subdirs, files in os.walk(path):
            file_list = []
            for file in files:
                if pattern:
                    if pattern in file:
                        file_list.append(os.path.join(path,file))
                        logger.info("File with pattern found, added to the list: %s" % file)
                else:
                    file_list.append(os.path.join(path,file))
                    logger.info("File added to the list: %s" % file)
            if not recursive:
                break
    else:
        raise ValueError("Path not valid")
    return file_list

def string_matching_ratio(stringA, stringB):
    """Compares two strings and returns a fuzzy string matching ratio"""
    # We can -in the future- change the fuzzy string
    # comparisson algorigth here, maybe bitap with
    # partial substring matching will be better.
    # In general ratio, partial_ratio, token_sort_ratio
    # and token_set_ratio did not give different 
    # results given that we are comparin a single
    # word.
    # Test Results to have an idea of ratios:
    '''
    Different channels fuzzy ratio comparission
        ('baseColor','diffusecolor')        =   67
        ('base','diffusecolor')             =   25
        ('specular','specularColor')        =   76
        ('specular','specularcolor')        =   76
        ('specular_color', 'specular_bump') =   67
        ('coat_color', 'coat_ior')          =   78
        ('secondary_specular_color', 'secondary_specular_ior')  =   91
        ('subsurface_weight', 'subsurface_Color')   =  67
        ('emission', 'emission_weight')     =   70
    Same channel diferent naming ratio comparission
        ('diffuse_weight','diffuseGain')    =   64
    '''
    return fuzz.token_set_ratio(stringA, stringB)

def load_json(file_path):
    """Loads a json an returns a dict"""
    with open(file_path) as handle:
        dictdump = json.loads(handle.read())
    return dictdump

def save_json(file_path, data):
    """ Dumps a dict into a json file"""
    pass

def get_config_materials():
    """Returns the CONFIG_MATERIALS_JSON as a dict"""
    return load_json(CONFIG_MATERIALS_JSON)

def search_material_mapping(textureset_element = None):
    """Give a textureset_element name, it searchs the CONFIG_JSON file material mapping keys.
    Uses fuzzy string matching to get an approximation using TEXTURESET_ELEMENT_MATCHING_RATIO
    as returns the first hit.""" 
    config = get_config_materials()
    logger.debug('TEXTURESET_ELEMENT_MATCHING_RATIO = %s' % TEXTURESET_ELEMENT_MATCHING_RATIO)
    for key in config['material_mapping']['PxrSurface']:
        ratio = string_matching_ratio(textureset_element, key)
        logger.info('comparing %s with %s. Ratio is %s' %(textureset_element, key, ratio))
        if ratio > TEXTURESET_ELEMENT_MATCHING_RATIO:
            logger.info('ratio above threshold. Matched %s with %s.' %(textureset_element, key))
            return config['material_mapping']['PxrSurface'][key]
    return 'None'

def get_unique_key_values(file_template_list, key):
    """Get unique key values from a list of dicts"""
    uniques = []
    for each in file_template_list:
        value = each[key]
        if value not in uniques:
           uniques.append(value)
    logger.info('Unique keys found: %s' %uniques)
    return uniques

def get_udim_file_templates(file_template_list):
    """Given a [] of files with <udim> in the file path, returns unique dicts"""
    # TODO: There has to a better way to do this!
    for each in file_template_list:
        each['file_path'] = each['file_path'].replace(each['udim'], '<udim>')
    unique_values = get_unique_key_values(file_template_list, 'file_path')
    found_values = []
    udim_groups = []
    for each in file_template_list:
        path = each['file_path']
        if path not in found_values:
            found_values.append(path)
            udim_groups.append(each)
    return udim_groups