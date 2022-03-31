# By Marc Alier , https://aprendizdeluthier.com
# granludo at the gmail thing
# March 2022
# License GPLv3

from numpy import *
import ezdxf
from gcode_lib import dxf2image
from gcode_lib import intersect

class fretboard:
## implements a fretted instument (guitar, bass, ukelele, etc) fretboard
## default values, they can be modified
## all units in mm unless othewise stated
    n_frets=22
    scale=640.0 #fender
    scale_right=628 # gibson
    fret_width=0.6
    bridge_compensation = 10 # displacement of the right side of the bridge in multiscale settings
    # radius=10 #inches
    width_at_nut = 58.0
    width_at_bridge = 80.0
    nut_width = 2.0
    extra_bottom = 5.0
    frets = [] # stores array of fret positions from NUT for the left scale (low E)
    frets_right = [] # stores fret positions of the right scale (high e)
    actual_frets = []
    left_side = []
    right_side =[]
    fret_perpenticular_to_centerline =-1


    def __init__(self) :
        self.calculate()

    def calculate(self): # makes the internal calculations of the fretboard
        self.calculate_frets()
        self.calculate_sides()
        self.calculate_2dfrets()

    def calculate_sides(self): #calculates the lines corresponding with the sides of the fretboard
        self.left_side=[[-(self.width_at_nut/2),0],[-(self.width_at_bridge/2),self.scale]]
        self.right_side=[[(self.width_at_nut/2),+self.bridge_compensation],[(self.width_at_bridge/2),self.scale_right+self.bridge_compensation]]

    def calculate_2dfrets(self): #calculates the segments of the frets, from side to side
        self.actual_frets=[]
        n=0
        while n < self.n_frets:
            fret_l=self.frets[n]
            fret_r=self.frets_right[n]
            p1 = array( [-200, fret_l ]) #using 200 as a far out point to calculate the instersection, for weird instruments should be bigger
            p2 = array( [200, fret_l ])
            p1r = array( [-200, fret_r ]) #using 200 as a far out point to calculate the instersection, for weird instruments should be bigger
            p2r = array( [200, fret_r ])
            p3 = array( self.left_side[0] )
            p4 = array( self.left_side[1] )
            p5 = array( self.right_side[0] )
            p6 = array( self.right_side[1] )
            point_a = intersect.seg_intersect( p1,p2, p3,p4)
            point_b = intersect.seg_intersect( p1r,p2r, p5,p6)
            self.actual_frets.append([point_a,point_b] )
            n=n+1

        for actual in self.actual_frets:
            print(actual)

    def calculate_frets(self) : #calculates the vertical distances of the frets with relation to the centerline
    # calculates the fret positions in the fretboard, only call it if
    # some of the attributes has been modified
        self.frets=[]
        n = 0
        fret = 0
        while n<self.n_frets :
            fret=self.scale - (self.scale / pow(2,(n/12)) )
            self.frets.append(fret)
            n=n+1
        self.frets_right=[]
        n = 0
        frets_right = 0
        while n<self.n_frets :
            fret=self.scale_right - (self.scale_right / pow(2,(n/12)) )+self.bridge_compensation
            self.frets_right.append(fret)
            n=n+1
        return

    def set_fret_perpenticular_to_centerline(self,number):
        #recalculates the whole fretboard defining the bridge compensation so the fret (number) is perpenticular to the centerline
        if number > self.n_frets:
            print("Fretboard Error set_fret_perpenticular_to_centerline:fret number out of range:"+str(number))
            return
        self.bridge_compensation=0
        #calculate fret heights without compensation
        self.calculate_frets()
        self.fret_perpenticular_to_centerline=number
        lfret_from_bridge=self.scale-self.frets[number]
        rfret_from_bridge=self.scale_right-self.frets_right[number]
        self.bridge_compensation = lfret_from_bridge-rfret_from_bridge
        print("lfret_from_bridge:"+str(lfret_from_bridge))
        print("rfret_from_bridge:"+str(rfret_from_bridge))
        print("Bridge compensation:"+str(self.bridge_compensation))
        # recalculate with actual compensation
        self.calculate()

    def __str__(self) :
        temp = "Fretboard: \n Scale="+ str(self.scale) + "\n"
        n=0
        for fret in self.frets :
            temp = temp + "fret "+str(n) + " = " +str(fret) + "\n"
            n=n+1
        return temp


    def generate_dxf(self, fname) :

        model_width = 500
        model_height = 900

        doc = ezdxf.new('R2010', setup=True)
        doc.header['$INSUNITS'] = 4 #sets units to milimeters
        # Add new entities to the modelspace:
        msp = doc.modelspace()
        fret_number=0
        draw=draw_tool()
#draw centerline
        msp.add_line((0, draw.transform(-10)), (0, draw.transform(self.scale+50)),dxfattribs={"linetype": "CENTER"}) #centerline
#draw fret_perpenticular_to_centerline
        if self.fret_perpenticular_to_centerline>=0:
            msp.add_line((-100,draw.transform(self.frets[self.fret_perpenticular_to_centerline])),(100,draw.transform(self.frets[self.fret_perpenticular_to_centerline])),dxfattribs={"linetype": "CENTER"})
# draws frets,
        for fret in self.actual_frets:
            p1=fret[0]
            p2=fret[1]
            draw.draw_line(msp,p1[0],p1[1],p2[0],p2[1])
            #using 100, 200 and 20 as arbitray numbers
            if fret_number==0 :
                fret_label="NUT"
            else :
                fret_label="FRET "+str(fret_number)+": "+str(p1[1])+" mm"
                msp.add_text(fret_label).set_pos((-150, draw.transform(p1[1])), align='MIDDLE_LEFT')
                fret_label="FRET "+str(fret_number)+": "+str(p2[1])+" mm"
                msp.add_text(fret_label).set_pos((150, draw.transform(p2[1])), align='MIDDLE_RIGHT')
#            print(fret_label)
            fret_number=fret_number+1
#draws sides
        draw.draw_line(msp,self.left_side[0][0],self.left_side[0][1],self.left_side[1][0],self.left_side[1][1])
        draw.draw_line(msp,self.right_side[0][0],self.right_side[0][1],self.right_side[1][0],self.right_side[1][1])
#draws compensated bridge line
        draw.draw_line(msp,-self.width_at_bridge/2,self.scale,(self.width_at_bridge)/2,self.scale_right+self.bridge_compensation)

#writes some legends
        msp.add_text("Scale="+str(self.scale)).set_pos((110, draw.transform(-30)), align='MIDDLE_RIGHT')
        msp.add_text("Scale_2="+str(self.scale_right)).set_pos((110, draw.transform(-40)), align='MIDDLE_RIGHT')
        msp.add_text("Width at nut="+str(self.width_at_nut)).set_pos((110, draw.transform(-10)), align='MIDDLE_RIGHT')
        msp.add_text("Width at bridge="+str(self.width_at_bridge)).set_pos((110, draw.transform(-20)), align='MIDDLE_RIGHT')
        msp.add_text("==========NUT:"+str(self.width_at_nut)+"mm =========").set_pos((0, draw.transform(-10)), align='MIDDLE_CENTER')
        msp.add_text("==========BRIDGE:"+str(self.width_at_bridge)+"=========").set_pos((0, draw.transform(self.scale+10)), align='MIDDLE_CENTER')
        if self.bridge_compensation!=0 :
             msp.add_text("BRIDGE SCALE COMPENSATION:"+str(self.bridge_compensation)+" ").set_pos((self.width_at_bridge/2, draw.transform(self.scale+4)), align='MIDDLE_CENTER')
        msp.add_text("granludo/gcode on github, fretboard generator by Marc Alier @granludo").set_pos((-100,draw.transform(-30)), align='LEFT')
        msp.add_text("https://aprendideluthier.com").set_pos((-100, draw.transform(-40)), align='LEFT')
        doc.saveas(fname)

class draw_tool:
    #silly class implemented for rendering nicelly, original coords mean 0,0 is at the nut
    flip_model=-1
    offset= 750 # arbitrary number
    grid = 5
    def __init__(self):
        self.flip_model=-1

    def transform(self,y):
        return self.offset+(y*self.flip_model)

    def draw_grid(self, msp):
        if grid <0 :
            return
        n=0
        while n<600:
            msp.add_line((-300, n), (300, n),dxfattribs={"linetype": "CENTER"}) #hoizontal grid
            msp.add_line((0, n), (0, 0),dxfattribs={"linetype": "CENTER"}) #vertical grid
            n=n+self.grid

    def draw_line(self,msp,x1,y1,x2,y2) :
        y1=self.transform(y1)
        y2=self.transform(y2)
        msp.add_line((x1,y1),(x2,y2))

fretb=fretboard()
fretb.scale=650
fretb.scale_right=630
fretb.width_at_nut=35
fretb.width_at_bridge=53
fretb.set_fret_perpenticular_to_centerline(12)
filename="./output/dxf/fretboard_cameron.dxf"
fretb.generate_dxf(filename)
dxf2image.convert_dxf2img([filename],"./output/png/")
dxf2image.convert_dxf2img([filename],"./output/pdf/", img_format=".pdf")


# Create a new DXF R2010 drawing, official DXF version name: "AC1024"
