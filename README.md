# geometry-art

## Origins and Goals
This is a personal repo where I recreate a project I did in 2016 when I first learned the python programming language.
The original goal was to challenge myself during a tutorial video that was a bit too slow, and I ended up playing with 
the turtle package, creating visuals I liked. At the time being, I didn't know about git, and I lost the code-base, so
I decided to rewrite it, using my current knowledge about python, in order to recreate it with a better code quality
(object-oriented, with better abstraction layers, documentation, names, etc.), and to further learn about python 
(e.g. match cases, type hints and other parts of the language I didn't use a lot before).

The repo is originally just meant for organizing my work and make it accessible from anywhere, but if anyone wants 
to use / modify the code, feel free! I would be happy to welcome any new contributor!

## Basics
The base of the programs was to build polygons inscribed in other polygons, in a recursive way, which allows to create 
a sort of spiral only constituted of straight lines, but looks quite smooth. Then using color-filling, one can create 
the illusion of shading and 3D shapes. Finally, tiling multiple polygons side by side allows to trick the eyes into
forgetting about the single polygons.
I am trying to make this the most abstract possible, in order to allow any type of polygons, any filling of those, 
multiple interpolation, shading modes etc.

## Some visuals examples

### Octogon-rings with only line-color
![grafik](https://user-images.githubusercontent.com/49560513/150682942-bf6a987e-5a66-41e6-89a0-0173a2a636b8.png | width=250)

### Filled-Triangle with only line-color
![grafik](https://user-images.githubusercontent.com/49560513/150682948-532bdbb3-369d-48ca-b737-eea7f16e9735.png)

### Pavement of 4 Square-Tiles, with alterning directions
![grafik](https://user-images.githubusercontent.com/49560513/150682956-52abddb7-8157-4f60-beba-77ec3366ee8e.png)

### Pavement of 6 Triangle-Tiles, with fill-color
![grafik](https://user-images.githubusercontent.com/49560513/150682959-dd3061e9-aca6-4408-9d36-d561a868a644.png)
