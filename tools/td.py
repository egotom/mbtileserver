
from datetime import datetime
import os,requests


# 地铁线路
#http://map.amap.com/service/subway?_1650147763410&srhdata=4403_drw_shenzhen.json
#http://map.amap.com/service/subway?_1650147763412&srhdata=4403_info_shenzhen.json

#http://map.amap.com/service/subway?_1650147798140&srhdata=3201_drw_nanjing.json
#http://map.amap.com/service/subway?_1650147798141&srhdata=3201_info_nanjing.json

#http://map.amap.com/service/subway?_1650147824334&srhdata=3301_drw_hangzhou.json
#http://map.amap.com/service/subway?_1650147824335&srhdata=3301_info_hangzhou.json

def subway():
    ct=[{"id":"1100", "cityname":"beijing", "name":"北京"},
        {"id":"3100", "cityname":"shanghai", "name":"上海"},
        {"id":"4401", "cityname":"guangzhou", "name":"广州"},
        {"id":"4403", "cityname":"shenzhen", "name":"深圳"},
        {"id":"4201", "cityname":"wuhan", "name":"武汉"},
        {"id":"1200", "cityname":"tianjin", "name":"天津"},
        {"id":"3201", "cityname":"nanjing", "name":"南京"},
        {"id":"8100", "cityname":"xianggang", "name":"香港"},
        {"id":"5000" , "cityname":"chongqing","name":"重庆"},
        {"id":"3301" , "cityname":"hangzhou","name":"杭州"},
        {"id":"2101" , "cityname":"shenyang","name":"沈阳"},
        {"id":"2102" , "cityname":"dalian","name":"大连"},
        {"id":"5101" , "cityname":"chengdu","name":"成都"},
        {"id":"2201" , "cityname":"changchun","name":"长春"},
        {"id":"3205" , "cityname":"suzhou","name":"苏州"},
        {"id":"4406" , "cityname":"foshan","name":"佛山"},
        {"id":"5301" , "cityname":"kunming","name":"昆明"},
        {"id":"6101" , "cityname":"xian","name":"西安"},
        {"id":"4101" , "cityname":"zhengzhou","name":"郑州"},
        {"id":"4301" , "cityname":"changsha","name":"长沙"},
        {"id":"3302" , "cityname":"ningbo","name":"宁波"},
        {"id":"3202" , "cityname":"wuxi","name":"无锡"},
        {"id":"3702" , "cityname":"qingdao","name":"青岛"},
        {"id":"3601" , "cityname":"nanchang","name":"南昌"},
        {"id":"3501" , "cityname":"fuzhou","name":"福州"},
        {"id":"4419" , "cityname":"dongguan","name":"东莞"},
        {"id":"4501" , "cityname":"nanning","name":"南宁"},
        {"id":"3401" , "cityname":"hefei","name":"合肥"},
        {"id":"5201" , "cityname":"guiyang","name":"贵阳"},
        {"id":"3502" , "cityname":"xiamen","name":"厦门"},
        {"id":"2301" , "cityname":"haerbin","name":"哈尔滨"},
        {"id":"1301" , "cityname":"shijiazhuang","name":"石家庄"},
        {"id":"6501" , "cityname":"wulumuqi","name":"乌鲁木齐"},
        {"id":"3303" , "cityname":"wenzhou","name":"温州"},
        {"id":"3701" , "cityname":"jinan","name":"济南"},
        {"id":"6201" , "cityname":"lanzhou","name":"兰州"},
        {"id":"3204" , "cityname":"changzhou","name":"常州"},
        {"id":"3203" , "cityname":"xuzhou","name":"徐州"},
        {"id":"1401" , "cityname":"taiyuan","name":"太原"},
        {"id":"1501" , "cityname":"huhehaote","name":"呼和浩特"}
    ]

    drw="http://map.amap.com/service/subway?_{}&srhdata={}_drw_{}.json"
    info="http://map.amap.com/service/subway?_{}&srhdata={}_info_{}.json"
    for it in ct:
        now = datetime.now()
        ts = round(datetime.timestamp(now)*100)
        print(it.get("id"),it.get("name"))
        rd = requests.get( drw.format(ts, it.get("id"), it.get("cityname")) )
        #rd.json()
        fp = open('{}_drw_{}.json'.format(it.get("id"), it.get("cityname")), 'w')
        fp.write(rd.text)
        fp.close
        
        ri = requests.get( info.format(ts, it.get("id"), it.get("cityname")) )
        fp = open('{}_info_{}.json'.format(it.get("id"), it.get("cityname")), 'w')
        fp.write(ri.text)
        fp.close
      
#subway()

#行政区域划分
#https://geo.datav.aliyun.com/areas_v3/bound/geojson?code=650500_full
#https://geo.datav.aliyun.com/areas_v3/bound/geojson?code=620000_full      
cn="https://geo.datav.aliyun.com/areas_v3/bound/geojson?code={}_full"
def boundary(ac):
    r=requests.get(cn.format(ac))
  
    fp = open('{}.json'.format(ac), 'w')
    fp.write(r.text)
    fp.close()
    
    fs = r.json().get('features') 
    for f in fs:
        n = f.get('properties').get('name')
        a = f.get('properties').get('adcode')
        print(n, "\t", a)
        
        e = f.get('properties').get('childrenNum')
        if e > 0:
            boundary(a)   

#boundary('100000')