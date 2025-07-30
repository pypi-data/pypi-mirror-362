
from __future__ import print_function
try:
   from tkinter import *
   from tkinter.filedialog import askopenfilename, asksaveasfilename
except:
   from Tkinter import *
   from tkFileDialog import askopenfilename, asksaveasfilename
try:
    from PIL import ImageEnhance
    from PIL import ImageOps
    from PIL import ImageFilter
    from PIL import Image as pImage
except:
    import ImageEnhance
    import ImageOps
    import ImageFilter
    import Image as pImage
import sys
#import scipy.signal

try:
    from PIL.Image import ANTIALIAS
except:
    from PIL.Image import LANCZOS as ANTIALIAS

class popupShotWindow:
    def __init__(self, root):
        top = self.top = Toplevel(root)
        self.l = Label(top, text="Enter shot")
        self.l.pack()
        self.e = Entry(top)
        self.e.pack()
        self.e.bind('<Return>', self.cleanup)
        self.b = Button(top, text='Ok', command=self.cleanup)
        self.b.pack()
        self.e.focus_set()
        self.top.lift()

    def cleanup(self, event=None):
        self.value = int(self.e.get())
        self.top.destroy()


class mymenu:
    def __init__(self, root):
        menubar = Frame(root, relief=RAISED, borderwidth=4)
        menubar.pack(side=TOP, expand=NO, fill=X)
        self.makeMenuBar(menubar)
        root.bind_all("<Control-q>", self.quit)
        root.bind_all("<Control-o>", self.loadimage)
        root.bind_all("<Control-b>", self.loadbg)
        root.bind_all("<Control-d>", self.loadshotmds)
        root.bind_all("<Control-i>", self.loadshotdat)
        root.bind_all("<Control-w>", self.showwarp)
        root.bind_all("<Control-l>", self.loadwarpjson)
        root.bind_all("<Control-m>", self.loadwarpmds)
        root.bind_all("<Control-s>", self.savewarp)
        self.root = root
        return

    def makeMenuBar(self, menubar):
        mb_file = Menubutton(menubar, text='File')
        mb_file.pack(side=LEFT)
        mb_file.menu = Menu(mb_file)
        mb_file.menu.add_command(label='load image', command=self.loadimage,
                                 accelerator="Ctrl+o")
        mb_file.menu.add_command(label='load background', command=self.loadbg,
                                 accelerator="Ctrl+b")
        mb_file.menu.add_command(label='load mds shot', command=self.loadshotmds,
                                 accelerator="Ctrl+d")
        mb_file.menu.add_command(label='load savefile shot', command=self.loadshotdat,
                                 accelerator="Ctrl+i")
        mb_file.menu.add_command(label='show warp', command=self.showwarp,
                                 accelerator="Ctrl+w")
        mb_file.menu.add_command(label='load warp json', command=self.loadwarpjson,
                                 accelerator="Ctrl+l")
        mb_file.menu.add_command(label='load warp mds', command=self.loadwarpmds,
                                 accelerator="Ctrl+m")
        mb_file.menu.add_command(label='save warp', command=self.savewarp,
                                 accelerator="Ctrl+s")
        mb_file.menu.add_separator()
        mb_file.menu.add_command(label='quit', command=self.quit,
                                 accelerator="Ctrl+q")
        mb_mask = Menubutton(menubar, text='Masks')
        mb_mask.pack(side=LEFT)
        self.v = IntVar()
        mb_mask.menu = Menu(mb_mask)
        mb_mask.menu.add_radiobutton(
            label='Image only', variable=self.v, state=ACTIVE, value=0, command=self.bl)
        mb_mask.menu.add_radiobutton(
            label='BG only', variable=self.v, value=-1, command=self.bl)
        mb_mask.menu.add_separator()
        mb_mask.menu.add_radiobutton(
            label='Add', variable=self.v, value=1, command=self.bl)
        mb_mask.menu.add_radiobutton(
            label='Diff', variable=self.v, value=2, command=self.bl)
        mb_mask.menu.add_radiobutton(
            label='Darker', variable=self.v, value=3, command=self.bl)
        mb_mask.menu.add_radiobutton(
            label='Lighter', variable=self.v, value=4, command=self.bl)
        mb_mask.menu.add_radiobutton(
            label='And', variable=self.v, value=5, command=self.bl)
        mb_mask.menu.add_radiobutton(
            label='Or', variable=self.v, value=6, command=self.bl)
        mb_mask.menu.add_radiobutton(
            label='Xor', variable=self.v, value=7, command=self.bl)
        mb_mask.menu.add_radiobutton(
            label='Mult', variable=self.v, value=8, command=self.bl)
        mb_mask.menu.add_separator()
        mb_mask.menu.add_radiobutton(
            label='Blend', variable=self.v, value=9, command=self.bl)

        mb_func = Menubutton(menubar, text='Image')
        mb_func.pack(side=LEFT)
        mb_func.menu = Menu(mb_func)
        mb_func.menu.add_command(label='load image', command=self.loadimage)
        mb_func.menu.add_command(label='reset image', command=self.resetimage)
        mb_func.menu.add_command(
            label='flip image vertical', command=self.flipimv)
        mb_func.menu.add_command(
            label='flip image horizontal', command=self.flipimh)
        mb_func.menu.add_command(
            label='transpose image', command=self.transposeim)
        mb_func.menu.add_command(label='Sharpen', command=self.sharp)
        mb_func.menu.add_command(label='Blur', command=self.blur)
        mb_func.menu.add_command(label='Median 3x3', command=self.med3)
        mb_func.menu.add_command(label='Median 5x5', command=self.med5)
        mb_func.menu.add_command(label='Median 7x7', command=self.med7)
        mb_func.menu.add_command(label='Autocontrast', command=self.autoc)
        mb_func.menu.add_command(label='Equalize', command=self.equalize)
        mb_func.menu.add_command(label='FindEdges', command=self.edge)
#        mb_func.menu.add_command(label='Wiener',command=self.wiener)

        mb_bgfunc = Menubutton(menubar, text='BGImage')
        mb_bgfunc.pack(side=LEFT)
        mb_bgfunc.menu = Menu(mb_bgfunc)
        mb_bgfunc.menu.add_command(label='load bgimage', command=self.loadbg)
        mb_bgfunc.menu.add_command(label='reset bgimage', command=self.resetbg)
        mb_bgfunc.menu.add_command(
            label='flip bg vertical', command=self.flipbgv)
        mb_bgfunc.menu.add_command(
            label='flip bg horizontal', command=self.flipbgh)
        mb_bgfunc.menu.add_command(
            label='transpose bg image', command=self.transposebg)
        mb_bgfunc.menu.add_command(label='Sharpen', command=self.bgsharp)
        mb_bgfunc.menu.add_command(label='Blur', command=self.bgblur)
        mb_bgfunc.menu.add_command(label='Median 3x3', command=self.bgmed3)
        mb_bgfunc.menu.add_command(label='Median 5x5', command=self.bgmed5)
        mb_bgfunc.menu.add_command(label='Median 7x7', command=self.bgmed7)
        mb_bgfunc.menu.add_command(label='Autocontrast', command=self.bgautoc)
        mb_bgfunc.menu.add_command(label='Equalize', command=self.bgequalize)
        mb_bgfunc.menu.add_command(label='FindEdges', command=self.bgedge)

        mb_file['menu'] = mb_file.menu
        mb_mask['menu'] = mb_mask.menu
        mb_func['menu'] = mb_func.menu
        mb_bgfunc['menu'] = mb_bgfunc.menu

        return

    def addui(self, ui):
        self.ui = ui

    def loadshotmds(self, event=None):
        self.w = popupShotWindow(self.root)
        self.root.wait_window(self.w.top)
        self.ui.load_data_from_mdsplus(self.ui.mdsdata, shot=self.w.value)

    def loadshotdat(self, event=None):
        sfilename = str(askopenfilename(filetypes=[("dat", "*.dat")]))
        if sfilename != None:
            self.ui.load_data_from_savefile(sfilename=sfilename)



    def savewarp(self, event=None):
        jfilename = str(asksaveasfilename(filetypes=[("json", "*.json")]))
        if jfilename != None:
            self.ui.savewarp(jfilename=jfilename)

    def loadwarpjson(self, event=None):
        jfilename = str(askopenfilename(filetypes=[("json", "*.json")]))
        if jfilename != None:
            self.ui.loadwarpjson(jfilename=jfilename)

    def loadwarpmds(self, event=None):
        self.w = popupShotWindow(self.root)
        self.root.wait_window(self.w.top)
        self.ui.load_warp_from_mdsplus(self.ui.mdswarp, shot=self.w.value)

    def loaddatamds(self, event=None):
        self.ui.load_data_from_mdsplus(self.ui.mdsdataargs)

    def loadimage(self, event=None):
        ifilename = str(askopenfilename(filetypes=[("tiff", "*.tiff"),
                                              ("png", "*.png"),
                                              ("allfiles", "*")]))
        if ifilename != None:
            self.ui.image = pImage.open(ifilename).convert(
                'L').resize((self.ui.W, self.ui.H), ANTIALIAS)
            self.ui.buimage = self.ui.image
            self.ui.refresh()

    def showwarp(self, event=None):
        self.ui.showwarp()

    def resetimage(self):
        self.ui.image = self.ui.buimage
        self.ui.refresh()

    def resetbg(self):
        self.ui.bgimage = self.ui.bubgimage
        self.ui.transpose = False
        self.ui.vflip = False
        self.ui.hflip = False
        self.ui.refresh()

    def loadbg(self, event=None):
        ifilename = str(askopenfilename(filetypes=[("tiff", "*.tiff"),
                                              ("png", "*.png"),
                                              ("allfiles", "*")]))
        if ifilename != None:
            self.ui.bgimage = pImage.open(ifilename).convert(
                'L').resize((self.ui.W, self.ui.H), ANTIALIAS)
            self.ui.bubgimage = self.ui.bgimage
            self.ui.refresh()

    def flipimv(self):
        self.ui.image = self.ui.image.transpose(pImage.FLIP_TOP_BOTTOM)
        self.ui.refresh()

    def flipimh(self):
        self.ui.image = self.ui.image.transpose(pImage.FLIP_LEFT_RIGHT)
        self.ui.refresh()

    def transposeim(self):
        self.ui.image = self.ui.image.transpose(pImage.TRANSPOSE)
        self.ui.refresh()

    def flipbgv(self):
        if self.ui.bgimage != None:
            self.ui.bgimage = self.ui.bgimage.transpose(pImage.FLIP_TOP_BOTTOM)
            self.ui.vflip = True
            self.ui.refresh()

    def flipbgh(self):
        if self.ui.bgimage != None:
            self.ui.hflip = True
            self.ui.bgimage = self.ui.bgimage.transpose(pImage.FLIP_LEFT_RIGHT)
            self.ui.refresh()

    def transposebg(self):
        if self.ui.bgimage != None:
            self.ui.transpose = True
            self.ui.bgimage = self.ui.bgimage.transpose(pImage.TRANSPOSE)
            self.ui.refresh()

    def sharp(self):
        d = ImageEnhance.Sharpness(self.ui.image)
        self.ui.image = d.enhance(2.0)
        self.ui.refresh()

    def blur(self):
        d = ImageEnhance.Sharpness(self.ui.image)
        self.ui.image = d.enhance(0.0)
        self.ui.refresh()

    def med3(self):
        self.ui.image = self.ui.image.filter(ImageFilter.MedianFilter(3))
        self.ui.refresh()

    def med5(self):
        self.ui.image = self.ui.image.filter(ImageFilter.MedianFilter(5))
        self.ui.refresh()

    def med7(self):
        self.ui.image = self.ui.image.filter(ImageFilter.MedianFilter(7))
        self.ui.refresh()

    def autoc(self):
        self.ui.image = ImageOps.autocontrast(self.ui.image)
        self.ui.refresh()

    def equalize(self):
        self.ui.image = ImageOps.equalize(self.ui.image)
        self.ui.refresh()

    def edge(self):
        self.ui.image = self.ui.image.filter(ImageFilter.FIND_EDGES)
        self.ui.refresh()
#   def wiener(self):
#        self.ui.image =  scipy.signal.wiener(self.ui.image,[5,5],noise=None)
#        self.ui.refresh()

    def bgsharp(self):
        d = ImageEnhance.Sharpness(self.ui.bgimage)
        self.ui.bgimage = d.enhance(2.0)
        self.ui.refresh()

    def bgblur(self):
        d = ImageEnhance.Sharpness(self.ui.bgimage)
        self.ui.bgimage = d.enhance(0.0)
        self.ui.refresh()

    def bgautoc(self):
        self.ui.bgimage = ImageOps.autocontrast(self.ui.bgimage)
        self.ui.refresh()

    def bgequalize(self):
        self.ui.bgimage = ImageOps.equalize(self.ui.bgimage)
        self.ui.refresh()

    def bgedge(self):
        self.ui.bgimage = self.ui.bgimage.filter(ImageFilter.FIND_EDGES)
        self.ui.refresh()

    def bl(self):
        self.ui.bl = self.v.get()
        self.ui.refresh()

    def bgmed3(self):
        self.ui.bgimage = self.ui.bgimage.filter(ImageFilter.MedianFilter(3))
        self.ui.refresh()

    def bgmed5(self):
        self.ui.bgimage = self.ui.bgimage.filter(ImageFilter.MedianFilter(5))
        self.ui.refresh()

    def bgmed7(self):
        self.ui.bgimage = self.ui.bgimage.filter(ImageFilter.MedianFilter(7))
        self.ui.refresh()

    def quit(self, event=None):
        if self.ui.spawned:
            print(self.ui.xposentry.get(), self.ui.yposentry.get(),
                  self.ui.rposentry.get(), self.ui.xstr.get())
        sys.exit()
        return
