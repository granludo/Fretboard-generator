# planer.py  v 0.2
# By Marc Alier , https://aprendizdeluthier.com
# March 2022
# Generates G CODE to plane with a CNC Machine, tested for Mach 3 .tab format
# starts from Origin X=0 Y=0 Z=0

###############################################
class GCode_Gen:
    G_START_SPINDLE = "M3"
    G_STOP_SPINDLE = "M5"

    file = None
    def __init__(self, filename ):
        self.file = open(filename, 'w+')

    def write(self,code):
        self.file.write(str(code)+"\n\r")
        print("g_code:"+str(code))
        return

    def end(self):
        self.file.flush()
        self.file.close()
###############################################
class g_point:
    x=0
    y=0
    z=0

    def __init__(self,x,y,z):
        self.x=x
        self.y=y
        self.z=z

    def __str__(self):
        return "X"+str(self.x) +" Y"+str(self.y)+" Z"+str(self.z)

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
g_code = GCode_Gen(filename)
# write a comment on tab file
g_code.write("(Planning on x from 0,0,0 with max x=" + str(max_x) + " y=" +str(max_y)+" z="+str(min_z)+" bit="+str(bit_width)+")")
g_code.write("(By Marc Alier , https://aprendizdeluthier.com)")
g_code.write("(Starts spindle)")
g_code.write(g_code.G_START_SPINDLE)

point = g_point(x,y,clear ) # Goes to starting point
g_code.write(point) # Goes to starting point

point=g_point(x,y,z)
g_code.write(point) # Goes to starting point

g_code.write("(starting planin at z="+str(z)+")")
while y < max_y:
    x=max_x
    point=g_point(x,y,z)
    g_code.write(point)
    y=y+(bit_width-overlap)
    point=g_point(x,y,z)
    g_code.write(point)
    if y < max_y:
        x=0
        point=g_point(x,y,z)
        g_code.write(point)
        y=y+(bit_width-overlap)
        point=g_point(x,y,z)
        g_code.write(point)

g_code.write("(program ending)")
point = g_point(0,0,clear )
g_code.write(point) # Goes to starting point
g_code.write("(stops spindle)")
g_code.write(g_code.G_STOP_SPINDLE)


g_code.end() #closes the file
