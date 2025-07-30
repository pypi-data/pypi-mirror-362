
import sys
import numpy as np
from scipy.interpolate import griddata


def polywarp(xi,yi,xo,yo,degree=1):
    """
    Fit a function of the form
    xi[k] = sum over i and j from 0 to degree of: kx[i,j] * xo[k]^i * yo[k]^j
    yi[k] = sum over i and j from 0 to degree of: ky[i,j] * xo[k]^i * yo[k]^j
    Return kx, ky
    len(xo) must be greater than or equal to (degree+1)^2
    """
    if len(xo) != len(yo) or len(xo) != len(xi) or len(xo) != len(yi):
        print("Error: length of xo, yo, xi, and yi must be the same")
        return
    if len(xo) < (degree+1.)**2.:
        print("Error: length of arrays must be greater than (degree+1)^2")
        return
    # ensure numpy arrays
    xo = np.array(xo)
    yo = np.array(yo)
    xi = np.array(xi)
    yi = np.array(yi)
    # set up some useful variables
    degree2 = (degree+1)**2
    x = np.array([xi,yi])
    u = np.array([xo,yo])
    ut = np.zeros([degree2,len(xo)])
    u2i = np.zeros(degree+1)
    for i in range(len(xo)):
        u2i[0] = 1.
        zz = u[1,i]
        for j in range(1,degree+1):
            u2i[j]=u2i[j-1]*zz
        ut[0:degree+1,i] = u2i
        for j in range(1,degree+1):
            ut[j*(degree+1):j*(degree+1)+degree+1,i]=u2i*u[0,i]**j
    uu = ut.T
    kk = np.dot(np.linalg.inv(np.dot(ut,uu).T).T,ut)
    kx = np.dot(kk,x[0,:].T).reshape(degree+1,degree+1)
    ky = np.dot(kk,x[1,:].T).reshape(degree+1,degree+1)
    return kx,ky

def poly_2d(a, kx, ky, dims=None):
    xlen, ylen = a.shape
    if dims != None:
       xlen = dims[0]
       ylen = dims[1]
    degree = len(kx)

    xi, yi = np.mgrid[0:xlen, 0:ylen]
    xo = xi
    yo = yi

    for i in np.arange(degree+1):
        for j in np.arange(degree+1):
            xo = xo + kx[j, i]*(xo**j)*(yo**i)
            yo = yo + ky[j, i]*(xo**j)*(yo**i)

    ao = griddata((xi, yi), a, (xo, yo), method='linear', fill_value=0)
    return ao
