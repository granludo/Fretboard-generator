
class gcode_gen:
## gcode_gen encapsulates the file where the gcode is output
## also echoes the code for debug purposes

    debug = 1
    G_START_SPINDLE = "M3"
    G_STOP_SPINDLE = "M5"

    file = None
    def __init__(self, filename ):
        self.file = open(filename, 'w+')

    def write(self,code):
        self.file.write(str(code)+"\n\r")
        if (self.debug):
            print("g_code:"+str(code))
        return

    def end(self):
        self.file.flush()
        self.file.close()

###############################################
class point:
## implements a point in g code (pun intended ;-) )
    x=0
    y=0
    z=0

    def __init__(self,x,y,z):
        self.x=x
        self.y=y
        self.z=z

    def __str__(self):
        return "X"+str(self.x) +" Y"+str(self.y)+" Z"+str(self.z)
