from math import cos,sin,radians,atan

r=64.995
gap = 0.8
ang = atan(gap/r)

spots = [ ]
spots.append([25,75])
spots.append([25,65])
spots.append([35,65])
spots.append([45,65])
for i in range(6):
	spots.append([5 + i * 10,55])
for j in range(5):
   for i in range(8):
        spots.append([5 + i * 10,45 - j * 10])
for i in range(len(spots)):
        x = spots[i][0]
        y = spots[i][1] + 1.8
        spots[i][0] = x + y * sin(ang) + 101.8
        spots[i][1] = y * cos(ang) + 51.69
        


