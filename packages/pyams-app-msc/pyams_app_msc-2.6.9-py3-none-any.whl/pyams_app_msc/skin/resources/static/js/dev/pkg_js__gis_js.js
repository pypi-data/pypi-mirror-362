"use strict";
(self["webpackChunkpyams_app_msc"] = self["webpackChunkpyams_app_msc"] || []).push([["pkg_js__gis_js"],{

/***/ "./pkg/js/_gis.js":
/*!************************!*\
  !*** ./pkg/js/_gis.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./_utils */ "./pkg/js/_utils.js");
/* provided dependency */ var $ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
function _typeof(o) { "@babel/helpers - typeof"; return _typeof = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function (o) { return typeof o; } : function (o) { return o && "function" == typeof Symbol && o.constructor === Symbol && o !== Symbol.prototype ? "symbol" : typeof o; }, _typeof(o); }
function ownKeys(e, r) { var t = Object.keys(e); if (Object.getOwnPropertySymbols) { var o = Object.getOwnPropertySymbols(e); r && (o = o.filter(function (r) { return Object.getOwnPropertyDescriptor(e, r).enumerable; })), t.push.apply(t, o); } return t; }
function _objectSpread(e) { for (var r = 1; r < arguments.length; r++) { var t = null != arguments[r] ? arguments[r] : {}; r % 2 ? ownKeys(Object(t), !0).forEach(function (r) { _defineProperty(e, r, t[r]); }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(e, Object.getOwnPropertyDescriptors(t)) : ownKeys(Object(t)).forEach(function (r) { Object.defineProperty(e, r, Object.getOwnPropertyDescriptor(t, r)); }); } return e; }
function _defineProperty(e, r, t) { return (r = _toPropertyKey(r)) in e ? Object.defineProperty(e, r, { value: t, enumerable: !0, configurable: !0, writable: !0 }) : e[r] = t, e; }
function _toPropertyKey(t) { var i = _toPrimitive(t, "string"); return "symbol" == _typeof(i) ? i : i + ""; }
function _toPrimitive(t, r) { if ("object" != _typeof(t) || !t) return t; var e = t[Symbol.toPrimitive]; if (void 0 !== e) { var i = e.call(t, r || "default"); if ("object" != _typeof(i)) return i; throw new TypeError("@@toPrimitive must return a primitive value."); } return ("string" === r ? String : Number)(t); }
function _slicedToArray(r, e) { return _arrayWithHoles(r) || _iterableToArrayLimit(r, e) || _unsupportedIterableToArray(r, e) || _nonIterableRest(); }
function _nonIterableRest() { throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); }
function _iterableToArrayLimit(r, l) { var t = null == r ? null : "undefined" != typeof Symbol && r[Symbol.iterator] || r["@@iterator"]; if (null != t) { var e, n, i, u, a = [], f = !0, o = !1; try { if (i = (t = t.call(r)).next, 0 === l) { if (Object(t) !== t) return; f = !1; } else for (; !(f = (e = i.call(t)).done) && (a.push(e.value), a.length !== l); f = !0); } catch (r) { o = !0, n = r; } finally { try { if (!f && null != t["return"] && (u = t["return"](), Object(u) !== u)) return; } finally { if (o) throw n; } } return a; } }
function _arrayWithHoles(r) { if (Array.isArray(r)) return r; }
function _createForOfIteratorHelper(r, e) { var t = "undefined" != typeof Symbol && r[Symbol.iterator] || r["@@iterator"]; if (!t) { if (Array.isArray(r) || (t = _unsupportedIterableToArray(r)) || e && r && "number" == typeof r.length) { t && (r = t); var _n = 0, F = function F() {}; return { s: F, n: function n() { return _n >= r.length ? { done: !0 } : { done: !1, value: r[_n++] }; }, e: function e(r) { throw r; }, f: F }; } throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); } var o, a = !0, u = !1; return { s: function s() { t = t.call(r); }, n: function n() { var r = t.next(); return a = r.done, r; }, e: function e(r) { u = !0, o = r; }, f: function f() { try { a || null == t["return"] || t["return"](); } finally { if (u) throw o; } } }; }
function _unsupportedIterableToArray(r, a) { if (r) { if ("string" == typeof r) return _arrayLikeToArray(r, a); var t = {}.toString.call(r).slice(8, -1); return "Object" === t && r.constructor && (t = r.constructor.name), "Map" === t || "Set" === t ? Array.from(r) : "Arguments" === t || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(t) ? _arrayLikeToArray(r, a) : void 0; } }
function _arrayLikeToArray(r, a) { (null == a || a > r.length) && (a = r.length); for (var e = 0, n = Array(a); e < a; e++) n[e] = r[e]; return n; }

var createMap = function createMap(map, config, options, callback) {
  return new Promise(function (resolve, reject) {
    var data = map.data();
    var settings = {
      preferCanvas: data.mapLeafletPreferCanvas || false,
      attributionControl: data.mapLeafletAttributionControl === undefined ? config.attributionControl : data.mapLeafletAttributionControl,
      zoomControl: data.mapLeafletZoomControl === undefined ? config.zoomControl : data.mapLeafletZoomControl,
      fullscreenControl: data.mapLeafletFullscreen === undefined ? config.fullscreenControl && {
        pseudoFullscreen: true
      } || null : data.mapLeafletFullscreen,
      crs: data.mapLeafletCrs || _utils__WEBPACK_IMPORTED_MODULE_0__["default"].getObject(config.crs) || L.CRS.EPSG3857,
      center: data.mapLeafletCenter || config.center,
      zoom: data.mapLeafletZoom || config.zoom,
      gestureHandling: data.mapLeafletWheelZoom === undefined ? !config.scrollWheelZoom : data.mapLeafletWheelZoom,
      keyboard: data.mapLeafletKeyboard === undefined ? config.keyboard && !L.Browser.mobile : data.amsLeafletKeyboard
    };
    settings = $.extend({}, settings, options);
    map.trigger('map.init', [map, settings, config]);
    var leafmap = L.map(map.attr('id'), settings),
      layersConfig = [],
      baseLayers = {},
      overlayLayers = {};
    if (config.layers) {
      var _iterator = _createForOfIteratorHelper(config.layers),
        _step;
      try {
        for (_iterator.s(); !(_step = _iterator.n()).done;) {
          var layerConfig = _step.value;
          map.trigger('map.layer.init', [map, layerConfig]);
          layersConfig.push(PyAMS_GIS.getLayer(map, leafmap, layerConfig));
        }
      } catch (err) {
        _iterator.e(err);
      } finally {
        _iterator.f();
      }
    } else {
      layersConfig.push(L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        name: 'osm',
        title: 'OpenStreetMap',
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      }));
    }
    $.when.apply($, layersConfig).then(function () {
      for (var _len = arguments.length, layers = new Array(_len), _key = 0; _key < _len; _key++) {
        layers[_key] = arguments[_key];
      }
      for (var _i = 0, _Object$entries = Object.entries(layers); _i < _Object$entries.length; _i++) {
        var _Object$entries$_i = _slicedToArray(_Object$entries[_i], 2),
          idx = _Object$entries$_i[0],
          layer = _Object$entries$_i[1];
        if (config.layers) {
          if (config.layers[idx].isVisible) {
            layer.addTo(leafmap);
          }
          if (config.layers[idx].isOverlay) {
            overlayLayers[config.layers[idx].title] = layer;
          } else {
            baseLayers[config.layers[idx].title] = layer;
          }
        } else {
          layer.addTo(leafmap);
        }
      }
      if (config.zoomControl && data.mapLeafletHideZoomControl !== true) {
        L.control.scale().addTo(leafmap);
      }
      if (config.layerControl) {
        L.control.layers(baseLayers, overlayLayers).addTo(leafmap);
      }
      if (config.center) {
        leafmap.setView(new L.LatLng(config.center.lat, config.center.lon), config.zoom || 13);
      } else if (config.bounds) {
        leafmap.fitBounds(config.bounds);
      }
      if (config.marker) {
        var icon = L.icon({
          iconUrl: '/--static--/pyams_gis/img/marker-icon.png',
          iconSize: [25, 41],
          iconAnchor: [12, 39]
        });
        var marker = L.marker();
        marker.setIcon(icon);
        marker.setLatLng({
          lon: config.marker.lon,
          lat: config.marker.lat
        });
        marker.addTo(leafmap);
      }
      map.data('leafmap', leafmap);
      map.data('leafmap.config', config);
      map.data('leafmap.layers', layers.reduce(function (res, layer) {
        return _objectSpread(_objectSpread({}, res), {}, _defineProperty({}, layer.options.name, layer));
      }, {}));
      map.trigger('map.finishing', [map, leafmap, config]);
      if (callback) {
        callback(leafmap, config);
      }
      map.trigger('map.finished', [map, leafmap, config]);
      resolve(leafmap);
    });
  });
};
var PyAMS_GIS = {
  /**
   * Map initialization
   *
   * @param maps: maps elements
   * @param options: optional maps configuration settings
   * @param callback: maps initialization callback
   */
  init: function init(maps, options, callback) {
    window.PyAMS_GIS = PyAMS_GIS;
    Promise.all([__webpack_require__.e(/*! import() */ "vendors-node_modules_leaflet_dist_leaflet-src_js").then(__webpack_require__.t.bind(__webpack_require__, /*! leaflet */ "./node_modules/leaflet/dist/leaflet-src.js", 23)), __webpack_require__.e(/*! import() */ "vendors-node_modules_leaflet_dist_leaflet_css").then(__webpack_require__.bind(__webpack_require__, /*! leaflet/dist/leaflet.css */ "./node_modules/leaflet/dist/leaflet.css"))]).then(function () {
      Promise.all([__webpack_require__.e(/*! import() */ "vendors-node_modules_leaflet-gesture-handling_dist_leaflet-gesture-handling_min_js").then(__webpack_require__.t.bind(__webpack_require__, /*! leaflet-gesture-handling */ "./node_modules/leaflet-gesture-handling/dist/leaflet-gesture-handling.min.js", 23)), __webpack_require__.e(/*! import() */ "node_modules_leaflet-gesture-handling_dist_leaflet-gesture-handling_css").then(__webpack_require__.bind(__webpack_require__, /*! leaflet-gesture-handling/dist/leaflet-gesture-handling.css */ "./node_modules/leaflet-gesture-handling/dist/leaflet-gesture-handling.css")), __webpack_require__.e(/*! import() */ "node_modules_leaflet-fullscreen_dist_Leaflet_fullscreen_js").then(__webpack_require__.t.bind(__webpack_require__, /*! leaflet-fullscreen */ "./node_modules/leaflet-fullscreen/dist/Leaflet.fullscreen.js", 23)), __webpack_require__.e(/*! import() */ "node_modules_leaflet-fullscreen_dist_leaflet_fullscreen_css").then(__webpack_require__.bind(__webpack_require__, /*! leaflet-fullscreen/dist/leaflet.fullscreen.css */ "./node_modules/leaflet-fullscreen/dist/leaflet.fullscreen.css"))]).then(function () {
        var $maps = $.map(maps, function (elt) {
          return new Promise(function (resolve, reject) {
            var map = $(elt),
              data = map.data(),
              config = data.mapConfiguration;
            if (config) {
              resolve(createMap(map, config, options, callback));
            } else {
              $.get(data.mapConfigurationUrl || 'get-map-configuration.json').then(function (config) {
                createMap(map, config, options, callback).then(function (leafmap) {
                  resolve({
                    'leafmap': leafmap,
                    'config': config
                  });
                });
              });
            }
          });
        });
        $.when.apply($, $maps).then();
      });
    });
  },
  /**
   * Get layer definition
   *
   * @param map: source map element
   * @param leafmap: current Leaflet map
   * @param layer: current layer definition
   */
  getLayer: function getLayer(map, leafmap, layer) {
    return new Promise(function (resolve, reject) {
      var factory = _utils__WEBPACK_IMPORTED_MODULE_0__["default"].getObject(layer.factory);
      if (factory !== undefined) {
        delete layer.factory;
        var deferred = [];
        if (layer.dependsOn) {
          for (var name in layer.dependsOn) {
            if (!layer.dependsOn.hasOwnProperty(name)) {
              continue;
            }
            if (_utils__WEBPACK_IMPORTED_MODULE_0__["default"].getObject(name) === undefined) {
              deferred.push(_utils__WEBPACK_IMPORTED_MODULE_0__["default"].getScript(layer.dependsOn[name]));
            }
          }
          delete layer.dependsOn;
        }
        $.when.apply($, deferred).then(function () {
          resolve(factory(map, leafmap, layer));
        });
      }
    });
  },
  /**
   * Layers factories
   */
  factory: {
    GeoJSON: function GeoJSON(map, leafmap, layer) {
      var url = layer.url;
      delete layer.url;
      var result = L.geoJSON(null, layer);
      map.on('map.finished', function (evt, map, leafmap, config) {
        $.get(url, function (data) {
          result.addData(data.geometry, {
            style: layer.style
          });
          if (config.fitLayer === layer.name) {
            leafmap.fitBounds(result.getBounds());
          }
        });
      });
      return result;
    },
    TileLayer: function TileLayer(map, leafmap, layer) {
      var url = layer.url;
      delete layer.url;
      return L.tileLayer(url, layer);
    },
    WMS: function WMS(map, leafmap, layer) {
      var url = layer.url;
      delete layer.url;
      return L.tileLayer.wms(url, layer);
    },
    Geoportal: {
      WMS: function WMS(map, leafmap, layer) {
        _utils__WEBPACK_IMPORTED_MODULE_0__["default"].getCSS('/--static--/pyams_gis/css/GpPluginLeaflet.min.css', 'geoportal');
        return L.geoportalLayer.WMS(layer);
      }
    },
    ESRI: {
      Feature: function Feature(map, leafmap, layer) {
        return L.esri.featureLayer(layer);
      }
    },
    Google: function Google(map, leafmap, layer) {
      var apiKey = layer.apiKey;
      delete layer.apiKey;
      if (_utils__WEBPACK_IMPORTED_MODULE_0__["default"].getObject('window.google.maps') === undefined) {
        var script = _utils__WEBPACK_IMPORTED_MODULE_0__["default"].getScript('https://maps.googleapis.com/maps/api/js?key=' + apiKey);
        $.when.apply($, [script]);
      }
      return L.gridLayer.googleMutant(layer);
    }
  }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (PyAMS_GIS);

/***/ })

}]);
//# sourceMappingURL=pkg_js__gis_js.js.map