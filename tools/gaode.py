#  高德矢量地图下载
import threading
import requests
import os
import random

uri="https://webrd0{}.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=7&x={}&y={}&z={}"
tp=threading.BoundedSemaphore(32)


def dl(z,x):
    tp.acquire()
    
    my=pow(2,z)
    cy=0
    fn='./gaode/{}/{}/'.format(z,x)
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
                r = requests.get( uri.format(random.choice([1,2,3,4]),x,y,z) )
                if r.status_code == 200:
                    print('.', end='',flush=True)
                    #print(fn+'b_{}_{}_{}.png'.format(z,x,y))                    
                    fp = open(fn+'g_{}_{}_{}.png'.format(z, x, y), 'wb')
                    fp.write(r.content)
                    fp.close()
                else:
                    print(z,x, y, r.status_code)
                    pass
                
            except Exception as e:
                    print(z,x,y,e)
                    continue
    print(z,x, end='',flush=True)
    tp.release()

tl=[]
for z in range(1,14):
    mx=pow(2,z)
    for x in range(mx):
        t=threading.Thread(target=dl, args=(z,x,))
        tl.append(t)
        
for t in tl:
    t.start()
    
for t in tl:
    t.join()
