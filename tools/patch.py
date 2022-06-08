import requests
from pymbtiles import  MBtiles,Tile
import sqlite3,random

dbFile = '../tilesets/bing.mbtiles'
con = sqlite3.connect(dbFile)
cur = con.cursor()

def generateQuadKey(x, y, z):
	quadKey = []
	for i in range(z,0,-1):
		digit = 0
		mask = 1 << (i - 1)
		if ((x & mask) != 0):
			digit=digit+1
		if ((y & mask) != 0):
			digit=digit+2
		quadKey.append(str(digit))
	return "".join(quadKey)

uri="https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503"
log = open("./patch.log",'a+')
db = MBtiles(dbFile, mode='r+')

def download(arr):    
    tiles=[]
    for a in arr:
        res= requests.get(uri.format(random.choice([0,1,2,3]), generateQuadKey(a[1], a[2], a[0]) ))
        if res.status_code == 200 and len(res.content)>0:
            tiles.append(Tile(z=a[0], x=a[1], y=a[2], data=res.content))
        else:
            log.writelines(str(a)+"\n")
        if len(tiles) > 300:
            print(a)
            db.write_tiles(tuple(tiles))
            tiles=[] 

    if len(tiles) > 0:
        db.write_tiles(tuple(tiles))
    con.commit()
    # exit()
    
for z in range(1,14):
    data = [r for r in cur.execute('SELECT zoom_level,tile_column,tile_row FROM map where zoom_level=?  ORDER BY tile_column, tile_row',(z,))]
    arr=[]
    if len(data) < pow(2,2*z):
        for x in range(0,pow(2,z)):
            for y in range(0,pow(2,z)):
                if (z,x,y) not in data:
                    # print((z,x,y))
                    arr.append((z,x,y))
    download(arr)
    # log.writelines(str(arr)+"\n")

log.close()
con.close()
