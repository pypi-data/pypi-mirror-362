
from pytangtv.check4updates import check4updates,updatemsgs

try:
   from Tkinter import *
   from tkFileDialog import askopenfilename, asksaveasfilename
   import tkMessageBox as mbox
except:
   from tkinter import *
   from tkinter.filedialog import askopenfilename, asksaveasfilename
   from tkinter import messagebox as mbox

helpmsg = """

    PyMorph helps users select control points to determine the polynomial
    cooeficients (kx,ky) for the following warping equation.

      xi[k] = sum over i and j from 0 to degree of: kx[i,j] * xo[k]^i * yo[k]^j
      yi[k] = sum over i and j from 0 to degree of: ky[i,j] * xo[k]^i * yo[k]^j

      The general workflow is as follows:

      1) Load the two layers with images from commandline or the 
         FGImage and BGImage menus.

      2) Process the images to highlight fiducials. Use the FGImage and
         BGImage menus. Also change contrast with the "Image range" entry
         boxes in the main window.

      3) Overlay the two layers using a selection from the Layers menu. 
         Check out the Blend selection. Use the slider to adjust the 
         relative blend of the layers .

      4) Select a Direction. 
         Forward - morph foreground image to background
         Reverse - morph background image to foreground
     
      5) Select points by mouse clicking on image to be morphed and 
         and dragging to the corresponding feature in the image to 
         be matched. Release mouse button. You will see a red dot on
         the one image and a blue dot on the second image. Repeat 
         until you have four dot pairs (for degree poly 1).

      6) Add points as needed to get a good morph across the image.

      7) Click "Morph off/Morph on" button to turn on morphing. 
         Button will display "Add more pts" when more control points
         are needed to solve for polynomial coeficients. The 
         number of points needed is (n+1)^2 for degree n polynomial.


          """



class popupHelpWindow:
    def __init__(self, root):
        top = self.top = Toplevel(root)
        self.l = Label(top, text="Pymorph help")
        self.l.pack()
        self.t = Text(top,height=40)
        self.t.pack()
        self.t.insert('1.0',helpmsg)
        self.b = Button(top, text='Ok', command=self.cleanup)
        self.b.pack()
        self.top.lift()

    def paste(self, event=None):
        print(event)

    def cleanup(self, event=None):
        self.top.destroy()

class popupUpdateWindow:
    def __init__(self, root):
        from importlib import metadata
        top = self.top = Toplevel(root)
        self.l = Label(top, text="Pymorph check for updates")
        self.l.pack()
        self.t = Text(top,height=10)
        self.t.pack()
        self.top.lift()
        try:
            _version = metadata.version('PyTangtv')
        except:
            _version = 'Version unknown'
        msg = updatemsgs('https://pypi.org/pypi/pytangtv/json', thisver=_version)

        self.t.insert('1.0',msg)
        self.b = Button(top, text='Ok', command=self.cleanup)
        self.b.pack()
   
    def paste(self, event=None):
        print(event)

    def cleanup(self, event=None):
        self.top.destroy()

