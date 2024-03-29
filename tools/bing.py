import threading
import requests
import os
import random

tname = 'vt'
# 矢量地图样式1 1-9级
url="http://r{}.tiles.ditu.live.com/tiles/r{}.png?g=41"
# 矢量地图样式2 1-18级
url2="http://dynamic.t{}.tiles.ditu.live.com/comp/ch/{}?it=G,VE,BX,L,LA&mkt=zh-cn,syr&n=z&og=111&ur=CN"
# 卫星图像1-18级
url3="https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503"
# 卫星图像1-18级
url4="https://ecn.t{}.tiles.virtualearth.net/tiles/a{}.jpeg?n=z&g=12327"
# 地形矢量图
url5="https://t.ssl.ak.dynamic.tiles.virtualearth.net/comp/ch/{}?mkt=zh-CN&it=G,VE,BX,L,LA&shading=t&n=z&og=1885&cstl=vbp2&o=webp"
tp=threading.BoundedSemaphore(16)

lf=open("./{}/log.log".format(tname),"a+")
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

def dl(z,x):
    tp.acquire()
    my=pow(2,z)
    cy=0
    fn='./{}/{}/{}/'.format(tname,z,x)
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
                subd=random.choice([0,1,2,3,4,5,6,7])
                QuadKey = generateQuadKey(x, y, z)
                r = requests.get( url4.format(subd, QuadKey) )
                if r.status_code == 200 and len(r.content) > 0:
                    print('.', end='',flush=True)
                    #print(fn+'b_{}_{}_{}.png'.format(z,x,y))                    
                    fp = open(fn+'b_{}_{}_{}.jpg'.format(z, x, y), 'wb')
                    fp.write(r.content)
                    fp.close()
                else:
                    # print(subd,"==", QuadKey,"==",z, x, y," : ",r.status_code, end='!',flush=True)
                    print((z, x, y),r.status_code, end='',flush=True)
                    lf.write(str((z, x, y))+"  : "+str(r.status_code)+"\n")
            except Exception as e:
                    #print(z,x,y,e)
                    print('!', end='',flush=True)
                    lf.write(str((z, x, y))+"\n")
                    
    print(z,x, end='\t',flush=True)
    tp.release()

tl=[]
for z in range(10,14):
    mx=pow(2,z)
    for x in range(mx):
        t=threading.Thread(target=dl, args=(z,x,))
        tl.append(t)
        
for t in tl:
    t.start()
    
for t in tl:
    t.join()

lf.close()
