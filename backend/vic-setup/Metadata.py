import os
dirpath = os.getcwd()
basinpath = dirpath + '/LandSurfaceData/ExtractData/Basin_Grid/BasinExtent.asc'
basinfile = open(basinpath, 'r')
lines = basinfile.readlines()
line = lines[0].split()
ncols = int(line[1])
line = lines[1].split()
nrows = int(line[1])
line = lines[2].split()
xllcorner = round(float(line[1]), 4)
line = lines[3].split()
yllcorner = round(float(line[1]), 4)
line = lines[4].split()
cellsize = round(float(line[1]), 4)
xrrcorner = xllcorner + cellsize*ncols
yrrcorner = yllcorner + cellsize*nrows
metainfo = str(xllcorner) + '\n' + str(yllcorner) + '\n' + str(xrrcorner) + '\n' + str(yrrcorner) + '\n' + str(cellsize) + '\n' + str(ncols) + '\n' + str(nrows)
with open('Metadata.info', 'a') as txt:
	txt.write(metainfo)
print(metainfo)
