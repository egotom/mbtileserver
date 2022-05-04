import threading
import requests
import os
requests.packages.urllib3.disable_warnings()

#下载地理空间数据云高程  http://www.gscloud.cn/ 
#http://www.gscloud.cn/wsd/gscloud_wsd/dataset/query_data?tableInfo=%7B%22offset%22%3A10%2C%22pageSize%22%3A10%2C%22totalPage%22%3A2257%2C%22totalSize%22%3A22561%2C%22sortSet%22%3A%5B%7B%22id%22%3A%22datadate%22%2C%22sort%22%3A%22desc%22%7D%5D%2C%22filterSet%22%3A%5B%5D%7D&pid=aeab8000652a45b38afbb7ff023ddabb

#http://www.gscloud.cn/wsd/gscloud_wsd/dataset/query_data?
#tableInfo={"offset":10,"pageSize":10,"totalPage":2257,"totalSize":22561,"sortSet":[{"id":"datadate","sort":"desc"}],"filterSet":[]}
#pid=aeab8000652a45b38afbb7ff023ddabb

#https://bjdl.gscloud.cn/sources/download/aeab8000652a45b38afbb7ff023ddabb/ASTGTMV003_N00E021?sid=sk10wKpg3eQJNl0sncaqOiA8mdXNixKFktvjlxen-lt7SQ&uid=638655
#https://bjdl.gscloud.cn/sources/download/aeab8000652a45b38afbb7ff023ddabb/ASTGTMV003_N02E025?sid=sk10wKpg3eQJNl0sncaqOiA8mdXNixKFktvjlxen-lt7SQ&uid=638655

uri = "https://bjdl.gscloud.cn/sources/download/aeab8000652a45b38afbb7ff023ddabb/{}?sid=sk10wKpg3eQJNl0sncaqOiA8mdXNixKFktvjlxen-lt7SQ&uid=638655"
tp=threading.BoundedSemaphore(10)

def dld(pdid):
    tp.acquire()
    with requests.get(url=uri.format(pdid), verify=False, stream=True) as rs:
        with open(dr+pdid+".zip", 'wb') as fd:
            for chunk in rs.iter_content(chunk_size=1024):
                if chunk:
                    fd.write(chunk)
    print(pdid)
    tp.release()
    
def main(fp):
    pg = 0
    for l in fp.readlines():
        x=l.split(" ")
        if len(x)==2 and x[0]=="#":
            pg = int(x[1]) 

    for i in range(pg, 22561, 10):
        fp.write("# {}\n".format(i))
        fp.flush()
        
        ar=[]
        try:
            r = requests.get(url="http://www.gscloud.cn/wsd/gscloud_wsd/dataset/query_data?tableInfo=%7B%22offset%22%3A{}%2C%22pageSize%22%3A10%2C%22totalPage%22%3A2257%2C%22totalSize%22%3A22561%2C%22sortSet%22%3A%5B%7B%22id%22%3A%22datadate%22%2C%22sort%22%3A%22desc%22%7D%5D%2C%22filterSet%22%3A%5B%5D%7D&pid=aeab8000652a45b38afbb7ff023ddabb".format(i), verify=False)
            res=r.json()
            ar = res.get("data")
        except Exception as e:
            print(repr(e))
            main(fp)
        
        tl=[]
        for p in ar:
            dataid = p.get("dataid")
            #path = p.get("path")
            #row = p.get("row")
            lon = p.get("ct_long")
            lat = p.get("ct_lat")
            fp.write("{}, {}, {}\n".format(dataid,lon,lat))
            fp.flush()
            t=threading.Thread(target=dld, args=(dataid, ))
            tl.append(t)
            
        for t in tl:
            t.start()
            
        for t in tl:
            t.join()

dr='./DEM/'
os.makedirs(dr, exist_ok=True)
fp=None
if os.path.exists(dr+'lon_lat.log'):
    fp = open(dr+'lon_lat.log', 'r+')
else:
    fp = open(dr+'lon_lat.log', 'w+')
    fp.write("dataid, ct_long, ct_lat\n")
    fp.flush()
    
main(fp)
fp.close()