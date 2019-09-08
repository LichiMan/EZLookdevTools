# Table of Contents
[LookdevTools](#LookdevTools)  
[Installation](#Installation)   
[Tools](#Tools)   
[&nbsp;&nbsp;&nbsp;&nbsp;Maya Surfacing Projects](#Maya-Surfacing-Projects)  
[&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Hierarchical Structure](#Hierarchical-Structure)  
[&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Export Subdivisions](#Export-subdivisions)  
[&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Export](#Export)  
[&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Instances](#Instances)  
[&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Substance Painter Udims](#Substance-Painter-and-Udims)  
[&nbsp;&nbsp;&nbsp;&nbsp;Maya Surfacing Viewport](#Maya-Surfacing-Viewport)  
[&nbsp;&nbsp;&nbsp;&nbsp;txmake](#txmake)  
[&nbsp;&nbsp;&nbsp;&nbsp;Material Mapping](#Material-Mapping)  
[&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Texture Import](#Texture-Import)  
[&nbsp;&nbsp;&nbsp;&nbsp;Katana Surfacing Projects](#Katana-Surfacing-Projects)  
[Macros and Gizmos](#Macros-and-Gizmos)  
[&nbsp;&nbsp;&nbsp;&nbsp;Katana](#Katana)   
[&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Material Lookdev](#Material-Lookdev)   
[&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Render Layers](#Render-Layers)  
[&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;TextureSet Loader](#TextureSet-Loader)   
[&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Texture Locatization](#Texture-Locatization)   
[&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Interactive Filters](#Interactive-Filters)   
[&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Grey Shaders Overrides](#Grey-Shaders-Overrides)   
[&nbsp;&nbsp;&nbsp;&nbsp;Nuke](#Nuke)   
[&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;AOV correct](#AOV-Correct)   
[&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Lightgroups correct](#Lightgroups-Correct)   
[&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Lightgroups ContactSheet](#Lightgroups-ContactSheet)   
[Writing tools](#Writing-tools)   
[&nbsp;&nbsp;&nbsp;&nbsp;Example plugin](#Example-plugin)   
[Road Map](#Road-Map)   
[&nbsp;&nbsp;&nbsp;&nbsp;v0.1](#v0.1)   
[&nbsp;&nbsp;&nbsp;&nbsp;What's next](#Whats-next)   
[&nbsp;&nbsp;&nbsp;&nbsp;Trello board](#Trello-board)   
[Credits](#Credits)   

| WARNING: Under development, do not use (yet!) |
| --- |

# LookdevTools
A tool set for maya, katana, renderman, and nuke for surfacing and look development.  
It aims to be the missing glue between maya (uv prepping and organizing), mari/painter, and maya/katana rendering. Covering most of the repeatitive tasks, letting you focus on the surfacing.   
Based on my own tool box used for lookdev.

The rendering tools are based on Pixar Renderman.

# Installation
##### Root
<pre># Lookdevtools
export LOOKDEVTOOLS="/run/media/ezequielm/misc/wrk/dev/EZLookdevTools""</pre>
<pre>
# PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$LOOKDEVTOOLS"</pre>
<pre>
# Renderman RMAN
# Replace this path for your Renderman Install!!
export RMANTREE=/opt/pixar/RenderManProServer-22.5
export PATH="${PATH}:$RMANTREE/bin"
</pre>
<pre># NUKE
export NUKE_PATH=$NUKE_PATH:$LOOKDEVTOOLS/nuke/plugins</pre>
##### katana_tools
Add this to your katana launcher
<pre>## Lookdevtools
export LDT_KATANA_ROOT=$LOOKDEVTOOLS/katana
export LDT_KATANA_TOOLS=$LOOKDEVTOOLS/katana/katana_tools
export LDT_KATANA_SHELVES=$LOOKDEVTOOLS/katana/katana_shelves
export KATANA_RESOURCES=$KATANA_RESOURCES:$LDT_KATANA_TOOLS:$LDT_KATANA_SHELVES:$PB/katana_tools
</pre>
##### Mari
<pre>soon</pre>
##### Substance Painter
<pre>soon</pre>

# Tools

## Maya Surfacing Projects
This tools allows you to:
* Organize maya meshes into different surfacing projects, and surfacing objects.
* Merge meshes for surfacing
* Export alembic files for surfacing

### Hierarchical Structure
#### example
* surfacing_root
    * room 
        * Floor
            * wood
            * rug
        * walls
            * wallFront
            * wallLeft
            * skirtings
    * armChair
        * leather
            * back
            * sit
            * sides
        * wood
            * armrests
            * legs
        * blanket
            * fabricSquare
            * edgingFabric

<img width="100%" src="docs/images/mayaEZSurfacing_create.gif" alt="EZSurfacing Tools" style="" />

#### Export

The pixar cabin, and kitchens shown here ready for export and surfacing  
<img width="50%" src="docs/images/mayaEZSurfacing.png" alt="EZSurfacing Tools" style="" /><img width="50%" src="docs/images/mayaEZSurfacing2.png" alt="Surfacing Tools" style="" />

##### export example
The armchair example from above exported   
<img width="50%" src="docs/images/mayaEZSurfacing_export.gif" alt="EZSurfacing Tools" style="" /><img width="50%" src="docs/images/mayaEZSurfacingExport.png" alt="Surfacing Tools" style="" />

##### Surfacing Projects:
It exports each surfacing projects as a single alembic file, containing its SurfacingObjects. 
Tipically this is the file you will bring to Mari or Substance Painter to create a single project.

##### SurfacingObjects
At export time, meshes inside a Surfacing Object will be merged to a single mesh.
The SurfacingObject will also be exported individually to a folder, named after the SurfacingProject they belong

##### Export subdivisions
By default, the meshes will be subdivided by 2 before merging and exporting for surfacing.  
To change this setting modify this line in  
lookdevtools/common/constants.py
```
SURFACING_SUBDIV_ITERATIONS = 2
```

##### Subdivions and memory
Usually this would not be a problem. However, if you are working not on a single asset, but a set (for ei the pixarCabin), you might find memory consumption spikes at export time due to subdivided meshs.
If this is an issue, you can either export each surfacing_project individually, or optimize your scene:
* Check for high poly count objects in your scene
* Avoid adding Instances to surfacing objects, instead add the instance source.

```
As Mari is optimized for one single mesh, Surfacing Objects count inside a surfacing project is important.   
The amount of SurfacingObjects can impact your performance. The more SurfacingObjects you have inside a single  
surfacing project, the slower Mari will be.
It is not recommended using more than 8 surfacing Objects per surfacing project for Mari.
```

##### Instances
When working with instanced meshes. As much as posible, only add the intance source to the surfacing objects.   
Notice in this set maya viewport -that was entirely built with instances- how only the panels source instances are added to the surfacing objects, and not the set itself.   
<img width="100%" src="docs/images/mayaEZSurfacingInstances.jpg" alt="Surfacing Tools" style="" />

##### Substance Painter and Udims
When using the surfacing_project alembic file, and Substance Painter with udim:
*  All meshes inside an SurfacingObject, should be contained inside a single uDim  
*  Surfacing_objects should not have overlapping Uvs.   

##### Maya Surfacing Viewport

Assign materials, or wireframe colors to surfacing projects or surfacing objects to visualize them in the Viewport.

<img width="100%" src="docs/images/wireframeColor.png" alt="Surfacing Tools" style="" />

## txmake

There are plenty of txmake tools available.  
What makes this tool handy is:
- multiprocessing: Run as many simultaneous txmakes as you want. This gives a performance boost of up to 9 times faster (as tested) when converting many textures at once.
- extra arguments list.
- search texture files recursively in a given folder.

## Material mapping

Imports textures into your maya scene.

Make sure the custom template matchs your file naming convention.   
Click on Search files in folder, and the tool will -for each texture file- load its surfacing project, surfacing_object, colorspace, textureset_element name as well as what shader_plug it should be connected in a PxrSurface shader, and group them together by udim.  
Make any assignment changes in this excel like interface before importing.   
<pre>
{surfacing_project}_{surfacing_object}_{textureset_element}_{colorspace}.{UDim}.{extension}
For example:
   room_chair_baseColor_sRGB.1001.exr
</pre>

<img width="100%" src="docs/images/materialMapping.png" alt="EZSurfacing Tools" style="margin-right: 10px;" />

###### Notes
* If your file name has the {colorspace} token somewhere, the tools will create the file nodes with the correct colorspaces. OCIO partially supported, only the commonly used colorspaces.  
Valid colorspaces are:
    * sRGB
    * raw
    * linear
* The tool uses fuzzy string matching to give naming some flexibility to errors or differences, like capital letters, camel casing, or different spellings.

#### Texture Import
206 Textures, from 6 Substance Painter textureSets imported to the Pixar cabin with a single click
<img width="100%" src="docs/images/materialMappingCabin.png" alt="EZSurfacing Tools" style="margin-right: 10px;" />

## Katana Surfacing Projects

Creates collections based on the surfacing attributes found in the scene graph.
Creates materials based on the surfacing attributes
It can also assign colors in the VP, matching the colors of the maya Viewport materials and wireframe.

<img width="100%" src="docs/images/katanaEZCollections2.png" alt="EZSurfacing Tools" style="margin-right: 10px;" />

<img width="40%" src="docs/images/katanaEZCollectionsShelves.jpg" alt="EZSurfacing Tools" style="margin-right: 10px;" />

###### Note
A node must be selected before running any of this tools, this node will be used as the scene point where to process and examine the scene graph locations.   

Collections, viewport colors, and material assignments are based on attribute values at locations as in.
```
/root/world//*{attr("geometry.arbitrary.myCustomAttribute") == value
```
The attributes used from this tools are
```
geometry.arbitrary.surfacing_project
geometry.arbitrary.surfacing_object
```
It can also be used to create collections of all unique values for any given attribute.

# Macros and Gizmos

## Katana

### Material Lookdev
Isolate materials from the scene and visualize them with a shaderBall.
Use the default Shaderball (cloth geo optional), or connect your own geometry.

<img width="100%" src="docs/images/mayaEZPrmanMaterialLookdev.png" alt="EZSurfacing Tools" style="margin-right: 10px;" />

###### Note
Requires a gaffer input.

### TextureSet Loader
Loads multiple texture files using tokens or keywords.
Load materials or texture sets from substance, megascans, or mari with ease, in a single node.

Using the ```<element>``` keyword for each map, and ```_MAPID_``` for renderman to pick up uDIMs if an atlas style is selected.  
It also accepts a manifold input (of any type), for tiling.

```
Metal_PaintedSteelBase_<element>.tex   
woodenTable_<element>._MAPID_.tex
```

Each texture set element (for ie: baseColor, or normal) can be added to the list.

<img width="50%" src="docs/images/katanaPrmanTextureSet.png" alt="EZSurfacing Tools" style="margin-right: 10px;" />

### Render Layers
Render layers creation with the usual parameters we all learned to love (or to live with!).  
<img width="50%" src="docs/images/EZPrmanRenderLayer.png" alt="EZSurfacing Tools" style="margin-right: 10px;" />

This node, works in conjuntion with a variable set name, branch the layer down the graph when its more convinient for your scene.  
<img width="30%" src="docs/images/EZPrmanRenderLayerVariableSet.png" alt="EZSurfacing Tools" style="margin-right: 10px;" />

By setting the preffix, and a wildcard as ```*``` or ```*dog*```, this settings will apply to any renderlayer with that prefix, or any render layer that contains the word ```dog```.  
<img width="70%" src="docs/images/EZPrmanRenderLayerWildcard.png" alt="EZSurfacing Tools" style="margin-right: 10px;" />

All the render layers settings are stored in the scene graph as a render layer type location.  
All settings (paths, CEL and collections) get flatten as a single CEL expressions.   
Inspect your renderlayer setup CELs in the scene graph.  
<img width="40%" src="docs/images/EZPrmanRenderLayerScenegraph.png" alt="EZSurfacing Tools" style="margin-right: 10px;" />

#### Aggregate mode
In aggreate mode, you can add and remove objects (with CEL, collections, or paths) from an already set up render layer coming from above in the node graph. 

Note the ```/root/world/thisOtherLight``` in the aggregate mode and how it gets added to the original CEL expression in the render layer location attributes. 

<img width="100%" src="docs/images/EZPrmanRenderLayerAggregate.png" alt="EZSurfacing Tools" style="margin-right: 10px;" />

### Texture locatization
Opscript to search and replace paths in all PxrTexture nodes at ```.material.nodes```

<img width="50%" src="docs/images/katanaTextureLocatization.png" alt="EZSurfacing Tools" style="margin-right: 10px;" />

###### Note
Point this Opscript to /root/world/geo//*, in the case that kfls are assigned to the objects.
Or to /materials//* in case the materials are local to your scene.

### Interactive Filters
Miscelaneous interactive filters for renderman 22
* resolution half, third
* quality presets
* save n threads
* scanning options
* use it
* Integrators: occlusion, occlusion with albedo, direct lighting, and default
* subdmeshes to poly (aka: ignore subdivisions)
* Grey shader override, and diffuseColor override for all materials

<img width="50%" src="docs/images/katanaPrmanInteractiveFilters.gif" alt="EZSurfacing Tools" style="" />

##### Grey shaders overrides
###### grey_shader:
This replaces all your shaders with a 0.18 standard material. 

###### grey_albedo:
This filter overrides only the diffuseColor with a 0.18 grey color.  
Keeping all other materials features values, like specular, roughness, normals, diplacements, etc.

<img width="50%" src="docs/images/katanaPrmanInteractiveFilterGreyAlbedo.jpg"      alt="EZSurfacing Tools" style="margin-right: 10px;" />

## Nuke
### AOV Correct
Select a nuke layer, and color correct it

<img width="50%" src="docs/images/nukeAovCorrect.png"      alt="EZSurfacing Tools" style="margin-right: 10px;" />

### Lightgroups Correct
Select a lightgroup layer from the preset menu, and mute/solo/color correct it

<img width="50%" src="docs/images/nukeLigthgroupsCorrect.png"      alt="EZSurfacing Tools" style="margin-right: 10px;" />

### Lightgroups contactSheet
Creates a contact sheet of all the default lightgroups

<img width="50%" src="docs/images/nukeLigthgroupsContactSheet.jpg"      alt="EZSurfacing Tools" style="margin-right: 10px;" />

###### Note
Expects ligthgroups layers named as in: lightgroup_a, lightgroup_b, lightgroup_c. 

## Writing tools
### Developing Plugins
The toolset is based on a plugin arquitecture.  
See yapsy documentation for more info   
http://yapsy.sourceforge.net/

### Example plugin
ExamplePlugIn.plugin_layout QtWidget is what you need to populate in order to add and show an UI.

<pre>tools/plugins/example_plugin/__init__.py</pre>

```

DCC_CONTEXT = None

try:
    # Add your imports here to make sure you
    # are in the correct dcc
    DCC_CONTEXT = True
except:
    logging.warning('PLUGIN: dcc packages not found')

class ExamplePlugIn(IPlugin):
    '''Example plugin'''
    name = "Example Plugin"

    plugin_layout = None

    def __init__ (self):
        if not DCC_CONTEXT:
            logging.warning('PLUGIN: ExamplePlugIn ui not loaded, dcc libs not found')
            self.plugin_layout = QtWidgets.QWidget()
            self.label_ui = QtWidgets.QLabel(self.plugin_layout)
            self.label_ui.setText(
                'ExamplePlugIn \nPlugin not available in this Application'
                )
        else:
            self.build_ui()
    
    def build_ui(self):
        '''Builds the ui for the plugin'''
        self.plugin_layout = QtWidgets.QWidget()
        plugin_layout = QtWidgets.QVBoxLayout()

        #UI Here

        # Set main layout
        self.plugin_layout.setLayout(plugin_layout)

```

<pre>tools/plugins/example_plugin.yapsy-plugin</pre>
```
[Core]
Name = Example plugin
Module = example_plugin

[Documentation]
Author = Ezequiel Mastrasso
Version = 1.0
Website = //ezequielm.com
Description = This is an example plugin configure, with UI entry points.
```
## Road map
### v0.1
Bridging the gap between all supported applications, while giving the minimum amount of tools to do so.

### What's Next
* Some code refactoring, and clean up to do 
* Maya uv's viewport utilities
* Maya lighting, lightgroups, and aov tools
* Maya and Katana turntable lightrigs
* Nuke gizmos upgrade
* Katana texture set loader as a supertool
* Katana aov manager as a supertool

### Trello board
* Trello board

## Credits
Ezequiel Mastrasso  
Anant Gupta

### Open Source Packages

fuzzywuzzy   
lucidity   
yapsy   

### Shader Ball
Mathieu Maurel   
https://www.artstation.com/artwork/wKveZ

### Texture Patterns
Elias Wick   
https://polycount.com/discussion/186513/free-checker-pattern-texture

### Pixar cabin
Surfacing, lighting, and rendering done by Ezequiel Mastrasso.

### Pixar kitchen
Surfacing, lighting, and rendering done by Ezequiel Mastrasso.  
This images are part of the original speed surfacing exercise that give birth to these tools.  

However the look and style is based on the original winner of the pixar Kitchen challenge  
Fabio Rossi Sciedlarczyk (scied)

### Event horizon 
Modeling, Surfacing, lighting, and rendering done by Ezequiel Mastrasso.