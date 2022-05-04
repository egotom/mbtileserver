#生成 MBtiles 数据库
#import matplotlib.pyplot as plt # plt 用于显示图片
#import matplotlib.image as mpimg # mpimg 用于读取图片
#import numpy as np
from pymbtiles import  MBtiles
import os

fn = 'Satellite.mbtiles'
db = None
if os.path.exists(fn):
    db = MBtiles(fn, mode='r+')
else:
    db = MBtiles(fn, mode='w')

def addTilesEx(dirs, name=""):
    db.meta['name'] = name
    db.meta['attribution'] = ""
    db.meta['description'] = ""
    db.meta['maxzoom'] = "12"
    db.meta['minzoom'] = "0"
    db.meta['bounds'] = ""
    db.meta['center'] = "104.13689, 33.96498,10"
    db.meta['pixel_scale'] = "256"
    db.meta['format'] = "png"
    db.meta['id'] = ""
    db.meta['version'] = ""
    db.meta['maskLevel'] = ""
    db.meta['mtime'] = ""
    db.meta['planettime'] = ""    
    db.meta['json'] = ""
    db.meta['basename'] = ""

    for root, dirs, files in os.walk(dirs, topdown=False):
        for d in files:
            fn=os.path.join(root, d)            
            a = d.split("_")
            ext=os.path.splitext(d)
            if len(a) > 3 and ext[1]==".png":
                z=int(a[1])
                x=int(a[2])
                y=int(a[3][:-4])
                # print(fn)
                fp = open(fn, "rb")        
                tile_data=fp.read()
                fp.close()
                db.write_tile(z, x, y, tile_data)  
                print(fn)
                
#addTilesEx("./360Safe/","mapbox")

def t(z=12, x=1179, y=889):
    tile_data = db.read_tile(z, x, y)
    if tile_data:
        fp=open("{}_{}_{}.jpg".format(z,x,y),"wb")
        fp.write(tile_data)
        fp.close()
t()

# tiles = (
#     Tile(z=1, x=0, y=0, tile_data=first_tile),
#     ...
# )
# with MBtiles('my.mbtiles', mode='r+') as out:
    # out.write_tiles(tiles)
    # out.write_tile(z=0, x=0, y=0, tile_data)
	
# with MBtiles('trails.mbtiles') as src:
#     tile_data = src.read_tile(z=0, x=0, y=0)
#     print(tile_data)