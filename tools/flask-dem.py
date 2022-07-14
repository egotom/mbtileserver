from flask import Flask,jsonify,make_response
from markupsafe import escape
import sys,logging
from rio_tiler.io import COGReader
from rio_tiler.errors import TileOutsideBounds
from rio_tiler.profiles import img_profiles
import morecantile

app = Flask(__name__)

@app.route('/tile/<int:z>/<int:x>/<int:y>')
def tiles(z,x,y):
    #return jsonify(z=z,x=x,y=y)
    cog = COGReader("an3857_rgb.tif", tms= morecantile.tms.get("WebMercatorQuad") )
    tls = cog.tile(tile_x=x, tile_y=y, tile_z=z, tilesize=256)
    prof = img_profiles.get("PNG", {})
    resp = make_response(tls.render(img_format="PNG", **prof))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Content-Type'] = 'image/png'
    return resp
    
if __name__ == '__main__':
    app.run(host='0.0.0.0',port='800')