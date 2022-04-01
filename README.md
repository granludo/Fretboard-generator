# MULTISCALE GUITAR/BASS FRETBOARD DESIGNER 
## also for any fretted stringed awesome instrument
by Marc Alier https://aprendizdeluthier.com https://www.essi.upc.edu/~ludo/
License GNU GPL 3.0
Contact: granludo (at) the gmail thing

## Files:
### fretbrd.py

Generates a stringed instrument fretoard , output in dxf, png and PDF

![sample]:(https://github.com/granludo/gcode/blob/main/output/png/fretboard_cameron.png?raw=true)

### planer_v02.py March 24th 2022
Generates GCode for a “face” operation. Starts at 0,0,0 and builds up a rectangle to max_x, max_y, 0. Clearance, bit with, overlap are in variables. No interfaces yet.

### planer_v03.py March 24th 2022
Generates GCode for a “face” operation. Starts at 0,0,0 and builds up a rectangle to max_x, max_y, 0. Clearance, bit with, overlap are in variables. No interfaces yet.
Uses the gcode_lib package




## gcode_lib package
Package with utility code
### gcode.py
Implements class gcode_gen wich should encapsulate writting gcode see planer_v03.py for example of use.

### dxf2image.py

Implements conversion of .DXF files to .PNG and PDF 
