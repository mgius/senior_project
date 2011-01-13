from os import path
# filepaths
mediadir = 'media'
spritedir = path.join(mediadir, 'sprites')
tilesdir = path.join(mediadir, 'tiles')

# Current restriction: must be a multiple of 32
mapsize = mapwidth, mapheight = 640, 640
statussize = statuswidth, statusheight = 640, 128

totalsize = (mapwidth, mapheight + statusheight)

# Current restriction: must be 30
fps = 30


