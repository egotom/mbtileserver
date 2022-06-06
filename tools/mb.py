#   mapbox卫星地图下载
import mariadb 
import requests
from uuid import getnode
import multiprocessing, threading, os, random, math
from datetime import datetime 

def deg2num(lat_deg, lon_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
    return (xtile, ytile)

def num2deg(xtile, ytile, zoom):
    n = 2.0 ** zoom
    lon_deg = xtile / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
    lat_deg = math.degrees(lat_rad)
    return (lat_deg, lon_deg)
    
conn = mariadb.connect(host="localhost", database="mapbox", user="root", password="root")
cur = conn.cursor() 
cur.execute("SELECT z, x, y FROM info WHERE name=?", ("mapbox",)) 
rcd=cur.fetchone()
# print(rcd[0], rcd[1])
mz= rcd[0]
mx= rcd[1]
my= rcd[2]
if not mz or not mx or not my:
    print("未定义下载任务！")

uri=None
mac_addr = getnode()
cur.execute("SELECT mac, mapbox_token, url FROM worker") 
for mac, mapbox_token, url in cur:
    if mac_addr == mac and mapbox_token in url:
        uri = url

#  pk.eyJ1Ijoia2Vpd2VuZyIsImEiOiJjbDBxMjByYW8wOGU3M2NxbmJ2Zno2Nm1zIn0.txEgI66SG9Xwd1kHSc1bqg

while not uri:
    at = input("请输入 mapbox access_token > ")
    sd = random.choice("abcd")
    uri = "https://"+sd+".tiles.mapbox.com/v4/mapbox.satellite/{}/{}/{}.jpg90?access_token="+at
    print("正在测试网络链接 ...")
    r = requests.get( uri.format(mz,0,0) )
    if r.status_code == 401:
        at = input("mapbox access_token 不正确，请重新输入 > ")
        uri = None
    if r.status_code == 200:
        cur.execute("INSERT INTO worker (mac, mapbox_token, url, create_at) VALUES (?, ?, ?, ?)", (mac_addr, at, uri, datetime.now())) 
        conn.commit()
        print("成功！")
    else:
        uri = None
 
np = multiprocessing.cpu_count()
lock = threading.Lock()
def getTask():
    xs=[]
    xd=[]
    cur.execute("SELECT done, x, worker_mac FROM progress") 
    for done, x, worker_mac in cur:
        xd.append(x)
        if mac_addr == worker_mac and done == "N":
            xs.append(x)
    
    if len(xs) == 0:
        lock.acquire()
        for x in range(mx):
            if x in xd:
                continue
            try: 
                cur.execute("INSERT INTO progress (done,z,x,worker_mac,create_at,update_at) VALUES (?, ?, ?, ?, ?,?)", ("N",mz,x,mac_addr,datetime.now(),datetime.now())) 
            except mariadb.Error as e: 
                print(f"Error: {e}")

            xs.append(x)
            if len(xs) == np:
                break
        conn.commit() 
        lock.release()
    # print(xs)
    return xs
    
def dl(ax):
    for x in ax:
        status = 0
        fn='./mapbox/'+str(x)
        os.makedirs(fn, exist_ok=True)
        
        cy=0
        for d in os.listdir(fn):
            j = d.split('_')
            if len(j) == 4:
                dy = j[3].split(".")[0]
                if int(dy) > cy:
                    cy = int(dy)
            
        for y in range(cy, my): 
            try:
                r = requests.get( uri.format(mz,x,y) )
                print(mz, x, y, r.status_code)
                if r.status_code == 200:
                    status = 0
                    # fp = open(fn+'/m_{}_{}_{}.png'.format(mz,x,y), 'wb')
                    fp = open(fn+'/{}.jpg'.format(y), 'wb')
                    fp.write(r.content)
                    fp.close()
                if r.status_code == 404:
                    print(uri.format(mz,x,y), r.status_code)
                    status += 1
                    if status > 10:
                        break

            except Exception as e:
                print(e)
            
        lock.acquire()
        try: 
            cur.execute("update progress set done=?, update_at=? where x=? and z=?", ("Y",datetime.now(), x, mz)) 
        except mariadb.Error as e: 
            print(f"Error: {e}")
        lock.release()

while True:
    thd=[]
    xs = getTask()
    if len(xs) == 0:
        break
    
    step = int(len(xs)/np)  if len(xs)>np else 1
    for i in range(np):
        s=i*step
        e=s+step
        if len(xs[s:e])==0:
            break
        th=threading.Thread(target=dl, args=(xs[s:e],))
        th.start()
        thd.append(th)
    for th in thd:
        th.join()
conn.close()