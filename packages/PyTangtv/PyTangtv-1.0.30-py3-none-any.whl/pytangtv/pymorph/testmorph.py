
import pytangtv
from pytangtv.pymorph import morphimage as mi
import requests
from io import BytesIO


import yaml
import numpy as np

from PIL import Image as pImage

bgurl = 'https://github.com/llnl-fesp/PyTangtv/raw/main/testfiles/bg.tiff'
response = requests.get(bgurl)
bg = pImage.open(BytesIO(response.content)).convert('L').crop((0,0,680,240))
bw,bh = bg.size
bga = np.asarray(bg)

iurl = 'https://github.com/llnl-fesp/PyTangtv/raw/main/testfiles/i.tiff'
response = requests.get(iurl)
i = pImage.open(BytesIO(response.content)).convert('L')
ia = np.asarray(i)
iw,ih = i.size

xi =  [564, 628, 531, 329, 329]
yi = [211, 152, 69, 69, 199]
xo =  [623, 700, 570, 323, 327]
yo = [574, 384, 97, 111, 544]


kx,ky = mi.polywarp(xi,yi,xo,yo,degree=1)
rkx,rky = mi.polywarp(xo,yo,xi,yi,degree=1)



pImage.fromarray(mi.poly_2d(ia,rkx,rky,dims=[bw,bh])).convert('L').show()
i.show()
pImage.fromarray(mi.poly_2d(bga,kx,ky,dims=[iw,ih])).convert('L').show()
bg.show()
