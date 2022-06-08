package handlers

import(
	"os"
	"fmt"
	"math"
	"time"
	"strings"
	"net/http"
	"io/ioutil"
	"math/rand"
)

func (ts *Tileset) get(z int64, x int64, y int64)([]byte, error ){
	url := ""
	rand.Seed(time.Now().UnixNano()+1210)
	sd := []string{"a","b","c"}
	rand.Shuffle(len(sd), func(i, j int) { sd[i], sd[j] = sd[j], sd[i] })

	sb := []string{"0","1","2","3"}
	rand.Shuffle(len(sb), func(i, j int) { sb[i], sb[j] = sb[j], sb[i] })

	var quad string = GenerateQuadKey(x,y,z)
	
	switch ts.name {
	case "osm":
		url = fmt.Sprintf("https://%s.tile.openstreetmap.org/%d/%d/%d.png",sd[0], z, x, y)
	
	case "mapbox":
		var token string = "pk.eyJ1IjoienpmYW5nZSIsImEiOiJjbDFxNHh3ZXUxNXl3M2RwYzByYXJ3OWdnIn0.-VcnWShx3SR9InJn3kRQvQ"
		url = fmt.Sprintf("https://%s.tiles.mapbox.com/v4/mapbox.satellite/%d/%d/%d.png?access_token=%s", sd[0], z, x, y, token)
	
	case "bing":
		url = fmt.Sprintf("http://dynamic.t%s.tiles.ditu.live.com/comp/ch/%s?it=G,VE,BX,L,LA&mkt=zh-cn,syr&n=z&og=111&ur=CN" ,sb[0], quad)
	
	case "bing1":
		url = fmt.Sprintf("http://r%s.tiles.ditu.live.com/tiles/r%s.png?g=41", sb[0], quad)

	case "bing2":
		url = fmt.Sprintf("http://dynamic.t%s.tiles.ditu.live.com/comp/ch/%s?it=G,VE,BX,L,LA&mkt=zh-cn,syr&n=z&og=111&ur=CN" ,sb[0], quad)
	
	case "bing3":
		url = fmt.Sprintf("https://t%s.dynamic.tiles.ditu.live.com/comp/ch/%s?mkt=zh-cn&n=z&it=A&src=o&og=503" ,sb[0], quad)

	default:
		return nil, fmt.Errorf("Unrecognized map vandor: %s", ts.name)
	}

    resp, err := http.Get(url)
    if err != nil {
        fmt.Println(err)
        return nil, err
    }
    defer resp.Body.Close()

    body, err := ioutil.ReadAll(resp.Body)
	//fmt.Println(ts.name,"+++++++++++++++++++++++++++++++",url,body)
	//WriteImg(fmt.Sprintf("%d_%d_%d.png",z, x, y), body)
    if resp.StatusCode == 200 && err == nil{
        err = ts.db.InserTile(z, x, y, &body)
        // fmt.Println("ok",err)
        return body, nil
    }
    return nil, err
}

type Tile struct {
	Z    int64
	X    int64
	Y    int64
	Lat  float64
	Long float64
}

type Conversion interface {
	deg2num(t *Tile) (x int64, y int64)
	num2deg(t *Tile) (lat float64, long float64)
}

func (*Tile) Deg2num(t *Tile) (x int64, y int64) {
	n := math.Exp2(float64(t.Z))
	x = int64(math.Floor((t.Long + 180.0) / 360.0 * n))
	if float64(x) >= n {
		x = int64(n - 1)
	}
	y = int64(math.Floor((1.0 - math.Log(math.Tan(t.Lat*math.Pi/180.0)+1.0/math.Cos(t.Lat*math.Pi/180.0))/math.Pi) / 2.0 * n))
	return
}

func WriteImg(fn string, data []byte){
	os.WriteFile(fn, data, 0666)
}

func (*Tile) Num2deg(t *Tile) (lat float64, long float64) {
	n := math.Pi - 2.0*math.Pi*float64(t.Y)/math.Exp2(float64(t.Z))
	lat = 180.0 / math.Pi * math.Atan(0.5*(math.Exp(n)-math.Exp(-n)))
	long = float64(t.X)/math.Exp2(float64(t.Z))*360.0 - 180.0
	return lat, long
}

func GenerateQuadKey(x int64, y int64, z int64) string {
	quadKey := []string{}
	for i:=z; i>0; i--{
		digit := 0
		mask := 1 << (i - 1)
		if (x & int64(mask)) != 0{
			digit++
		}
		if (y & int64(mask)) != 0{
			digit++
			digit++
		}			
		quadKey=append(quadKey, fmt.Sprintf("%d", digit))
	}
	return strings.Join(quadKey[:], "")
}
	
