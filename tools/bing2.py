#  bing卫星地图分布式下载

import mariadb 
import requests
from uuid import getnode
import multiprocessing, threading, os, math, random
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

conn = mariadb.connect(host="localhost", database="bing2", user="root", password="v")
cur = conn.cursor() 
cur.execute("SELECT z, p, p2, url FROM info WHERE name=?", ("bing2",)) 
taskList = []
uri=""
for z, p, p2, url in cur:
    # print(z)
    # print(p)
    # print(p2)
    # print(url)
    
    if len(p)==0 or  len(p2)==0 or  len(z)==0 or  len(url)==0:
        print("未定义任务！")
        exit()
    uri = url

    z, z2 = z.split(',')
    z = int(z)
    z2 = int(z2)+1
    for zi in range(z,z2):
        lon = float(p.split(',')[0])
        lat = float(p.split(',')[1])
        x, y = deg2num(lat,lon,zi)

        lon = float(p2.split(',')[0])
        lat = float(p2.split(',')[1])
        x2, y2 = deg2num(lat,lon,zi)

        if x > x2:
            sw=x
            x=x2
            x2=sw+1
        xs=[]
        for i in range(x,x2):
            xs.append(i)

        if y > y2:
            sw=y
            y=y2
            y2=sw+1

        taskList.append({'z':zi, 'x':xs, 'y':(y,y2)})

mac_addr = getnode()
lock = threading.Lock()
np = multiprocessing.cpu_count()
tp=threading.BoundedSemaphore(np)

def getTask():
    print("----------------------------------------")
    cur.execute("SELECT z, x FROM progress where done = 'Y' or worker_mac != ? ", (mac_addr,)) 
    for z, x in cur:
        for tl in taskList:
            if tl['z'] == z and x in tl['x']:
                tl['x'].remove(x)
    tls=[]
    for tl in taskList:
        if len(tl['x'])>0 and tl['y'][0] != tl['y'][1]:
            for x in tl['x']:
                tls.append((tl['z'], x, tl['y']))
                if len(tls) == np:
                    break
        if len(tls) == np:
            break
    return tls
    
def dl(z, x, cy, my):
    tp.acquire()
    
    # cy = cy
    fn='./bing2/{}/{}/'.format(z,x)
    os.makedirs(fn, exist_ok=True)
    # for d in os.listdir(fn):
    #     dl=d.split('_')
    #     if len(dl) == 4:
    #         py = int(dl[3].split(".")[0])
    #         if py > cy:
    #             cy = py

    lock.acquire()
    try: 
        cur.execute('''INSERT INTO progress (done, z, x, worker_mac, create_at) select ?, ?, ?, ?, ? WHERE NOT EXISTS (
            SELECT done FROM progress WHERE z = ? and x = ?) LIMIT 1''', ("N", z, x, mac_addr, datetime.now(), z, x)) 
        conn.commit()
    except mariadb.Error as e: 
        print(f"Error: {e}")
    lock.release()

    for y in range(cy,my):
        quad = generateQuadKey(x, y, z)
        try:
            r = requests.get( uri.format(random.choice([0,1,2,3]), quad) )
            if r.status_code == 200 and len(r.content)>0:
                print('.', end='',flush=True)
                #print(fn+'b_{}_{}_{}.png'.format(z,x,y))
                fp = open(fn+'b_{}_{}_{}.png'.format(z, x, y), 'wb')
                fp.write(r.content)
                fp.close()
            else:
                print(r.status_code, end='!\t')
                lock.acquire()
                cur.execute("INSERT INTO error(z, x, y, quad, status_code) values(?,?,?,?,?) ; ", (z, x, y, quad, r.status_code)) 
                conn.commit()
                lock.release()
                
        except Exception as e:
            print("!",e)
            lock.acquire()
            cur.execute("INSERT INTO error(z,x,y,quad,status_code) values(?,?,?,?,?) ; ", (z, x, y, quad,'000')) 
            conn.commit()
            lock.release()

    print(z,x, end='\t',flush=True)
    lock.acquire()
    try: 
        cur.execute("update progress set done=?, update_at=? where x=? and z=?", ("Y",datetime.now(), x, z)) 
        conn.commit()
    except mariadb.Error as e: 
        print(f"Error: {e}")
    lock.release()
    tp.release()
    
while True:
    tls=getTask()
    if len(tls)==0:
        break

    thd = []
    for tl in tls:
        th=threading.Thread(target=dl, args=(tl[0], tl[1], tl[2][0], tl[2][1], ))
        th.start()
        thd.append(th)
    for th in thd:
        th.join()
                
cur.execute("SELECT z, x, y from error where status_code !='200';") 
for z, x, y in cur:
    quad = generateQuadKey(x, y, z)
    r = requests.get( uri.format(random.choice([0,1,2,3]), quad) )
    if r.status_code == 200:                  
        fp = open('./bing2/{}/{}/b_{}_{}_{}.png'.format(z,x, z, x, y), 'wb')
        fp.write(r.content)
        fp.close()
        cur.execute("delete from error where z =? and x=? and y=? ;", (z, x, y))   
    else:
        print(z,x, y, r.status_code, end='!')
    
conn.commit()
conn.close()

print("清理文件...")
dirs="./bing2/"
for root, dirs, files in os.walk(dirs, topdown=False):
    for d in files:
        fn=os.path.join(root, d)
        stat=os.stat(fn)
        if stat.st_size == 0 :
            print(fn)
            os.remove(fn)