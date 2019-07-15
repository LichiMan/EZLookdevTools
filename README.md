# Table of Contents
[EZLookdevTools](#EZLookdevTools)  
[Installation](#Installation)   
[&nbsp;&nbsp;&nbsp;Windows](#Windows)   
[&nbsp;&nbsp;&nbsp;Linux](#Linux)   
[Maya EZSurfacing](#Maya-EZSurfacing)  
[&nbsp;&nbsp;&nbsp;Hierarchical Structure](#Hierarchical-Structure)  
[Katana Shelves](#Katana-Shelves)  
[Katana Renderman Macros](#Katana-Renderman-Macros)  
[&nbsp;&nbsp;&nbsp;MaterialLookdev](#MaterialLookdev)  
[&nbsp;&nbsp;&nbsp;TextureSet Loader](#TextureSet-Loader)  
[&nbsp;&nbsp;&nbsp;EZCollections and Materials](#EZCollections-and-Materials)  
[&nbsp;&nbsp;&nbsp;Interactive Filters](#Interactive-Filters)  
[&nbsp;&nbsp;&nbsp;Override albedo with grey](#Override-albedo-with-grey)  
[&nbsp;&nbsp;&nbsp;Texture locatization](#Texture-locatization)  
[Nuke Gizmos](#Nuke-Gizmos)  
[Credits](#Credits)  



# EZLookdevTools
A quick developed tool set for maya, katana, renderman, and nuke to surface the pixar cabin challenge

# Installation
## Windows
##### Maya EZSurfacing
<pre>set PYTHONPATH=%PYTHONPATH%;%EZ_ROOT%/maya/"</pre>
##### Katana Tools
Add this to your katana launcher
<pre>set EZ_ROOT=/path/to/EZLookdevTools/
set EZ_KATANA_TOOLS=%EZ_ROOT%/katana/katana_tools
set EZ_KATANA_SHELVES=%EZ_ROOT%/katana/katana_shelves
set KATANA_RESOURCES=%KATANA_RESOURCES%;%EZ_KATANA_TOOLS%;%EZ_KATANA_SHELVES%
set PYTHONPATH=%PYTHONPATH%;%EZ_ROOT%/katana"</pre>


##### Nuke Tools
Add the location /path/to/EZLookdevTools/nuke/nuke_gizmos to your NUKE_PATH environment variable

## Linux
##### Maya EZSurfacing
<pre>export PYTHONPATH="${PYTHONPATH}:%EZ_ROOT%/maya/"</pre>
##### Katana Tools
Add this lines to your katana launcher
<pre>export EZ_ROOT=/path/to/EZLookdevTools/
export EZ_KATANA_TOOLS=$EZ_ROOT/katana/katana_tools
export EZ_KATANA_SHELVES=$EZ_ROOT/katana/katana_shelves
export KATANA_RESOURCES=$KATANA_RESOURCES:$EZ_KATANA_TOOLS:$EZ_KATANA_SHELVES
export PYTHONPATH="${PYTHONPATH}:$EZ_ROOT/katana"</pre>
##### Nuke Tools
<pre>export NUKE_PATH=$NUKE_PATH:/path/to/EZLookdevTools/nuke/nuke_gizmos
</pre>

# Maya EZSurfacing
This tools allows you to group and organize your maya meshes into different surfacing projects, and surfacing objects.
Also handles projects export to alembic files, and surfacing objects merging.
The attributes added to the meshes transforms allows the assignment of materials and textureSets programatically (currently katana only, see katana shelves)

##### USAGE
```
import EZSurfacing.ui as EZSurfacingUI
EZSurfacingUI.show()
```

<img width="50%" src="docs/images/mayaEZSurfacing.png" alt="EZSurfacing Tools" style="" /><img width="50%" src="docs/images/mayaEZSurfacing2.png" alt="EZSurfacing Tools" style="" />
The pixar cabin, and kitchens shown here ready for surfacing

<img width="48%" src="docs/images/mayaEZSurfacing_export.gif" alt="EZSurfacing Tools" style="" /><img width="48%" src="docs/images/mayaEZSurfacing_create.gif" alt="EZSurfacing Tools" style="" />

## Hierarchical Structure
* Surfacing_projectA
  * Surfacing_objectA
    * mesh1
    * mesh2
    * mesh3
  * Surfacing_objectA
      * mesh1
      * mesh2
      * mesh3
* Surfacing_projectB
  * Surfacing_objectB
    * mesh4
    * mesh5

##### EZSurfacing_project:
This will export as single alembic.  
Tipically this is the file you will bring to mari or substance painter to create a single project.

##### EZSurfacing_Object  
Everything included inside a surfacing object will be merged to a single geometry for export.
This is specially important for Mari where the amount of different meshes can impact your performance.
The foundry states Mari is optimized for 1 single mesh.
The more more meshes, the slower Mari will be, It is not recommended using more than 6 meshes (or surfacing Objects) inside a Mari project.


##### Note
If using substance painter -using the uDim- meshes inside an EZSurfacing_Object should be contained inside a single uDim!

# Katana Shelves

# Katana Renderman Macros

## MaterialLookdev
Quickly isolate materials from the scene and visualize them.
Use the default Shaderball (cloth geo optional), or connect your own geometry.  
Requires a gaffer input.

<img width="50%" src="docs/images/mayaEZPrmanMaterialLookdev.png" alt="EZSurfacing Tools" style="margin-right: 10px;" />

## TextureSet Loader
This macro allows to load multiple texture files using tokens or keywords.
Load materials or texture sets from substance, megascans, or mari with ease, in a single node.

Using the ```<element>``` keyword for each map, and ```_MAPID_``` for renderman to pick up uDIMs if an atlas style is selected.  
It also accepts a manifold input (of any type), for tiling.

```
Metal_PaintedSteelBase_<element>.tex   
woodenTable_<element>._MAPID_.tex
```

Each texture set element (for ie: baseColor, or normal) can be added to the list.

<img width="50%" src="docs/images/katanaPrmanTextureSet.png" alt="EZSurfacing Tools" style="margin-right: 10px;" />


## EZCollections and Materials
Run EZCollections from the shelve to automaticaly create collections based on the EZ attributes found in the scene graph.
Create either the Surfacing Project, or the Surfacing Object collections.
A node must be selected before running, this node will be used as the scene point where to process and examine the scene graph locations.   

It can also be used to create collections of all unique values for any give attribute

```
import EZSurfacing as EZSurfacing

#creates EZSurfacing project collections
attribute_name = 'geometry.arbitrary.EZSurfacing_project'
EZSurfacing.create_EZ_collections(attribute_name)

#creates EZSurfacing object collections
attribute_name = 'geometry.arbitrary.EZSurfacing_object'
EZCollections = EZSurfacing.create_EZ_collections(attribute_name)

#creates a material per object collections
EZSurfacing.create_EZ_materials(attribute_name)
#creates a viewer material per object collections
EZSurfacing.create_EZ_viewer_settings(attribute_name)


```

Collections are based on attribute values at locations as in
```
/root/world//*{attr("geometry.arbitrary.myCustomAttribute") == value
```
<img width="100%" src="docs/images/katanaEZCollections2.png" alt="EZSurfacing Tools" style="margin-right: 10px;" />

## Texture locatization
Opscript to search and replace paths in all PxrTexture nodes inside a network material at scenegraph location's ```.material.nodes```

<img width="50%" src="docs/images/katanaTextureLocatization.png" alt="EZSurfacing Tools" style="margin-right: 10px;" />

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

### Override albedo with grey
Overrides only the diffuse color, keeping all other materials features

<img width="50%" src="docs/images/katanaPrmanInteractiveFilterGreyAlbedo.jpg"      alt="EZSurfacing Tools" style="margin-right: 10px;" />

# Nuke Gizmos
## Lightgroups
Soon

# Credits
## Shader Ball
Mathieu Maurel
https://www.artstation.com/artwork/wKveZ

## Texture Patterns
Elias Wick
https://polycount.com/discussion/186513/free-checker-pattern-texture