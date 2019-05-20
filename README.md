# Table of Contents
[EZLookdevTools](#EZLookdevTools)  
[Installation](#Installation)   
[&nbsp;&nbsp;&nbsp;Windows](#Windows)   
[&nbsp;&nbsp;&nbsp;Linux](#Linux)   
[Maya EZSurfacing](#Maya-EZSurfacing)  
[&nbsp;&nbsp;&nbsp;Hierarchical Structure](#Hierarchical-Structure)  
[Katana Shelves](#Katana-Shelves)  
[Katana Renderman Macros](#Katana-Renderman-Macros)  
[Nuke Gizmos](#Nuke-Gizmos)  
[Credits](#Credits)  



# EZLookdevTools
Look dev tools for maya, katana, renderman, and nuke

# Installation
## Windows
##### Maya EZSurfacing
Add the location EZLookdevTools/maya/ to your PYTHONPATH environment variable
##### Katana Tools
Add this to your katana launcher
<pre>set EZ_ROOT=/path/to/EZLookdevTools/
set EZ_KATANA_TOOLS=%EZ_ROOT%/katana/katana_tools
set EZ_KATANA_SHELVES=%EZ_ROOT%/katana/katana_shelves
set KATANA_RESOURCES=%KATANA_RESOURCES%;%EZ_KATANA_TOOLS%;%EZ_KATANA_SHELVES%</pre>

##### Nuke Tools
Add the location /path/to/EZLookdevTools/nuke/nuke_gizmos to your NUKE_PATH environment variable

## Linux
##### Maya EZSurfacing
<pre>export PYTHONPATH="${PYTHONPATH}:/path/to/EZLookdevTools/maya/"</pre>
##### Katana Tools
Add this lines to your katana launcher
<pre>export EZ_ROOT=/path/to/EZLookdevTools/
export EZ_KATANA_TOOLS=$EZ_ROOT/katana/katana_tools
export EZ_KATANA_SHELVES=$EZ_ROOT/katana/katana_shelves
export KATANA_RESOURCES=$KATANA_RESOURCES:$EZ_KATANA_TOOLS:$EZ_KATANA_SHELVES</pre>
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

<img width="100%" src="docs/images/mayaEZSurfacing.png" alt="EZSurfacing Tools" style="margin-right: 10px;" />
     
<video width="50%" controls> <source src="docs/images/mayaEZSurfacing_create.mov" type="video/mp4"> </video><video width="50%" controls> <source src="docs/images/mayaEZSurfacing_export.mov" type="video/mp4"></video>

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

# Katana SuperTools
## EZCollections
Soon  
Given a scene location path and an attribute name creates a collection for each one of the values found.
Can be used in conjuntion with the Maya EZSurface exported allembic to create collections for the surfacing projects and surfacing objects, given the attributes ```EZSurfacing_project``` or ```EZSurfacing_object```

# Katana Renderman Macros

## MaterialLookdev
Quickly isolate materials from the scene and visualize them.
Use the default Shaderball (cloth geo optional), or connect your own geometry.  
Requires a gaffer input.

<img width="50%" src="docs/images/mayaEZPrmanMaterialLookdev.png" alt="EZSurfacing Tools" style="margin-right: 10px;" />

## TextureSet Loader
This macro allows to load multiple texture files from a folder using tokens or keywords.    
Using the ```<element>``` keyword for each map, and ```_MAPID_``` for renderman to pick up uDIMs if an atlas style is selected.  
It also accepts a manifold input (of any type), for tiling.

```
Metal_PaintedSteelBase_<element>.tex   
woodenTable_<element>._MAPID_.tex
```

Each texture set element (for ie: baseColor, or normal) can be added to the list.
<img width="50%" src="docs/images/katanaPrmanTextureSet.png" alt="EZSurfacing Tools" style="margin-right: 10px;" />

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

<video width="50%" controls><source src="docs/images/katanaPrmanInteractiveFilters.mov" type="video/mp4"> </video>

### Override albedo with 0.18 grey
Overrides only the diffuse color, keeping all other materials features

<img width="50%" src="docs/images/katanaPrmanInteractiveFilerGreyAlbedo.jpg"      alt="EZSurfacing Tools" style="margin-right: 10px;" />

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