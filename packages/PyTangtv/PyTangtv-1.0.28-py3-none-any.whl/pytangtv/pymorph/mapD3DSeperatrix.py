from matplotlib import pyplot as plt
from matplotlib import markers
from scipy.io import readsav
import numpy as np
import json
from pytangtv.pymorph import morphimage as mi
import MDSplus as mds
import ctypes as ct

c_float_p = ct.POINTER(ct.c_float)
c_int_p = ct.POINTER(ct.c_int)

shlib = ct.CDLL('/usr/local/diags/tangtv/lib/idlbracket.so')
shlib.bracket_list.restype = ct.c_int
shlib.bracket_list.argtypes = [
        c_float_p,c_float_p,ct.c_int,c_float_p,c_float_p,
        ct.c_int,ct.c_int,c_int_p,c_int_p ]
        

def bracket_list(r0,z0,ri,zi):
        numpts = len(r0)
        ylen,xlen = ri.shape
        rl = np.array(r0,dtype=np.float32)
        zl = np.array(z0,dtype=np.float32)
        xind = (2*numpts * ct.c_int)()
        yind = (2*numpts * ct.c_int)()
        shlib.bracket_list(rl.ctypes.data_as(c_float_p),
                           zl.ctypes.data_as(c_float_p),
                           ct.c_int(numpts),
                           ri.astype(np.float32).ctypes.data_as(c_float_p),
                           zi.astype(np.float32).ctypes.data_as(c_float_p),
                           ct.c_int(xlen),ct.c_int(ylen),
                           ct.cast(xind,c_int_p),ct.cast(yind,c_int_p))
        xa = np.array(xind[0:2*numpts])
        ya = np.array(yind[0:2*numpts])
        ongrid = xa >= 0
        return (xa[ongrid],ya[ongrid])


def mapD3DSeperatrix(shot,time,geom,warp=None,runid='efit01',server=None,tree=None,vflip=False,hflip=False):



   geom = readsav(geom)['geom']

   rendered=geom['rendered'][0]
   imylen,imxlen = rendered.shape 
   wf=geom['wireframe'][0]
   ri=geom['rimpact'][0]
   zi=geom['zimpact'][0]
   phii=geom['phiimpact'][0]

   if server == None:
      s = mds.Connection('atlas.gat.com')
   else:
      s = server

   if tree == None:
      efit01 = s.openTree(runid,shot)

   atime = s.get('\ATIME')
   zmaxis = s.get('\ZMAXIS')*100
   rmidin = s.get('\RMIDIN')*100
   rmidout = s.get('\RMIDOUT')*100
   bdry = s.get('\BDRY').value*100
   rxpt1 = s.get('\RXPT1')*100
   zxpt1 = s.get('\ZXPT1')*100
   rxpt2 = s.get('\RXPT2')*100
   zxpt2 = s.get('\ZXPT2')*100
   rvsin = s.get('\RVSIN')*100
   zvsin = s.get('\ZVSIN')*100
   rvsout = s.get('\RVSOUT')*100
   zvsout = s.get('\ZVSOUT')*100

   if tree == None:
      s.closeTree(runid,shot)

   i = np.where(atime > time)
   j = i[0][0]

   rpts = [float(rmidin[j]),float(rmidout[j])]
   zpts = [float(zmaxis[j]),float(zmaxis[j])]
   xmid,ymid = bracket_list(rpts,zpts,ri,zi)

   xbdry,ybdry = bracket_list(bdry[i,0][0],bdry[i,1][0],ri,zi)
   bdry = bdry[j]
   i = np.where(bdry[:,0] > 0)
   xbdry,ybdry = bracket_list(bdry[i,0][0],bdry[i,1][0],ri,zi)

   if rxpt1[j] > 0 and zvsin[j] < 0:
      rxpt = rxpt1
      zxpt = zxpt1
   elif rxpt2[j] > 0 and zvsin[j] > 0:
      rxpt = rxpt2
      zxpt = zxpt2

   inrleg = [float(rxpt[j]),float(rvsin[j])]
   inzleg = [float(zxpt[j]),float(zvsin[j])]
   xinleg,yinleg = bracket_list(inrleg,inzleg,ri,zi)

   outrleg = [float(rxpt[j]),float(rvsout[j])]
   outzleg = [float(zxpt[j]),float(zvsout[j])]
   xoutleg,youtleg = bracket_list(outrleg,outzleg,ri,zi)

   if warp != None:
      with open(warp,'r') as f:
          warp = json.load(f)
      xo = warp['xo']
      yo = warp['yo']
      xi = warp['xi']
      yi = warp['yi']
      if not vflip:
         for i in range(len(yi)):
            yi[i] = imylen - yi[i] - 1
      if hflip:
         for i in range(len(xi)):
            xi[i] = imxlen - xi[i] - 1
           
      kx,ky = mi.polywarp(xo,yo,xi,yi,warp['degree'])
      wxbdry,wybdry = mi.poly_pts(xbdry,ybdry,kx,ky)
      wxinleg,wyinleg = mi.poly_pts(xinleg,yinleg,kx,ky)
      wxoutleg,wyoutleg = mi.poly_pts(xoutleg,youtleg,kx,ky)
      wxmid,wymid = mi.poly_pts(xmid,ymid,kx,ky)
      return wxbdry,wybdry,wxinleg,wyinleg,wxoutleg,wyoutleg,wxmid,wymid
   else:
      return xbdry,ybdry,xinleg,yinleg,xoutleg,youtleg,xmid,ymid



def mapSurface(r0,z0,geom,warp=None,vflip=False,hflip=False):
   geom = readsav(geom)['geom']
   rendered=geom['rendered'][0]
   imylen,imxlen = rendered.shape 
   ri=geom['rimpact'][0]
   zi=geom['zimpact'][0]

   xsurf,ysurf = bracket_list(r0,z0,ri,zi)

   if warp != None:
      with open(warp,'r') as f:
          warp = json.load(f)
      xo = warp['xo']
      yo = warp['yo']
      xi = warp['xi']
      yi = warp['yi']
      if not vflip:
         for i in range(len(yi)):
            yi[i] = imylen - yi[i] - 1
      if hflip:
         for i in range(len(xi)):
            xi[i] = imxlen - xi[i] - 1
           
      kx,ky = mi.polywarp(xo,yo,xi,yi,warp['degree'])
      wxsurf,wysurf = mi.poly_pts(xsurf,ysurf,kx,ky)
      return wxsurf,wysurf
   else:
      return xsurf,ysurf
