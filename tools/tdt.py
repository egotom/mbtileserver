#天地图遥感图：
#https://t3.tianditu.gov.cn/img_w/wmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=img&STYLE=default&TILEMATRIXSET=w&FORMAT=tiles&TILECOL={x}&TILEROW={y}&TILEMATRIX={z}&tk=a4ee5c551598a1889adfabff55a5fc27

import threading
import requests
import os
import random

token='a4ee5c551598a1889adfabff55a5fc27'
uri="https://t{}.tianditu.gov.cn/img_w/wmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=img&STYLE=default&TILEMATRIXSET=w&FORMAT=tiles&TILECOL={}&TILEROW={}&TILEMATRIX={}&tk="+token
tp=threading.BoundedSemaphore(32)
uas = [
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 Edg/100.0.1185.50"
]
header={
    'User-Agent':random.choice(uas),
    'Cookie':"HWWAFSESTIME=1650991039236; HWWAFSESID=79760943cdbba148a4; TDTSESID=rBACA2JoH7+6kxZy/28rAg=="
} 

def dl(z,x):
    tp.acquire()
    
    my=pow(2,z)
    cy=0
    fn='./tiandi/{}/{}/'.format(z,x)
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
                r = requests.get( uri.format(random.choice([0,1,2,3,4,5,6,7]),x,y,z), headers=header)
                if r.status_code == 200:
                    print('.', end='',flush=True)
                    #print(fn+'t_{}_{}_{}.jpg'.format(z,x,y))                    
                    fp = open(fn+'t_{}_{}_{}.jpg'.format(z, x, y), 'wb')
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
for z in range(0,3):
    mx=pow(2,z)
    for x in range(mx):
        t=threading.Thread(target=dl, args=(z,x,))
        tl.append(t)
        
for t in tl:
    t.start()
    
for t in tl:
    t.join()
