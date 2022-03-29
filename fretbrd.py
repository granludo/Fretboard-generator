# By Marc Alier , https://aprendizdeluthier.com
# granludo at the gmail thing
# March 2022
# License GPLv3

import ezdxf

class fretboard:
## implements a fretted instument (guitar, bass, ukelele, etc) fretboard
## default values, they can be modified
## all units in mm unless othewise stated
    n_frets=22
    scale=640
    # scale_right=640
    fret_width=0,6
    # radius=10 #inches
    width_at_nut = 58
    with_at_16th = 64
    extra_bottom = 5
    frets = []

    def __init__(self) :
        self.calculate_frets()

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


        model_width = 300
        model_height = 900

        doc = ezdxf.new('R2010', setup=True)
        doc.header['$INSUNITS'] = 4 #sets units to milimeters
        # Add new entities to the modelspace:
        msp = doc.modelspace()
        # Add a LINE entity
        msp.add_line((model_width/2, 0), (model_width/2, model_height)) #centerline
        fret_number=0;
        for fret in self.frets:
            msp.add_line((100,fret+20),(200,fret+20))
            #using 100, 200 and 20 as arbitray numbers
            if fret_number==0 :
                fret_label="NUT"
            else :
                fret_label="FRET "+str(fret_number)+": "+str(fret)
            msp.add_text(fret_label).set_pos((220, fret+25), align='MIDDLE_RIGHT')
    #        msp.add_text(fret_label,  dxfattribs={'style': 'LiberationSerif','height': 0.8}).set_pos((220, fret+20), align='LEFT')
            print(fret_label)
            fret_number=fret_number+1
        doc.saveas(fname)


fretb=fretboard()
fretb.generate_dxf("fretboard_test.dxf")




# Create a new DXF R2010 drawing, official DXF version name: "AC1024"
