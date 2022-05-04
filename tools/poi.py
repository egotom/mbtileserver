import requests
from pymongo import MongoClient
from pprint import pprint
from decimal import Decimal

client = MongoClient("mongodb://localhost:27017")
db=client.amap
#serverStatusResult=db.command("serverStatus")
#pprint(serverStatusResult)

fp = open('poi.log', 'r+')
ll=fp.readline()
pll = ll.split(",")
lon,plat = Decimal('91.247703'),0
if len(pll)==2:
    lon,plat = Decimal(pll[0]),Decimal(pll[1])

url="https://ditu.amap.com/service/regeo?longitude={}&latitude={}"

while lon < 121.977416:
    lat = Decimal('41.473895')
    if plat > 0:
        lat=plat
        plat=-1
    ctt=1
    while lat > 18.265208:
        ct=0
        try:
            print(lon,lat,"\t",end="",flush=True)
            r = requests.get( url.format(lon,lat) )
            if r.status_code == 200:
                #db.poi.insert_one(r.json())
                data=r.json().get("data")
                if data:
                    poi=data.get("poi_list")
                    if poi:
                        db.poi.insert_many(poi)
                        ct=1
                        
                    road=data.get("road_list")
                    if road:
                        db.road.insert_many(road)
                        
                    cross=data.get("cross_list")
                    if cross:
                        db.cross.insert_many(cross)
                    if data["sea_area"]["name"] !="":
                        break
                
                fp.seek(0, 0)
                fp.write(str(lon)+","+str(lat))
                fp.flush()
        except Exception as e:
            print(e)
            continue
        
        if ct==1:
            ctt=1
        else:
            ctt=ctt+1
        lat = lat - ctt*Decimal('0.002')
    lon = lon + Decimal('0.002')

fp.close()
#91.247703，41.473895 
#121.977416, 18.265208

