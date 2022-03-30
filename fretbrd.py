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
    scale=640.0
    # scale_right=640
    fret_width=0.6
    # radius=10 #inches
    width_at_nut = 58.0
    width_at_bridge = 80.0
    nut_width = 2.0
    extra_bottom = 5.0
    frets = [] # stores array of fret positions from NUT
    actual_frets = []
    left_side = []
    right_side =[]


    def __init__(self) :
        self.calculate()

    def calculate(self):
        self.calculate_frets()
        self.left_side=[[-(self.width_at_nut/2),0],[-(self.width_at_bridge/2),self.scale]]
        self.right_side=[[(self.width_at_nut/2),0],[(self.width_at_bridge/2),self.scale]]
        self.calculate_2dfrets()

    def calculate_2dfrets(self):
        self.actual_frets=[]
        for fret in self.frets:
            p1 = array( [-200, fret ]) #using 200 as a far out point to calculate the instersection, for weird instruments should be bigger
            p2 = array( [200, fret ])
            p3 = array( self.left_side[0] )
            p4 = array( self.left_side[1] )
            p5 = array( self.right_side[0] )
            p6 = array( self.right_side[1] )
            point_a = intersect.seg_intersect( p1,p2, p3,p4)
            point_b = intersect.seg_intersect( p1,p2, p5,p6)
            self.actual_frets.append([point_a,point_b] )

        for actual in self.actual_frets:
            print(actual)

    def calculate_frets(self) :
    # calculates the fret positions in the fretboard, only call it if
    # some of the attributes has been modified
        self.frets=[]
        n = 0
        fret = 0
        while n<25 :
            fret=self.scale - (self.scale / pow(2,(n/12)) )
            self.frets.append(fret)
            n=n+1
        return

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
        # Add a LINE entity
        msp.add_line((0, 0), (0, self.scale+50)) #centerline
        fret_number=0;
        for fret in self.actual_frets:
            p1=fret[0]
            p2=fret[1]
            msp.add_line((p1[0],p1[1]),(p2[0],p2[1]))
            #using 100, 200 and 20 as arbitray numbers
            if fret_number==0 :
                fret_label="NUT"
            else :
                fret_label="FRET "+str(fret_number)+": "+str(p2[1])+" mm"
                msp.add_text(fret_label).set_pos((150, p1[1]), align='MIDDLE_RIGHT')
#            print(fret_label)
            fret_number=fret_number+1
        msp.add_line((self.left_side[0][0],self.left_side[0][1]),(self.left_side[1][0],self.left_side[1][1]))
        msp.add_line((self.right_side[0][0],self.right_side[0][1]),(self.right_side[1][0],self.right_side[1][1]))
        msp.add_text("Scale="+str(self.scale)).set_pos((110, -30), align='MIDDLE_RIGHT')
        msp.add_text("Width at nut="+str(self.width_at_nut)).set_pos((110, -10), align='MIDDLE_RIGHT')
        msp.add_text("Width at bridge="+str(self.width_at_bridge)).set_pos((110, -20), align='MIDDLE_RIGHT')
        msp.add_text("==========NUT:"+str(self.width_at_nut)+"mm =========").set_pos((0, -6), align='MIDDLE_CENTER')
        msp.add_text("==========BRIDGE:"+str(self.width_at_bridge)+"=========").set_pos((0, self.scale), align='MIDDLE_CENTER')
        msp.add_text("granludo/gcode on github, fretboard generator by Marc Alier @granludo").set_pos((-100, -30), align='LEFT')
        msp.add_text("https://aprendideluthier.com").set_pos((-100, -40), align='LEFT')
        doc.saveas(fname)


fretb=fretboard()
fretb.generate_dxf("./output/dxf/fretboard_test.dxf")
dxf2image.convert_dxf2img(["./output/dxf/fretboard_test.dxf"],"./output/png/")
dxf2image.convert_dxf2img(["./output/dxf/fretboard_test.dxf"],"./output/pdf/", img_format=".pdf")


# Create a new DXF R2010 drawing, official DXF version name: "AC1024"
