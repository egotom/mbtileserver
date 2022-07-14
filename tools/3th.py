import threading
import requests
import os
import random

tname = 'gac'
url="http://gac-geo.googlecnapps.cn/maps/vt?lyrs=s&x={}&y={}&z={}"

tp=threading.BoundedSemaphore(16)

os.makedirs("./{}".format(tname), exist_ok=True)
lf=open("./{}/log.log".format(tname),"a+")

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
                r = requests.get( url.format(x,y,z) )
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
for z in range(0,10):
    mx=pow(2,z)
    for x in range(mx):
        t=threading.Thread(target=dl, args=(z,x,))
        tl.append(t)
        
for t in tl:
    t.start()
    
for t in tl:
    t.join()

lf.close()
