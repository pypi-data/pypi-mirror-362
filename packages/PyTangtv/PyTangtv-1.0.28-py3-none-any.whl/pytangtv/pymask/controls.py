
import os
try:
    from tkinter import *
except:
    from Tkinter import *

thisfile=os.path.realpath(__file__)
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

        frame2 = Frame(frame)
        frame2.pack(side=TOP)
        left = Button(frame2,bitmap='@'+bitmaps+'left.xbm',
            command=ui.leftstep)
        left.pack(side=LEFT)
        right = Button(frame2,bitmap='@'+bitmaps+'right.xbm',
             command=ui.rightstep)
        right.pack(side=LEFT)
        down = Button(frame,bitmap='@'+bitmaps+'down.xbm',
             command=ui.downstep)
        down.pack(side=TOP)
        frame2 = Frame(frame)
        frame2.pack(side=TOP)
        rotl = Button(frame2,bitmap='@'+bitmaps+'rotl.xbm',command=ui.rotl)
        rotl.pack(side=LEFT)
        rotr = Button(frame2,bitmap='@'+bitmaps+'rotr.xbm',command=ui.rotr)
        rotr.pack(side=LEFT)

        Button(frame,text="Reset",command=ui.reset).pack(side=TOP)
        Button(frame,text="Refresh",command=ui.refresh).pack(side=TOP)
        Button(frame,text="Write",command=ui.iwrite).pack(side=TOP)


        frame = Frame(topframe)
        frame.pack(side=LEFT)
        frame2 = Frame(frame)
        frame2.pack(side=TOP)
        Label(frame2,text='X Step').pack(side=LEFT)
        ui.xstepentry = Entry(frame2,width=10)
        ui.xstepentry.insert(0,"%d" % ui.hstep)
        ui.xstepentry.pack(side=RIGHT,padx=2,pady=2)

        frame2 = Frame(frame)
        frame2.pack(side=TOP)
        Label(frame2,text='X Pos').pack(side=LEFT)
        ui.xposentry = Entry(frame2,width=10)
        ui.xposentry.insert(0,"%d" % ui.hpos)
        ui.xposentry.pack(side=RIGHT,padx=2,pady=2)

        frame2 = Frame(frame)
        frame2.pack(side=TOP)
        Label(frame2,text='Y Step').pack(side=LEFT)
        ui.ystepentry = Entry(frame2,width=10)
        ui.ystepentry.insert(0,"%d" % ui.vstep)
        ui.ystepentry.pack(side=RIGHT,padx=2,pady=2)

        frame2 = Frame(frame)
        frame2.pack(side=TOP)
        Label(frame2,text='Y Pos').pack(side=LEFT)
        ui.yposentry = Entry(frame2,width=10)
        ui.yposentry.insert(0,"%d" % ui.hpos)
        ui.yposentry.pack(side=RIGHT,padx=2,pady=2)

        frame2 = Frame(frame)
        frame2.pack(side=TOP)
        Label(frame2,text='Rot Step').pack(side=LEFT)
        ui.rstepentry = Entry(frame2,width=10)
        ui.rstepentry.insert(0,"%d" % ui.rstep)
        ui.rstepentry.pack(side=RIGHT,padx=2,pady=2)

        frame2 = Frame(frame)
        frame2.pack(side=TOP)
        Label(frame2,text='Rotation').pack(side=LEFT)
        ui.rposentry = Entry(frame2,width=10)
        ui.rposentry.insert(0,"%d" % ui.rot)
        ui.rposentry.pack(side=TOP,padx=2,pady=2)

        frame2 = Frame(frame)
        frame2.pack(side=TOP)
        Label(frame2,text='Stretch').pack(side=LEFT)
        ui.xstr = Entry(frame2,width=10)
        ui.xstr.insert(0,'1.0')
        ui.xstr.pack(side=TOP,padx=2,pady=2)

        frame2 = Frame(frame)
        frame2.pack(side=TOP)
        Label(frame2,text='YStretch').pack(side=LEFT)
        ui.ystr = Entry(frame2,width=10)
        ui.ystr.insert(0,'1.0')
        ui.ystr.pack(side=TOP,padx=2,pady=2)

        Label(parent,text='Image and Background Merge control').pack(side=TOP)
        ui.scale = Scale(parent,from_=0, to=1,resolution=0.02,orient=HORIZONTAL,command=ui.refreshcb)
        ui.scale.pack(side=TOP,expand=FALSE,fill=X)
                
