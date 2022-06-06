import threading
import requests
import os
import random

# 矢量地图样式1 1-9级
url="http://r{}.tiles.ditu.live.com/tiles/r{}.png?g=41"
# 矢量地图样式2 1-18级
url2="http://dynamic.t{}.tiles.ditu.live.com/comp/ch/{}?it=G,VE,BX,L,LA&mkt=zh-cn,syr&n=z&og=111&ur=CN"
# 卫星图像1-18级
url3="https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503"
tp=threading.BoundedSemaphore(16)

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

def dl(z,x,v=1):
    tp.acquire()
    my=pow(2,z)
    cy=0
    fn='./bing/{}/{}/'.format(z,x)
    os.makedirs(fn, exist_ok=True)
    dirs = os.listdir(fn)
    for d in dirs:
        dl=d.split('_')
        if len(dl) == 4:
            py = int(dl[3].split(".")[0])
            if py>cy:
                cy = py
    if cy < (my-1):
        for y in range(cy,my):
            try:
                quad = generateQuadKey(x, y, z)
                r = requests.get( url3.format(random.choice([0,1,2,3]), quad) )
                if r.status_code == 200:
                    print('.', end='',flush=True)
                    #print(fn+'b_{}_{}_{}.png'.format(z,x,y))                    
                    fp = open(fn+'b_{}_{}_{}.png'.format(z, x, y), 'wb')
                    fp.write(r.content)
                    fp.close()
                else:
                    print(z,x, y, r.status_code, end='!')
                    pass
                
            except Exception as e:
                    print(z,x,y,e)
                    continue
    print(z,x, end='',flush=True)
    tp.release()

tl=[]
for z in range(1,19):
    mx=pow(2,z)
    for x in range(mx):
        t=threading.Thread(target=dl, args=(z,x,1,))
        tl.append(t)
        
for t in tl:
    t.start()
    
for t in tl:
    t.join()
