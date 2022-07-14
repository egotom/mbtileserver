from osgeo import gdal
from osgeo import osr
import math
MAXZOOMLEVEL = 32


DEFAULT_GDAL2TILES_OPTIONS = {
    'verbose': False,
    'title': '',
    'profile': 'mercator',
    'url': '',
    'resampling': 'average',
    's_srs': None,
    'zoom': None,
    'tile_size': 256,
    'resume': False,
    'srcnodata': None,
    'tmscompatible': False,
    'quiet': False,
    'kml': False,
    'webviewer': 'all',
    'copyright': '',
    'googlekey': 'INSERT_YOUR_KEY_HERE',
    'bingkey': 'INSERT_YOUR_KEY_HERE',
    'nb_processes': 1
}


gdal.UseExceptions()


class GlobalMercator(object):
    r"""
    TMS Global Mercator Profile
    ---------------------------

    Functions necessary for generation of tiles in Spherical Mercator projection,
    EPSG:3857.

    Such tiles are compatible with Google Maps, Bing Maps, Yahoo Maps,
    UK Ordnance Survey OpenSpace API, ...
    and you can overlay them on top of base maps of those web mapping applications.

    Pixel and tile coordinates are in TMS notation (origin [0,0] in bottom-left).

    What coordinate conversions do we need for TMS Global Mercator tiles::

         LatLon      <->       Meters      <->     Pixels    <->       Tile

     WGS84 coordinates   Spherical Mercator  Pixels in pyramid  Tiles in pyramid
         lat/lon            XY in meters     XY pixels Z zoom      XYZ from TMS
        EPSG:4326           EPSG:3857
         .----.              ---------               --                TMS
        /      \     <->     |       |     <->     /----/    <->      Google
        \      /             |       |           /--------/          QuadTree
         -----               ---------         /------------/
       KML, public         WebMapService         Web Clients      TileMapService

    What is the coordinate extent of Earth in EPSG:3857?

      [-20037508.342789244, -20037508.342789244, 20037508.342789244, 20037508.342789244]
      Constant 20037508.342789244 comes from the circumference of the Earth in meters,
      which is 40 thousand kilometers, the coordinate origin is in the middle of extent.
      In fact you can calculate the constant as: 2 * math.pi * 6378137 / 2.0
      $ echo 180 85 | gdaltransform -s_srs EPSG:4326 -t_srs EPSG:3857
      Polar areas with abs(latitude) bigger then 85.05112878 are clipped off.

    What are zoom level constants (pixels/meter) for pyramid with EPSG:3857?

      whole region is on top of pyramid (zoom=0) covered by 256x256 pixels tile,
      every lower zoom level resolution is always divided by two
      initialResolution = 20037508.342789244 * 2 / 256 = 156543.03392804062

    What is the difference between TMS and Google Maps/QuadTree tile name convention?

      The tile raster itself is the same (equal extent, projection, pixel size),
      there is just different identification of the same raster tile.
      Tiles in TMS are counted from [0,0] in the bottom-left corner, id is XYZ.
      Google placed the origin [0,0] to the top-left corner, reference is XYZ.
      Microsoft is referencing tiles by a QuadTree name, defined on the website:
      http://msdn2.microsoft.com/en-us/library/bb259689.aspx

    The lat/lon coordinates are using WGS84 datum, yes?

      Yes, all lat/lon we are mentioning should use WGS84 Geodetic Datum.
      Well, the web clients like Google Maps are projecting those coordinates by
      Spherical Mercator, so in fact lat/lon coordinates on sphere are treated as if
      the were on the WGS84 ellipsoid.

      From MSDN documentation:
      To simplify the calculations, we use the spherical form of projection, not
      the ellipsoidal form. Since the projection is used only for map display,
      and not for displaying numeric coordinates, we don't need the extra precision
      of an ellipsoidal projection. The spherical projection causes approximately
      0.33 percent scale distortion in the Y direction, which is not visually
      noticeable.

    How do I create a raster in EPSG:3857 and convert coordinates with PROJ.4?

      You can use standard GIS tools like gdalwarp, cs2cs or gdaltransform.
      All of the tools supports -t_srs 'epsg:3857'.

      For other GIS programs check the exact definition of the projection:
      More info at http://spatialreference.org/ref/user/google-projection/
      The same projection is designated as EPSG:3857. WKT definition is in the
      official EPSG database.

      Proj4 Text:
        +proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0
        +k=1.0 +units=m +nadgrids=@null +no_defs

      Human readable WKT format of EPSG:3857:
         PROJCS["Google Maps Global Mercator",
             GEOGCS["WGS 84",
                 DATUM["WGS_1984",
                     SPHEROID["WGS 84",6378137,298.257223563,
                         AUTHORITY["EPSG","7030"]],
                     AUTHORITY["EPSG","6326"]],
                 PRIMEM["Greenwich",0],
                 UNIT["degree",0.0174532925199433],
                 AUTHORITY["EPSG","4326"]],
             PROJECTION["Mercator_1SP"],
             PARAMETER["central_meridian",0],
             PARAMETER["scale_factor",1],
             PARAMETER["false_easting",0],
             PARAMETER["false_northing",0],
             UNIT["metre",1,
                 AUTHORITY["EPSG","9001"]]]
    """

    def __init__(self, tileSize=256):
        "Initialize the TMS Global Mercator pyramid"
        self.tileSize = tileSize
        self.initialResolution = 2 * math.pi * 6378137 / self.tileSize
        # 156543.03392804062 for tileSize 256 pixels
        self.originShift = 2 * math.pi * 6378137 / 2.0
        # 20037508.342789244

    def LatLonToMeters(self, lat, lon):
        "Converts given lat/lon in WGS84 Datum to XY in Spherical Mercator EPSG:3857"
        mx = lon * self.originShift / 180.0
        my = math.log(math.tan((90 + lat) * math.pi / 360.0)) / (math.pi / 180.0)
        my = my * self.originShift / 180.0
        return mx, my

    def MetersToLatLon(self, mx, my):
        "Converts XY point from Spherical Mercator EPSG:3857 to lat/lon in WGS84 Datum"

        lon = (mx / self.originShift) * 180.0
        lat = (my / self.originShift) * 180.0

        lat = 180 / math.pi * (2 * math.atan(math.exp(lat * math.pi / 180.0)) - math.pi / 2.0)
        return lat, lon

    def PixelsToMeters(self, px, py, zoom):
        "Converts pixel coordinates in given zoom level of pyramid to EPSG:3857"

        res = self.Resolution(zoom)
        mx = px * res - self.originShift
        my = py * res - self.originShift
        return mx, my

    def MetersToPixels(self, mx, my, zoom):
        "Converts EPSG:3857 to pyramid pixel coordinates in given zoom level"

        res = self.Resolution(zoom)
        px = (mx + self.originShift) / res
        py = (my + self.originShift) / res
        return px, py

    def PixelsToTile(self, px, py):
        "Returns a tile covering region in given pixel coordinates"

        tx = int(math.ceil(px / float(self.tileSize)) - 1)
        ty = int(math.ceil(py / float(self.tileSize)) - 1)
        return tx, ty

    def PixelsToRaster(self, px, py, zoom):
        "Move the origin of pixel coordinates to top-left corner"

        mapSize = self.tileSize << zoom
        return px, mapSize - py

    def MetersToTile(self, mx, my, zoom):
        "Returns tile for given mercator coordinates"
        px, py = self.MetersToPixels(mx, my, zoom)
        return self.PixelsToTile(px, py)

    def TileBounds(self, tx, ty, zoom):
        "Returns bounds of the given tile in EPSG:3857 coordinates"
        minx, miny = self.PixelsToMeters(tx * self.tileSize, ty * self.tileSize, zoom)
        maxx, maxy = self.PixelsToMeters((tx + 1) * self.tileSize, (ty + 1) * self.tileSize, zoom)
        return (minx, miny, maxx, maxy)

    def TileLatLonBounds(self, tx, ty, zoom):
        "Returns bounds of the given tile in latitude/longitude using WGS84 datum"
        bounds = self.TileBounds(tx, ty, zoom)
        minLat, minLon = self.MetersToLatLon(bounds[0], bounds[1])
        maxLat, maxLon = self.MetersToLatLon(bounds[2], bounds[3])

        return (minLat, minLon, maxLat, maxLon)

    def Resolution(self, zoom):
        "Resolution (meters/pixel) for given zoom level (measured at Equator)"
        # return (2 * math.pi * 6378137) / (self.tileSize * 2**zoom)
        return self.initialResolution / (2**zoom)

    def ZoomForPixelSize(self, pixelSize):
        "Maximal scaledown zoom of the pyramid closest to the pixelSize."
        for i in range(MAXZOOMLEVEL):
            if pixelSize > self.Resolution(i):
                if i != -1:
                    return i - 1
                else:
                    return 0    # We don't want to scale up

    def GoogleTile(self, tx, ty, zoom):
        "Converts TMS tile coordinates to Google Tile coordinates"
        # coordinate origin is moved from bottom-left to top-left corner of the extent
        return tx, (2**zoom - 1) - ty

    def QuadTree(self, tx, ty, zoom):
        "Converts TMS tile coordinates to Microsoft QuadTree"
        quadKey = ""
        ty = (2**zoom - 1) - ty
        for i in range(zoom, 0, -1):
            digit = 0
            mask = 1 << (i - 1)
            if (tx & mask) != 0:
                digit += 1
            if (ty & mask) != 0:
                digit += 2
            quadKey += str(digit)

        return quadKey

def geo_query(ds, ulx, uly, lrx, lry, querysize=0):
    """
    For given dataset and query in cartographic coordinates returns parameters for ReadRaster()
    in raster coordinates and x/y shifts (for border tiles). If the querysize is not given, the
    extent is returned in the native resolution of dataset ds.

    raises Gdal2TilesError if the dataset does not contain anything inside this geo_query
    """
    geotran = ds.GetGeoTransform()
    rx = int((ulx - geotran[0]) / geotran[1] + 0.001)
    ry = int((uly - geotran[3]) / geotran[5] + 0.001)
    rxsize = int((lrx - ulx) / geotran[1] + 0.5)
    rysize = int((lry - uly) / geotran[5] + 0.5)

    if not querysize:
        wxsize, wysize = rxsize, rysize
    else:
        wxsize, wysize = querysize, querysize

    # Coordinates should not go out of the bounds of the raster
    wx = 0
    if rx < 0:
        rxshift = abs(rx)
        wx = int(wxsize * (float(rxshift) / rxsize))
        wxsize = wxsize - wx
        rxsize = rxsize - int(rxsize * (float(rxshift) / rxsize))
        rx = 0
    if rx + rxsize > ds.RasterXSize:
        wxsize = int(wxsize * (float(ds.RasterXSize - rx) / rxsize))
        rxsize = ds.RasterXSize - rx

    wy = 0
    if ry < 0:
        ryshift = abs(ry)
        wy = int(wysize * (float(ryshift) / rysize))
        wysize = wysize - wy
        rysize = rysize - int(rysize * (float(ryshift) / rysize))
        ry = 0
    if ry + rysize > ds.RasterYSize:
        wysize = int(wysize * (float(ds.RasterYSize - ry) / rysize))
        rysize = ds.RasterYSize - ry

    return (rx, ry, rxsize, rysize), (wx, wy, wxsize, wysize)
        
        
gm = GlobalMercator()
b = gm.TileBounds(tx=408, ty=307, zoom=9)
print(b)
ds = gdal.Open('/mnt/d/work/gis/gdal/o3.tif', gdal.GA_ReadOnly)
rb, wb = geo_query(ds, b[0], b[3], b[2], b[1])
mem_drv = gdal.GetDriverByName('MEM')
dstile = mem_drv.Create('', tilesize, tilesize, tilebands)

print(rb, wb)