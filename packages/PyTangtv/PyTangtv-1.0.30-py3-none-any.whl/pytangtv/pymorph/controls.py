
import pytangtv
import os
try:
   from tkinter import *
except:
   from Tkinter import *
from idlelib.tooltip import Hovertip

thisfile=os.path.realpath(pytangtv.__file__)
thispath=os.path.dirname(thisfile)
bitmaps=thispath+'/bitmaps/'


class controls:
    def __init__(self,parent,ui):
        tiptopframe = Frame(parent)
        tiptopframe.pack(side=TOP,fill=BOTH)
        topframe = Frame(tiptopframe)
        topframe.pack(side=LEFT)
        frame = Frame(topframe)
        frame.pack(side=LEFT)

        up = Button(frame,bitmap='@'+bitmaps+'up.xbm',
             command=ui.upstep)
        up.pack(side=TOP)
        Hovertip(up,'Shift control points\nup.')

        frame2 = Frame(frame)
        frame2.pack(side=TOP)
        left = Button(frame2,bitmap='@'+bitmaps+'left.xbm',
            command=ui.leftstep)
        left.pack(side=LEFT)
        Hovertip(left,'Shift control points\nto the left.')
        right = Button(frame2,bitmap='@'+bitmaps+'right.xbm',
             command=ui.rightstep)
        right.pack(side=LEFT)
        Hovertip(right,'Shift control points\nto the right.')
        down = Button(frame,bitmap='@'+bitmaps+'down.xbm',
             command=ui.downstep)
        down.pack(side=TOP)
        Hovertip(down,'Shift control points\ndown.')
        frame2 = Frame(frame)
        frame2.pack(side=TOP)
        rotl = Button(frame2,bitmap='@'+bitmaps+'rotl.xbm',command=ui.rotl)
        rotl.pack(side=LEFT)
        Hovertip(rotl,'Rotate control points\ncounter-clock.')
        rotr = Button(frame2,bitmap='@'+bitmaps+'rotr.xbm',command=ui.rotr)
        rotr.pack(side=LEFT)
        Hovertip(rotr,'Rotate control points clockwise.')

        _b = Button(frame,text="Reset",command=ui.reset)
        _b.pack(side=TOP)
        Hovertip(_b,'Set image layers\nback to as loaded.')
        _b = Button(frame,text="Refresh",command=ui.refresh)
        _b.pack(side=TOP)
        Hovertip(_b,'Refresh display.')


        frame = Frame(topframe)
        frame.pack(side=LEFT)
        frame2 = Frame(frame)
        frame2.pack(side=TOP)
        _l = Label(frame2,text='X Step')
        _l.pack(side=LEFT)
        Hovertip(_l,'Step size when\nshifting pts horizontally.')
        ui.xstepentry = Entry(frame2,width=10)
        ui.xstepentry.insert(0,"%d" % ui.hstep)
        ui.xstepentry.pack(side=RIGHT,padx=2,pady=2)

        frame2 = Frame(frame)
        frame2.pack(side=TOP)
        _l = Label(frame2,text='Y Step')
        _l.pack(side=LEFT)
        Hovertip(_l,'Step size when\nshifting pts vertically.')
        ui.ystepentry = Entry(frame2,width=10)
        ui.ystepentry.insert(0,"%d" % ui.vstep)
        ui.ystepentry.pack(side=RIGHT,padx=2,pady=2)

        frame2 = Frame(frame)
        frame2.pack(side=TOP)
        _l=Label(frame2,text='Rot Step')
        _l.pack(side=LEFT)
        Hovertip(_l,'Step size when\nrotating  pts.')
        ui.rstepentry = Entry(frame2,width=10)
        ui.rstepentry.insert(0,"%d" % ui.rstep)
        ui.rstepentry.pack(side=RIGHT,padx=2,pady=2)

        _l=Label(parent,text='FGImage and BGImage Merge control')
        _l.pack(side=TOP)
        _m = """
              Determines how the foreground (top) 
              and background (bottom) image overlay 
              is displayed. Only used for Layers/Blend.

                 0 - Foreground only
                 1 - Background only
                 """
        Hovertip(_l,_m)
        ui.scale = Scale(parent,from_=0, to=1,resolution=0.02,orient=HORIZONTAL,command=ui.refreshcb)
        ui.scale.pack(side=TOP,expand=FALSE,fill=X)
                
