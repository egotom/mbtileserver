package main

import (
	"fmt"
	"math"
	"reflect"
	gdal "github.com/lukeroth/gdal"
)

type tileCoord struct {
	z, x, y int64
}
const(
	ts = 256
	circumference float64 = 2.0 * math.Pi * 6378137.0 
	shift float64 =  math.Pi * 6378137.0
	ks float64 =34.64599404531959
)

func Tile(tc tileCoord,  src, dist string ) error{
	iDataset,_ := gdal.Open(src, gdal.ReadOnly)
	defer iDataset.Close()
	
	rdt := iDataset.RasterBand(1).RasterDataType()
	rbc := iDataset.RasterCount()
	adfGeoTransform :=iDataset.GeoTransform()
	// fmt.Println(adfGeoTransform)

	mz := math.Pow(2, float64(tc.z))

	ux := float64(tc.x)*circumference/mz-shift
	uy := float64(tc.y+1)*circumference/mz-shift 
	lx := float64(tc.x+1)*circumference/mz-shift
	ly := float64(tc.y)*circumference/mz-shift

	fmt.Println(ux,uy,lx,ly)

	rx := int((ux-adfGeoTransform[0])/adfGeoTransform[1]+0.001)
	ry := int((uy-adfGeoTransform[3])/adfGeoTransform[5]+0.001)
	rxSize := int((lx-ux)/adfGeoTransform[1] + 0.5)
	rySize := int((ly-uy)/adfGeoTransform[5] + 0.5)

	wxSize, wySize := rxSize, rySize
	wx, wy := 0, 0
	if rx < 0 {
		rxshift := math.Abs(float64(rx))
		wx = int(float64(wxSize)*(rxshift/float64(rxSize)))
		wxSize = wxSize - wx
		rxSize = int(float64(rxSize) - float64(rxSize)*(rxshift/float64(rxSize)))
		rx = 0
	}

	if ry < 0 {
		ryshift := math.Abs(float64(ry))
		wy = int(float64(wySize)*(ryshift/float64(rySize)))
		wySize = int(float64(wySize) - float64(wy))
		rySize = int(float64(rySize) - float64(rySize)*(ryshift/float64(rySize)))
		ry = 0
	}

	adfGeoTransform[0] = adfGeoTransform[0] + float64(rx)*adfGeoTransform[1] + float64(ry)*adfGeoTransform[2]
	adfGeoTransform[3] = adfGeoTransform[3] + float64(rx)*adfGeoTransform[4] + float64(ry)*adfGeoTransform[5]
	
    adfGeoTransform[1] = (lx-ux)/ts
    adfGeoTransform[5] = -1*(ly-uy)/ts

	fmt.Println(rx, ry, rxSize, rySize, "  ---   ", wx, wy, wxSize, wySize)

	bfs := ts*ts*rbc
	var buffer interface{}
	// var nPixelSpace, nLineSpace int = 0,0
	switch rdt{
		case gdal.Byte:
			// t := reflect.TypeOf((*byte)(nil)).Elem()
			// nPixelSpace=int(t.Size())*rbc
			buffer = make([]byte, bfs)
			
		case gdal.UInt16, gdal.Int16:
			// t := reflect.TypeOf((*int16)(nil)).Elem()
			// nPixelSpace=int(t.Size())*rbc
			buffer = make([]int16, bfs)
			
		case gdal.UInt32, gdal.Int32:
			// t := reflect.TypeOf((*int32)(nil)).Elem()
			// nPixelSpace=int(t.Size())*rbc
			buffer = make([]int32, bfs)
			
		case gdal.Float32:
			// t := reflect.TypeOf((*float32)(nil)).Elem()
			// nPixelSpace=int(t.Size())*rbc
			buffer = make([]float32, bfs)
			
		case gdal.Float64:
			// t := reflect.TypeOf((*float64)(nil)).Elem()
			// nPixelSpace=int(t.Size())*rbc
			buffer = make([]float64, bfs)
			
		default:
			// t := reflect.TypeOf((*int8)(nil)).Elem()
			// nPixelSpace=int(t.Size())*rbc
			buffer = make([]int8, bfs)
	}
	
	aBand := make([]int, rbc)
	for i := 0; i < rbc; i++{
		aBand[i]=i+1
	}
	driver := iDataset.Driver()
	oDataset := driver.Create(dist, ts, ts, rbc, rdt, nil)
	defer oDataset.Close()
	oDataset.SetGeoTransform(adfGeoTransform);
	oDataset.SetProjection(iDataset.Projection());
	fmt.Println(iDataset.Projection())
	// iDataset.IO(gdal.Read, rx, ry, rxSize, rySize, buffer, rxSize, rySize, rbc, aBand, nPixelSpace, nLineSpace, 0)
	iDataset.IO(gdal.Read, rx, ry, ts, ts, buffer, ts, ts, rbc, aBand, 0, 0, 0)
	oDataset.IO(gdal.Write, wx, wy, ts, ts, buffer, ts, ts, rbc, aBand, 0, 0, 0)
	return nil
}

// func Resolution(zoom int64) float64{
// 	//"Resolution (meters/pixel) for given zoom level (measured at Equator)"
// 	return (2 * math.Pi * 6378137) / (ts * math.Pow(2, float64(zoom)))
// 	// return self.initialResolution / (2**zoom)
// }

// func PixelsToMeters(px, py, zoom int64) (float64,float64){
// 	//"Converts pixel coordinates in given zoom level of pyramid to EPSG:3857"
// 	res := Resolution(zoom)
// 	mx := float64(px) * res - shift
// 	my := float64(py) * res - shift
// 	return mx, my
// }


// func TileBounds(tx, ty, zoom int64)(float64,float64,float64,float64){
// 	//"Returns bounds of the given tile in EPSG:3857 coordinates"
// 	minx, miny := PixelsToMeters(tx * ts, ty * ts, zoom)
// 	maxx, maxy := PixelsToMeters((tx + 1) * ts, (ty + 1) * ts, zoom)
// 	return minx, miny, maxx, maxy
// }

func Tl(tc tileCoord, src, dist string) error{
	iDataset,_ := gdal.Open(src, gdal.ReadOnly)
	defer iDataset.Close()
	
	rdt := iDataset.RasterBand(1).RasterDataType()
	rbc := iDataset.RasterCount()
	adfGeoTransform :=iDataset.GeoTransform()
	// fmt.Println(adfGeoTransform)

	rx := 0
	ry := 3000
	rxSize, rySize := 512, 512

	adfGeoTransform[0] = adfGeoTransform[0] + float64(rx)*adfGeoTransform[1] + float64(ry)*adfGeoTransform[2]
	adfGeoTransform[3] = adfGeoTransform[3] + float64(rx)*adfGeoTransform[4] + float64(ry)*adfGeoTransform[5]
	
    adfGeoTransform[1] = adfGeoTransform[1]/2
    adfGeoTransform[5] = adfGeoTransform[5]/2

	bfs := ts*ts*rbc
	var buffer interface{}
	var nPixelSpace, nLineSpace int = 0, 0
	switch rdt{
		case gdal.Byte:
			t := reflect.TypeOf((*byte)(nil)).Elem()
			nPixelSpace=int(t.Size())*rbc
			buffer = make([]byte, bfs)
			
		case gdal.UInt16, gdal.Int16:
			t := reflect.TypeOf((*int16)(nil)).Elem()
			nPixelSpace=int(t.Size())*rbc
			buffer = make([]int16, bfs)
			
		case gdal.UInt32, gdal.Int32:
			t := reflect.TypeOf((*int32)(nil)).Elem()
			nPixelSpace=int(t.Size())*rbc
			buffer = make([]int32, bfs)
			
		case gdal.Float32:
			t := reflect.TypeOf((*float32)(nil)).Elem()
			nPixelSpace=int(t.Size())*rbc
			buffer = make([]float32, bfs)
			
		case gdal.Float64:
			t := reflect.TypeOf((*float64)(nil)).Elem()
			nPixelSpace=int(t.Size())*rbc
			buffer = make([]float64, bfs)
			
		default:
			t := reflect.TypeOf((*int8)(nil)).Elem()
			nPixelSpace=int(t.Size())*rbc
			buffer = make([]int8, bfs)
	}
	
	aBand := make([]int, rbc)
	for i := 0; i < rbc; i++{
		aBand[i]=i+1
	}

	oDataset := iDataset.Driver().Create(dist, ts, ts, rbc, rdt, nil)
	defer oDataset.Close()
	oDataset.SetGeoTransform(adfGeoTransform);
	oDataset.SetProjection(iDataset.Projection());
	fmt.Println(iDataset.Projection())
	// iDataset.IO(gdal.Read, rx, ry, rxSize, rySize, buffer, rxSize, rySize, rbc, aBand, nPixelSpace, nLineSpace, 0)
	iDataset.IO(gdal.Read, rx, ry, rxSize, rySize, buffer, rxSize, rySize, rbc, aBand, nPixelSpace, nLineSpace, 0)
	oDataset.IO(gdal.Write, rx, ry, ts, ts, buffer, rxSize, rySize, rbc, aBand, 0, 0, 0)
	return nil
}

func main() {
	tile := tileCoord{9,408,307}
	// fullMap := "/mnt/e/dem/a_3857_n_rgb.tif"
	fullMap := "/mnt/d/work/gis/gdal/o3.tif"
	tileMap := "o.tif"
	// Tile(tile, fullMap, tileMap)
	Tl(tile, fullMap, tileMap)
}
