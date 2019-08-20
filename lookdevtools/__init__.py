import sys
import os
import logging

logger = logging.getLogger(__name__)

# Load external packages
current_dir = os.path.dirname(__file__)
external_packages_dir = os.path.join(current_dir,'external')
logger.info('EXTERNAL MODULES: Appending external modules dir to sys.path: %s'
            %external_packages_dir)
sys.path.append(external_packages_dir)

import yapsy as yapsy
try:
    from yapsy.PluginManager import PluginManager
    logger.info('EXTERNAL MODULES: yapsy.PluginManager loaded succesfuly')
except:
    raise RuntimeError('EXTERNAL MODULES: failed to load external modules')

def load_plugins():
    # Plugin manager
    plugins = PluginManager()
    plugins_folder = os.path.join(current_dir,'plugins')
    plugins.setPluginPlaces([plugins_folder])
    plugins.collectPlugins()
    plugins.locatePlugins()
    logger.info('PLUGINS: plugin candidates %s' % plugins.getPluginCandidates())
    for pluginInfo in plugins.getAllPlugins():
        plugins.activatePluginByName(pluginInfo.name)
        logger.info('PLUGINS: plugin activated %s' % plugins.activatePluginByName(pluginInfo.name))
    return plugins