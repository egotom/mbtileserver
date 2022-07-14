import requests
import sqlite3,random,threading,multiprocessing,os

np = multiprocessing.cpu_count()
tp=threading.BoundedSemaphore(np)
tname='bing'
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

# uri="https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503"
uri="http://dynamic.t{}.tiles.ditu.live.com/comp/ch/{}?it=G,VE,BX,L,LA&mkt=zh-cn,syr&n=z&og=111&ur=CN"
log = open("./patch.log",'a+')

def download(arr):   
    tp.acquire()
    for a in arr:
        res= requests.get(uri.format(random.choice([0,1,2,3]), generateQuadKey(a[1], a[2], a[0]) ))
        if res.status_code == 200 and len(res.content)>0:
            print('.', end='',flush=True)
            fn='./{}/{}/{}/'.format(tname,a[0],a[1])
            os.makedirs(fn, exist_ok=True)
            fp = open(fn+'b_{}_{}_{}.png'.format(a[0],a[1],a[2]), 'wb')
            fp.write(res.content)
            fp.close()            
        else:
            print('!', end='',flush=True)
            log.writelines(str(a)+"\n")
    tp.release()

thd=[]
for z in range(1,14):
    arrs=[]
    data = [r for r in cur.execute('SELECT tile_column,tile_row FROM map where zoom_level=?  ORDER BY tile_column, tile_row',(z,))]
    wh = pow(2,z)
    if len(data) <= (wh+1)*(wh+1):
        for x in range(0,wh):
            for y in range(0, wh):
                if (x,y) not in data:
                    # print((z,x,y))
                    arrs.append((z, x, y))
                    if len(arrs) > 2000:
                        th=threading.Thread(target=download, args=(arrs, ))
                        arrs=[]
                        th.start()
                        thd.append(th)
    if len(arrs) > 0:
        th=threading.Thread(target=download, args=(arrs, ))
        arrs=[]
        th.start()
        thd.append(th)

for t in thd:
    t.join()
    # log.writelines(str(arr)+"\n")

log.close()
con.close()
