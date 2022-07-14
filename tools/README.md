# mapdl

下载地图

## 目录和文件说明

    mp.py Mapbox瓦片地图下载脚本，内含分布式任务调度功能。<python 虚拟运行环境目录>

    bing.py Bing Map 瓦片地图下载脚本.
	
	bing2.py BingMap 卫星瓦片地图分布式下载脚本.

    task.py CSV 坐标生成bing2任务数据库表。
     
    osm.py OpenStreetMap 瓦片地图下载脚本.

    poi.py 高德POI 下载脚本。

    mbtiles.py 从文件系统导入mbtiles数据库脚本。

    mapbox.sql Mapbox瓦片地图下载任务调度数据库。

    td.py 地铁线路，行政区划下载。
	
	gaode.py 高德矢量地图下载。
	
	dem.py 地理空间数据云 高程数据下载。
	
	flask-dem.py 动态高程切片服务器。
	
    
## 依赖的软件

+ python3

+ Mariadb 

+ SQLite3