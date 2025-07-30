from __future__ import print_function
try:
   from Tkinter import *
   from tkFileDialog import askopenfilename, asksaveasfilename
   import tkMessageBox as mbox
except:
   from tkinter import *
   from tkinter.filedialog import askopenfilename, asksaveasfilename
   from tkinter import messagebox as mbox

try:
    from pathlib import Path
except:
    from pathlib2 import Path

import sys
import os
import time
#import scipy.signal
import requests,yaml
from pytangtv.pymorph import help

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

class popupUrlWindow:
    def __init__(self, root):
        top = self.top = Toplevel(root)


        self.l = Label(top, text="Enter URL")
        self.l.pack()
        self.e = Entry(top,width=80)
        self.e.pack()
        self.e.bind('<Return>', self.cleanup)
        self.e.bind('<Control-V>', self.popup_paste)
        self.e.bind("<Button-3>", self.display_popup)
        self.menu = Menu(self.e, tearoff=False)
        self.menu.add_command(label="Copy", command=self.popup_copy)
        self.menu.add_command(label="Cut", command=self.popup_cut)
        self.menu.add_separator()
        self.menu.add_command(label="Paste", command=self.popup_paste)
        self.b = Button(top, text='Ok', command=self.cleanup)
        self.b.pack()
        self.e.focus_set()
        self.top.lift()

    def display_popup(self, event):
        self.menu.post(event.x_root, event.y_root)

    def popup_copy(self):
        self.e.event_generate("<<Copy>>")

    def popup_cut(self):
        self.e.event_generate("<<Cut>>")

    def popup_paste(self):
        self.e.event_generate("<<Paste>>")


    def cleanup(self, event=None):
        self.value = str(self.e.get())
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
        root.bind_all("<Control-y>", self.loadwarpyaml)
        root.bind_all("<Control-m>", self.loadwarpmds)
        #root.bind_all("<Control-m>", self.loadwarpsave)
        root.bind_all("<Control-t>", self.savewarpjson)
        root.bind_all("<Control-s>", self.savewarpyaml)
        self.root = root
        return

    def makeMenuBar(self, menubar):
        mb_file = Menubutton(menubar, text='File')
        mb_file.pack(side=LEFT)
        mb_file.menu = Menu(mb_file)
        mb_file.menu.add_command(label='download config', command=self.getconfig)
        mb_file.menu.add_command(label='show warp', command=self.showwarp,
                                 accelerator="Ctrl+w")
        mb_file.menu.add_command(label='load warp yaml', command=self.loadwarpyaml,
                                 accelerator="Ctrl+y")
        mb_file.menu.add_command(label='load warp json', command=self.loadwarpjson,
                                 accelerator="Ctrl+l")
        mb_file.menu.add_command(label='load warp mds', command=self.loadwarpmds,
                                 accelerator="Ctrl+m")
        mb_file.menu.add_command(label='load warp save', command=self.loadwarpsave)
        mb_file.menu.add_command(label='save warp yaml', command=self.savewarpyaml,
                                 accelerator="Ctrl+s")
        mb_file.menu.add_command(label='save warp json', command=self.savewarpjson,
                                 accelerator="Ctrl+t")
        mb_file.menu.add_command(label='save final image', command=self.savefinal,
                                 accelerator="Ctrl+s")
        mb_file.menu.add_separator()
        mb_file.menu.add_command(label='quit', command=self.quit,
                                 accelerator="Ctrl+q")

        mb_edit = Menubutton(menubar, text='Edit')
        mb_edit.pack(side=LEFT)
        mb_edit.menu = Menu(mb_edit)
        mb_edit.menu.add_command(label='undo pt',command=self.undolast,accelerator="Ctrl-z")

        mb_mask = Menubutton(menubar, text='Layers')
        mb_mask.pack(side=LEFT)
        self.v = IntVar()
        mb_mask.menu = Menu(mb_mask)
        mb_mask.menu.add_radiobutton(
            label='FG only', variable=self.v, state=ACTIVE, value=0, command=self.bl)
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
        _m = mb_mask.menu.add_radiobutton(
            label='Blend', variable=self.v, value=9, command=self.bl)

        mb_func = Menubutton(menubar, text='FGImage')
        mb_func.pack(side=LEFT)
        mb_func.menu = Menu(mb_func)
        mb_func.menu.add_command(label='load image', command=self.loadimage)
        mb_func.menu.add_command(label='load url', command=self.loadurl)
        mb_func.menu.add_command(label='load mds shot', command=self.loadshotmds,
                                 accelerator="Ctrl+d")
        mb_func.menu.add_command(label='load savefile shot', command=self.loadshotdat,
                                 accelerator="Ctrl+i")
        mb_func.menu.add_command(label='save image', command=self.saveimage)
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
        mb_bgfunc.menu.add_command(label='load image', command=self.loadbg)
        mb_bgfunc.menu.add_command(label='load url', command=self.loadburl)
        mb_bgfunc.menu.add_command(label='load mds shot', command=self.loadbgshotmds)
        mb_bgfunc.menu.add_command(label='load savefile shot', command=self.loadbgshotdat)
        mb_bgfunc.menu.add_command(label='save image', command=self.savebg)
        mb_bgfunc.menu.add_command(label='reset image', command=self.resetbg)
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

        mb_hfunc = Menubutton(menubar, text='Help')
        mb_hfunc.pack(side=RIGHT)
        mb_hfunc.menu = Menu(mb_hfunc)
        mb_hfunc.menu.add_command(label='Help', command=self.help)
        mb_hfunc.menu.add_command(label='Check for updates', command=self.update)
        mb_hfunc.menu.add_separator()
        mb_hfunc.menu.add_command(label='About', command=self.showvers)

        mb_file['menu'] = mb_file.menu
        mb_edit['menu'] = mb_edit.menu
        mb_mask['menu'] = mb_mask.menu
        mb_func['menu'] = mb_func.menu
        mb_bgfunc['menu'] = mb_bgfunc.menu
        mb_hfunc['menu'] = mb_hfunc.menu

        return

    def addui(self, ui):
        self.ui = ui

    def getconfig(self):
        url = 'https://github.com/llnl-fesp/PyTangtv/raw/main/pytangtv/pymorph/pymorph.yaml'
        response = requests.get(url)
        config = yaml.safe_load(response.content.decode("utf-8"))
        with open(str(Path.home())+'/.pymorph.yaml', 'w') as outfile:
             outfile.write("# \n")
             outfile.write("# Written by "+os.getlogin()+"\n")
             outfile.write("# on  "+time.ctime()+"\n")
             outfile.write("# \n")
             yaml.dump(config, outfile,indent=4,default_flow_style=False)


    def loadshotmds(self, event=None):
        self.w = popupShotWindow(self.root)
        self.root.wait_window(self.w.top)
        self.ui.fimage.load_data_from_mdsplus(shot=self.w.value)
        self.ui.updateranges()
        self.ui.refresh()

    def loadshotdat(self, event=None):
        sfilename = str(askopenfilename(filetypes=[("dat", "*.dat")]))
        if sfilename != None:
            self.ui.fimage.load_data_from_savefile(sfilename=sfilename)
        self.ui.updateranges()
        self.ui.refresh()


    def savewarpyaml(self, event=None):
        yfilename = str(asksaveasfilename(filetypes=[("yaml", "*.yaml")]))
        if yfilename != None:
            self.ui.savewarpyaml(yfilename=yfilename)

    def savewarpjson(self, event=None):
        jfilename = str(asksaveasfilename(filetypes=[("json", "*.json")]))
        if jfilename != None:
            self.ui.savewarpjson(jfilename=jfilename)

    def loadwarpyaml(self, event=None):
        yfilename = str(askopenfilename(filetypes=[("yaml", "*.yaml")]))
        if yfilename != None:
            self.ui.loadwarpyaml(yfilename=yfilename)

    def loadwarpjson(self, event=None):
        jfilename = str(askopenfilename(filetypes=[("json", "*.json")]))
        if jfilename != None:
            self.ui.loadwarpjson(jfilename=jfilename)
        self.ui.refresh()

    def loadwarpmds(self, event=None):
        self.w = popupShotWindow(self.root)
        self.root.wait_window(self.w.top)
        print(self.w.value)
        self.ui.load_warp_from_mdsplus(shot=self.w.value)
        self.ui.refresh()

    def loadwarpsave(self, event=None):
        wfilename = str(askopenfilename(filetypes=[("dat", "*.dat")]))
        if wfilename != None:
            self.ui.load_warp_from_savefile(wfilename)
        self.ui.refresh()

    def loadurl(self, event=None):
        self.w = popupUrlWindow(self.root)
        self.root.wait_window(self.w.top)
        self.ui.fimage.loadurl(url=self.w.value)
        self.ui.updateranges()
        self.ui.refresh()

    def loadimage(self, event=None):
        self.ui.fimage.loadimage()
        self.ui.updateranges()
        self.ui.updateranges()
        self.ui.refresh()

    def showwarp(self, event=None):
        self.ui.showwarp()

    def showvers(self, event=None):
        self.ui.showvers()

    def resetimage(self):
        self.ui.fimage.reset()
        self.ui.refresh()

    def resetbg(self):
        self.ui.bgimage.reset()
        self.ui.refresh()

    def undolast(self):
        self.ui.undolast()
        self.ui.refresh()

    def saveimage(self, event=None):
        ifilename = str(asksaveasfilename(filetypes=[("tiff", ".tif .tiff"),
                                              ("png", "*.png"),
                                              ("jpg", "*.jpg")]))
        if ifilename != None:
            self.ui.im1.save(ifilename)
    def savefinal(self, event=None):
        ifilename = str(asksaveasfilename(filetypes=[("tiff", ".tif .tiff"),
                                              ("png", "*.png"),
                                              ("jpg", "*.jpg")]))
        if ifilename != None:
            self.ui.simage.save(ifilename)
    def savebg(self, event=None):
        ifilename = str(asksaveasfilename(filetypes=[("tiff", ".tif .tiff"),
                                              ("png", "*.png"),
                                              ("jpg", "*.jpg")]))
        if ifilename != None:
            self.ui.im2.save(ifilename)

    def loadbg(self, event=None):
        self.ui.bgimage.loadimage()
        self.ui.updateranges()
        self.ui.refresh()

    def loadburl(self, event=None):
        self.w = popupUrlWindow(self.root)
        self.root.wait_window(self.w.top)
        self.ui.bgimage.loadurl(url=self.w.value)
        self.ui.updateranges()
        self.ui.refresh()

    def loadbgshotmds(self, event=None):
        self.w = popupShotWindow(self.root)
        self.root.wait_window(self.w.top)
        self.ui.bgimage.load_data_from_mdsplus(shot=self.w.value)
        self.ui.updateranges()
        self.ui.refresh()

    def loadbgshotdat(self, event=None):
        sfilename = str(askopenfilename(filetypes=[("dat", "*.dat")]))
        if sfilename != None:
            self.ui.bgimage.load_data_from_savefile(sfilename=sfilename)
        self.ui.updateranges()
        self.ui.refresh()


    def flipimv(self):
        if self.ui.fimage != None:
           self.ui.fimage.dovflip()
           self.ui.refresh()

    def flipimh(self):
        if self.ui.fimage != None:
           self.ui.fimage.dohflip()
           self.ui.refresh()

    def transposeim(self):
        if self.ui.fimage != None:
           self.ui.fimage.dotranspose()
           self.ui.refresh()

    def flipbgv(self):
        if self.ui.bgimage != None:
            self.ui.bgimage.dovflip()
            self.ui.refresh()

    def flipbgh(self):
        if self.ui.bgimage != None:
            self.ui.bgimage.dohflip()
            self.ui.refresh()

    def transposebg(self):
        if self.ui.bgimage != None:
            self.ui.bgimage.dotranspose()
            self.ui.refresh()

    def sharp(self):
        self.ui.fimage.sharp()
        self.ui.refresh()

    def blur(self):
        self.ui.fimage.blur()
        self.ui.refresh()

    def med3(self):
        self.ui.fimage.med3()
        self.ui.refresh()

    def med5(self):
        self.ui.fimage.med5()
        self.ui.refresh()

    def med7(self):
        self.ui.fimage.med7()
        self.ui.refresh()

    def autoc(self):
        self.ui.fimage.autoc()
        self.ui.refresh()

    def equalize(self):
        self.ui.fimage.equalize()
        self.ui.refresh()

    def edge(self):
        self.ui.fimage.edge()
        self.ui.refresh()

    def bgsharp(self):
        self.ui.bgimage.sharp()
        self.ui.refresh()

    def bgblur(self):
        self.ui.bgimage.blur()
        self.ui.refresh()

    def bgautoc(self):
        self.ui.bgimage.autoc()
        self.ui.refresh()

    def bgequalize(self):
        self.ui.bgimage.equalize()
        self.ui.refresh()

    def bgedge(self):
        self.ui.bgimage.edge()
        self.ui.refresh()

    def bl(self):
        self.ui.bl = self.v.get()
        self.ui.refresh()

    def bgmed3(self):
        self.ui.bgimage.med3()
        self.ui.refresh()

    def bgmed5(self):
        self.ui.bgimage.med5()
        self.ui.refresh()

    def bgmed7(self):
        self.ui.bgimage.med7()
        self.ui.refresh()

    def quit(self, event=None):
        sys.exit()
        return

    def help(self):
        self.w = help.popupHelpWindow(self.root)
        self.root.wait_window(self.w.top)

    def update(self):
        self.w = help.popupUpdateWindow(self.root)
        self.root.wait_window(self.w.top)

