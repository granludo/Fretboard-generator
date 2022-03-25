# planer.py  v 0.3
# By Marc Alier , https://aprendizdeluthier.com
# March 2022
# Generates G CODE to plane with a CNC Machine, tested for Mach 3 .tab format
# Generates GCode for a “face” operation.
# Starts at 0,0,0 and builds up a rectangle to max_x, max_y, 0.
# Clearance, bit with, overlap are in variables. No interfaces yet.

# v3 modified to work with package .gcode_lib gcode_tools
from gcode_lib import gcode
## imports gcode_gen and g_point
###############################################
###############################################
max_x = 450
max_y = 500

#stepdown = 0.2
#finishing_pass = 1
min_z = -0.2
bit_width = 8
overlap = 1
clear = 10

z=0
x=0
y=0



filename = "planer_x"+str(max_x)+"y"+str(max_y)+"z"+str(min_z)+"bit"+str(bit_width)+".tab"
g_code = gcode.gcode_gen(filename)
# write a comment on tab file
g_code.write("(Planning on x from 0,0,0 with max x=" + str(max_x) + " y=" +str(max_y)+" z="+str(min_z)+" bit="+str(bit_width)+")")
g_code.write("(By Marc Alier , https://aprendizdeluthier.com)")
g_code.write("(Starts spindle)")
g_code.write(g_code.G_START_SPINDLE)

point = gcode.point(x,y,clear ) # Goes to starting point
g_code.write(point) # Goes to starting point

point=gcode.point(x,y,z)
g_code.write(point) # Goes to starting point

g_code.write("(starting planin at z="+str(z)+")")
while y < max_y:
    x=max_x
    point=gcode.point(x,y,z)
    g_code.write(point)
    y=y+(bit_width-overlap)
    point=gcode.point(x,y,z)
    g_code.write(point)
    if y < max_y:
        x=0
        point=gcode.point(x,y,z)
        g_code.write(point)
        y=y+(bit_width-overlap)
        point=gcode.point(x,y,z)
        g_code.write(point)

g_code.write("(program ending)")
point = gcode.point(0,0,clear )
g_code.write(point) # Goes to starting point
g_code.write("(stops spindle)")
g_code.write(g_code.G_STOP_SPINDLE)


g_code.end() #closes the file
