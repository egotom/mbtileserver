import 'ol/ol.css';
import Map from 'ol/Map';
import TileLayer from 'ol/layer/Tile';
import View from 'ol/View';
// import {OSM, TileDebug} from 'ol/source';

const map = new Map({
    layers: [
        new TileLayer({
            source: new XYZ({
                url: "http://localhost:8000/services/bing/tiles/{z}/{x}/{y}.png"
            })
        })
    ],
    view: new View({
        center: [113.27, 23.13],
        projection: 'EPSG:4326',
        zoom: 6
    }),
    target: 'map'
});

// const map = new Map({
//   layers: [
//     new TileLayer({
//       source: new OSM(),
//     }),
//     new TileLayer({
//       source: new TileDebug(),
//     }),
//   ],
//   target: 'map',
//   view: new View({
//     center: [0, 0],
//     zoom: 1,
//   }),
// });
