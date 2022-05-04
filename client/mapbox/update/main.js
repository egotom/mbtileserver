var mapView;

$(function() {
	var baseUrl='http://localhost:8000';
	var mapStyle=null;
	var map = null;
	var draw = null;
	var bar = null;
	var cancellationToken = null;
	var requests = [];

	function initializeMap() {
		mapboxgl.accessToken = 'pk.eyJ1IjoiYWxpYXNocmFmIiwiYSI6ImNqdXl5MHV5YTAzNXI0NG51OWFuMGp4enQifQ.zpd2gZFwBTRqiapp1yci9g';
		map = new mapboxgl.Map({
			container: 'map-view',
			style: mapStyle, 
			center: [121.540,31.233], 
			zoom: 9
		});
	}

	function initializeRectangleTool() {
		var modes = MapboxDraw.modes;
		modes.draw_rectangle = DrawRectangle.default;
		draw = new MapboxDraw({
			modes: modes
		});
		map.addControl(draw);
		map.on('draw.create', function (e) {
			M.Toast.dismissAll();
		});
		$("#rectangle-draw-button").click(function() {
			startDrawing();
		})
	}

	function startDrawing() {
		removeGrid();
		draw.deleteAll();
		draw.changeMode('draw_rectangle');
		M.Toast.dismissAll();
		M.toast({html: '在地图上选择两点确定一个矩形区域。', displayLength: 7000})
	}

	function initializeGridPreview() {
		$("#grid-preview-button").click(previewGrid);
		map.on('click', showTilePopup);
	}

	function showTilePopup(e) {
		if(!e.originalEvent.ctrlKey) {
			return;
		}
		var maxZoom = getMaxZoom();
		var x = lat2tile(e.lngLat.lat, maxZoom);
		var y = long2tile(e.lngLat.lng, maxZoom);
		var content = "X, Y, Z<br/><b>" + x + ", " + y + ", " + maxZoom + "</b><hr/>";
		content += "Lat, Lng<br/><b>" + e.lngLat.lat + ", " + e.lngLat.lng + "</b>";
        new mapboxgl.Popup()
			.setLngLat(e.lngLat)
            .setHTML(content)
            .addTo(map);
        console.log(e.lngLat)
	}

	function long2tile(lon,zoom) {
		return (Math.floor((lon+180)/360*Math.pow(2,zoom)));
	}

	function lat2tile(lat,zoom)  {
		return (Math.floor((1-Math.log(Math.tan(lat*Math.PI/180) + 1/Math.cos(lat*Math.PI/180))/Math.PI)/2 *Math.pow(2,zoom)));
	}

	function tile2long(x,z) {
		return (x/Math.pow(2,z)*360-180);
	}

	function tile2lat(y,z) {
		var n=Math.PI-2*Math.PI*y/Math.pow(2,z);
		return (180/Math.PI*Math.atan(0.5*(Math.exp(n)-Math.exp(-n))));
	}

	function getTileRect(x, y, zoom) {
		var c1 = new mapboxgl.LngLat(tile2long(x, zoom), tile2lat(y, zoom));
		var c2 = new mapboxgl.LngLat(tile2long(x + 1, zoom), tile2lat(y + 1, zoom));
		return new mapboxgl.LngLatBounds(c1, c2);
	}

	function getMinZoom() {
		return Math.min(parseInt($("#zoom-from-box").val()), parseInt($("#zoom-to-box").val()));
	}

	function getMaxZoom() {
		return Math.max(parseInt($("#zoom-from-box").val()), parseInt($("#zoom-to-box").val()));
	}

	function getArrayByBounds(bounds) {
		var tileArray = [
			[ bounds.getSouthWest().lng, bounds.getNorthEast().lat ],
			[ bounds.getNorthEast().lng, bounds.getNorthEast().lat ],
			[ bounds.getNorthEast().lng, bounds.getSouthWest().lat ],
			[ bounds.getSouthWest().lng, bounds.getSouthWest().lat ],
			[ bounds.getSouthWest().lng, bounds.getNorthEast().lat ],
		];
		return tileArray;
	}

	function getPolygonByBounds(bounds) {
		var tilePolygonData = getArrayByBounds(bounds);
		var polygon = turf.polygon([tilePolygonData]);
		return polygon;
	}

	function isTileInSelection(tileRect) {
		var polygon = getPolygonByBounds(tileRect);
		var areaPolygon = draw.getAll().features[0];
		if(turf.booleanDisjoint(polygon, areaPolygon) == false) {
			return true;
		}
		return false;
	}

	function getBounds() {
		var coordinates = draw.getAll().features[0].geometry.coordinates[0];
		var bounds = coordinates.reduce(function(bounds, coord) {
			return bounds.extend(coord);
		}, new mapboxgl.LngLatBounds(coordinates[0], coordinates[0]));
		return bounds;
	}

	function getGrid(zoomLevel) {
		var bounds = getBounds();
		var rects = [];
		//var thisZoom = zoomLevel - (outputScale-1)
		var thisZoom = zoomLevel
		var TY = lat2tile(bounds.getNorthEast().lat, thisZoom);
		var LX = long2tile(bounds.getSouthWest().lng, thisZoom);
		var BY = lat2tile(bounds.getSouthWest().lat, thisZoom);
		var RX = long2tile(bounds.getNorthEast().lng, thisZoom);
		for(var y = TY; y <= BY; y++) {
			for(var x = LX; x <= RX; x++) {
				var rect = getTileRect(x, y, thisZoom);
				if(isTileInSelection(rect)) {
					rects.push({x: x, y: y, z: thisZoom, rect: rect});
				}
			}
		}
		return rects
	}

	function getAllGridTiles() {
		var allTiles = [];
		for(var z = getMinZoom(); z <= getMaxZoom(); z++) {
			var grid = getGrid(z);
			// TODO shuffle grid via a heuristic (hamlet curve? :/)
			allTiles = allTiles.concat(grid);
		}
		return allTiles;
	}

	function removeGrid() {
		removeLayer("grid-preview");
	}

	function previewGrid() {
		var maxZoom = getMaxZoom();
		var grid = getGrid(maxZoom);
		var pointsCollection = []
		for(var i in grid) {
			var feature = grid[i];
			var array = getArrayByBounds(feature.rect);
			pointsCollection.push(array);
		}
		removeGrid();
		map.addLayer({
			'id': "grid-preview",
			'type': 'line',
			'source': {
				'type': 'geojson',
				'data': turf.polygon(pointsCollection),
			},
			'layout': {},
			'paint': {
				"line-color": "#fa8231",
				"line-width": 3,
			}
		});
		var totalTiles = getAllGridTiles().length;
		M.toast({html: '该区域总共 ' + totalTiles.toLocaleString() + ' 个切片.', displayLength: 5000})
	}

	function previewRect(rectInfo) {
		var array = getArrayByBounds(rectInfo.rect);
		var id = "temp-" + rectInfo.x + '-' + rectInfo.y + '-' + rectInfo.z;
		map.addLayer({
			'id': id,
			'type': 'line',
			'source': {
				'type': 'geojson',
				'data': turf.polygon([array]),
			},
			'layout': {},
			'paint': {
				"line-color": "#ff9f1a",
				"line-width": 3,
			}
		});
		return id;
	}

	function removeLayer(id) {
		if(map.getSource(id) != null) {
			map.removeLayer(id);
			map.removeSource(id);
		}
	}

	function generateQuadKey(x, y, z) {
	    var quadKey = [];
	    for (var i = z; i > 0; i--) {
	        var digit = '0';
	        var mask = 1 << (i - 1);
	        if ((x & mask) != 0) {
	            digit++;
	        }
	        if ((y & mask) != 0) {
	            digit++;
	            digit++;
	        }
	        quadKey.push(digit);
	    }
	    return quadKey.join('');
	}

	function initializeDownloader() {
		bar = new ProgressBar.Circle($('#progress-radial').get(0), {
			strokeWidth: 12,
			easing: 'easeOut',
			duration: 200,
			trailColor: '#eee',
			trailWidth: 1,
			from: {color: '#0fb9b1', a:0},
			to: {color: '#20bf6b', a:1},
			svgStyle: null,
			step: function(state, circle) {
				circle.path.setAttribute('stroke', state.color);
			}
		});
		$("#download-button").click(startDownloading);
		$("#stop-button").click(stopDownloading);
	}

	function showTinyTile(base64) {
		var currentImages = $(".tile-strip img");
		for(var i = 4; i < currentImages.length; i++) {
			$(currentImages[i]).remove();
		}
		var image = $("<img/>").attr('src', "data:image/png;base64, " + base64)
		var strip = $(".tile-strip");
		strip.prepend(image)
	}

	async function startDownloading() {
		if(draw.getAll().features.length == 0) {
			M.toast({html: '先选择下载区域.', displayLength: 3000})
			return;
		}
		cancellationToken = false; 
		requests = [];
		$("#main-sidebar").hide();
		$("#download-sidebar").show();
		$(".tile-strip").html("");
		$("#stop-button").html("停止");
		removeGrid();
		clearLogs();
		M.Toast.dismissAll();
		var timestamp = Date.now().toString();
		var allTiles = getAllGridTiles();
		
		updateProgress(0, allTiles.length);
		var bounds = getBounds();
		var boundsArray = [bounds.getSouthWest().lng, bounds.getSouthWest().lat, bounds.getNorthEast().lng, bounds.getNorthEast().lat]
		var centerArray = [bounds.getCenter().lng, bounds.getCenter().lat, getMaxZoom()]

		let i = 0;
		async.eachLimit(allTiles, 16, function(item, done) {
			if(cancellationToken) {
				return;
			}
			var boxLayer = previewRect(item);
			var data = new FormData();
			data.append('x', item.x)
			data.append('y', item.y)
			data.append('z', item.z)
			data.append('quad', generateQuadKey(item.x, item.y, item.z))
			data.append('timestamp', timestamp)
			data.append('bounds', boundsArray.join(","))
			data.append('center', centerArray.join(","))

			var request = $.ajax({
				"url": baseUrl+"/services/b/tiles/download",
				async: true,
				timeout: 30 * 1000,
				type: "POST",
			    contentType: false,
			    processData: false,
				data: data,
				dataType: 'json',
			}).done(function(data) {
				if(cancellationToken) {
					return;
				}
				if(data.code == 200) {
					//showTinyTile(data.image)
					logItem(item.x, item.y, item.z, data.message);
				} else {
					logItem(item.x, item.y, item.z, data.code + " 下载切片失败！");
				}

			}).fail(function(data, textStatus, errorThrown) {
				if(cancellationToken) {
					return;
				}
				logItem(item.x, item.y, item.z, "传输切片失败！");
				//allTiles.push(item);
				//console.log(data,"------------",textStatus,errorThrown);
			}).always(function(data) {
				i++;
				removeLayer(boxLayer);
				updateProgress(i, allTiles.length);
				done();
				if(cancellationToken) {
					return;
				}
				$("#stop-button").css("background-color", "rgb(200,100,100)");
			});
			requests.push(request);
		}, async function(err) {
			await $.ajax({
				url: baseUrl+"/services/b/tiles/end-download",
				async: true,
				timeout: 30 * 1000,
				type: "post",
				contentType: false,
				processData: false,
				data: {},
				dataType: 'json',
			})
			updateProgress(allTiles.length, allTiles.length);
			logItemRaw("完成");
			$("#stop-button").html("完成");
			$("#stop-button").css("color", "white");
			$("#stop-button").css("background-color", "rgb(32,191,107)");
		});
	}

	function updateProgress(value, total) {
		var progress = value / total;
		bar.animate(progress);
		bar.setText(Math.round(progress * 100) + '<span>%</span>');
		$("#progress-subtitle").html(value.toLocaleString() + " <span>out of</span> " + total.toLocaleString())
	}

	function logItem(x, y, z, text) {
		logItemRaw(x + ',' + y + ',' + z + ' : ' + text)
	}

	function logItemRaw(text) {
		var logger = $('#log-view');
		logger.val(logger.val() + '\n' + text);
		logger.scrollTop(logger[0].scrollHeight);
	}

	function clearLogs() {
		var logger = $('#log-view');
		logger.val('');
	}

	function stopDownloading() {
		cancellationToken = true;

		for(var i =0 ; i < requests.length; i++) {
			var request = requests[i];
			try {
				request.abort();
			} catch(e) {

			}
		}

		$("#main-sidebar").show();
		$("#download-sidebar").hide();
		removeGrid();
		clearLogs();
	}

	function initMapSource(){
		$('.dropdown-trigger').dropdown({constrainWidth: false});
		$.ajax({
			"url": baseUrl+"/services",
			async: true,
			timeout: 30 * 1000,
			type: "GET",
			contentType: false,
			processData: false,
			dataType: 'json',
		}).done(function(data) {
			$("#source-box").val(data[0].url);
			var dropdown = $("#sources");
			mapStyle={
				'version': 8,
				'sources': {
					'raster-tiles': {
						'type': 'raster',
						'tiles': [baseUrl+"/services/"+data[0].name+"/tiles/{z}/{x}/{y}.png"],
						'tileSize': 256,
						'attribution':'Map tiles by Bing'
					}
				},
				'layers': [
					{
						'id': 'simple-tiles',
						'type': 'raster',
						'source': 'raster-tiles',
						'minzoom': 0,
						'maxzoom': 18
					}
				]
			};
			
			for(var key of data) {
				var url = key.url;
				var item = $("<li><a></a></li>");
				item.attr("data-url", url);
				item.find("a").text(key.name);
				item.click(function() {
					var url = $(this).attr("data-url");
					$("#source-box").val(url);
					map.setStyle({
						'version': 8,
						'sources': {
							'raster-tiles': {
								'type': 'raster',
								'tiles': [baseUrl+"/services/"+$(this).find("a").text()+"/tiles/{z}/{x}/{y}.png"],
								'tileSize': 256,
								'attribution':'Map tiles by Bing'
							}
						},
						'layers': [
							{
								'id': 'simple-tiles',
								'type': 'raster',
								'source': 'raster-tiles',
								'minzoom': 0,
								'maxzoom': 18
							}
						]
					});
				});
				dropdown.append(item);
			}
			initializeMap();
			initializeRectangleTool();
			initializeGridPreview();
		});
	}

	initMapSource();
	// initializeMap();
	//initializeRectangleTool();
	// initializeGridPreview();
	initializeDownloader();
});