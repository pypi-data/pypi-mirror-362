"use strict";
(self["webpackChunkpyams_app_msc"] = self["webpackChunkpyams_app_msc"] || []).push([["pkg_js__calendar_js"],{

/***/ "./pkg/js/_calendar.js":
/*!*****************************!*\
  !*** ./pkg/js/_calendar.js ***!
  \*****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _fullcalendar_core__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @fullcalendar/core */ "./node_modules/@fullcalendar/core/index.js");
/* harmony import */ var _fullcalendar_daygrid__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @fullcalendar/daygrid */ "./node_modules/@fullcalendar/daygrid/index.js");
/* harmony import */ var _fullcalendar_list__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @fullcalendar/list */ "./node_modules/@fullcalendar/list/index.js");
/* harmony import */ var _fullcalendar_interaction__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @fullcalendar/interaction */ "./node_modules/@fullcalendar/interaction/index.js");
/* harmony import */ var _fullcalendar_bootstrap__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @fullcalendar/bootstrap */ "./node_modules/@fullcalendar/bootstrap/index.js");
/* provided dependency */ var $ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");





var isSmallDevice = function isSmallDevice() {
  return window.innerWidth < 768;
};
var createCalendar = function createCalendar(calendar, config, options, callback) {
  return new Promise(function (resolve, reject) {
    var data = calendar.data();
    var settings = {
      plugins: [_fullcalendar_interaction__WEBPACK_IMPORTED_MODULE_0__["default"], _fullcalendar_daygrid__WEBPACK_IMPORTED_MODULE_1__["default"], _fullcalendar_list__WEBPACK_IMPORTED_MODULE_2__["default"], _fullcalendar_bootstrap__WEBPACK_IMPORTED_MODULE_3__["default"]],
      initialView: isSmallDevice() ? 'listMonth' : 'dayGridMonth',
      themeSystem: 'bootstrap',
      locale: $('html').attr('lang'),
      headerToolbar: {
        start: 'title',
        center: 'today',
        right: 'prev,next'
      },
      bootstrapFontAwesome: {
        prev: 'fa-chevron-left',
        next: 'fa-chevron-right'
      },
      firstDay: 1,
      weekNumberCalculation: 'ISO',
      eventDidMount: PyAMS_calendar.mountedEvent,
      eventClick: PyAMS_calendar.clickEvent
    };
    settings = $.extend({}, settings, config, options);
    calendar.trigger('calendar.init', [calendar, settings]);
    var instance = new _fullcalendar_core__WEBPACK_IMPORTED_MODULE_4__.Calendar(calendar.get(0), settings);
    calendar.trigger('calendar.finishing', [calendar, instance, settings]);
    if (callback) {
      callback(instance, config);
    }
    calendar.trigger('calendar.finished', [calendar, instance, settings]);
    instance.render();
    resolve(instance);
  });
};
var PyAMS_calendar = {
  init: function init(calendars, options, callback) {
    var $calendars = $.map(calendars, function (elt) {
      return new Promise(function (resolve, reject) {
        var calendar = $(elt),
          data = calendar.data(),
          config = data.calendarConfig;
        if (config) {
          resolve(createCalendar(calendar, config, options, callback));
        } else {
          $.get(data.calendarUrl || 'get-calendar-configuration.json', function (config) {
            resolve(createCalendar(calendar, config, options, callback));
          });
        }
      });
    });
    $.when.apply($, $calendars).then();
  },
  mountedEvent: function mountedEvent(info) {
    var elt = $(info.el),
      lang = $('html').attr('lang'),
      startDate = new Intl.DateTimeFormat(lang, {
        hour: '2-digit',
        minute: '2-digit'
      }).format(info.event.start);
    elt.tooltip({
      title: "".concat(startDate, " - ").concat(info.event.title)
    });
  },
  clickEvent: function clickEvent(info) {
    var _event$extendedProps;
    var event = info.event,
      href = (_event$extendedProps = event.extendedProps) === null || _event$extendedProps === void 0 ? void 0 : _event$extendedProps.href;
    if (href) {
      window.location.href = href;
    }
  }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (PyAMS_calendar);

/***/ })

}]);
//# sourceMappingURL=pkg_js__calendar_js.js.map