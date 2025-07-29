"use strict";
(self["webpackChunkpyams_app_msc"] = self["webpackChunkpyams_app_msc"] || []).push([["pkg_js__form_js"],{

/***/ "./pkg/js/_form.js":
/*!*************************!*\
  !*** ./pkg/js/_form.js ***!
  \*************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var jquery_form__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! jquery-form */ "./node_modules/jquery-form/dist/jquery.form.min.js");
/* harmony import */ var jquery_form__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(jquery_form__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var jquery_validation__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! jquery-validation */ "./node_modules/jquery-validation/dist/jquery.validate.js");
/* harmony import */ var jquery_validation__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(jquery_validation__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var jsrender__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! jsrender */ "./node_modules/jsrender/jsrender.js");
/* harmony import */ var jsrender__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(jsrender__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var jquery_scrollto__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! jquery.scrollto */ "./node_modules/jquery.scrollto/jquery.scrollTo.js");
/* harmony import */ var jquery_scrollto__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(jquery_scrollto__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./_utils */ "./pkg/js/_utils.js");
/* provided dependency */ var $ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
function _createForOfIteratorHelper(r, e) { var t = "undefined" != typeof Symbol && r[Symbol.iterator] || r["@@iterator"]; if (!t) { if (Array.isArray(r) || (t = _unsupportedIterableToArray(r)) || e && r && "number" == typeof r.length) { t && (r = t); var _n = 0, F = function F() {}; return { s: F, n: function n() { return _n >= r.length ? { done: !0 } : { done: !1, value: r[_n++] }; }, e: function e(r) { throw r; }, f: F }; } throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); } var o, a = !0, u = !1; return { s: function s() { t = t.call(r); }, n: function n() { var r = t.next(); return a = r.done, r; }, e: function e(r) { u = !0, o = r; }, f: function f() { try { a || null == t["return"] || t["return"](); } finally { if (u) throw o; } } }; }
function _unsupportedIterableToArray(r, a) { if (r) { if ("string" == typeof r) return _arrayLikeToArray(r, a); var t = {}.toString.call(r).slice(8, -1); return "Object" === t && r.constructor && (t = r.constructor.name), "Map" === t || "Set" === t ? Array.from(r) : "Arguments" === t || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(t) ? _arrayLikeToArray(r, a) : void 0; } }
function _arrayLikeToArray(r, a) { (null == a || a > r.length) && (a = r.length); for (var e = 0, n = Array(a); e < a; e++) n[e] = r[e]; return n; }





var ERRORS_TEMPLATE_STRING = "\n\t<div class=\"alert alert-{{:status}}\" role=\"alert\">\n\t\t<button type=\"button\" class=\"close\" data-dismiss=\"alert\" \n\t\t\t\taria-label=\"{{*: MyAMS.i18n.BTN_CLOSE }}\">\n\t\t\t<i class=\"fa fa-times\" aria-hidden=\"true\"></i>\n\t\t</button>\n\t\t{{if header}}\n\t\t<h5 class=\"alert-heading\">{{:header}}</h5>\n\t\t{{/if}}\n\t\t{{if message}}\n\t\t<p>{{:message}}</p>\n\t\t{{/if}}\n\t\t{{if messages}}\n\t\t<ul>\n\t\t{{for messages}}\n\t\t\t<li>\n\t\t\t\t{{if header}}<strong>{{:header}} :</strong>{{/if}}\n\t\t\t\t{{:message}}\n\t\t\t</li>\n\t\t{{/for}}\n\t\t</ul>\n\t\t{{/if}}\n\t\t{{if widgets}}\n\t\t<ul>\n\t\t{{for widgets}}\n\t\t\t<li>\n\t\t\t\t{{if header}}<strong>{{:header}} :</strong>{{/if}}\n\t\t\t\t{{:message}}\n\t\t\t</li>\n\t\t{{/for}}\n\t\t</ul>\n\t\t{{/if}}\n\t</div>";
var ERROR_TEMPLATE = $.templates({
  markup: ERRORS_TEMPLATE_STRING,
  allowCode: true
});

/**
 * Clear form messages
 */
var clearMessages = function clearMessages(form) {
  $('.alert-success, SPAN.state-success', form).not('.persistent').remove();
  $('.state-success', form).removeClassPrefix('state-');
  $('.invalid-feedback', form).remove();
  $('.is-invalid', form).removeClass('is-invalid');
};

/**
 * Clear form alerts
 */
var clearAlerts = function clearAlerts(form) {
  $('.alert-danger, SPAN.state-error', form).not('.persistent').remove();
  $('.state-error', form).removeClassPrefix('state-');
  $('.invalid-feedback', form).remove();
  $('.is-invalid', form).removeClass('is-invalid');
};
var PyAMS_form = {
  init: function init(forms) {
    $('label', forms).removeClass('col-md-3');
    $('.col-md-9', forms).removeClass('col-md-9');
    $('input, select, textarea', forms).addClass('form-control');
    $('button', forms).addClass('border');
    $('button[type="submit"]', forms).addClass('btn-primary');
    var lang = $('html').attr('lang');

    //
    // Initialize input masks
    //

    var inputs = $('input[data-input-mask]');
    if (inputs.length > 0) {
      __webpack_require__.e(/*! import() */ "vendors-node_modules_inputmask_dist_inputmask_js").then(__webpack_require__.t.bind(__webpack_require__, /*! inputmask */ "./node_modules/inputmask/dist/inputmask.js", 23)).then(function () {
        inputs.each(function (idx, elt) {
          var input = $(elt),
            data = input.data(),
            defaultOptions = {
              autoUnmask: true,
              clearIncomplete: true,
              removeMaskOnSubmit: true
            },
            settings = $.extend({}, defaultOptions, data.amsInputMaskOptions || data.amsOptions || data.options),
            veto = {
              veto: false
            };
          input.trigger('before-init.ams.inputmask', [input, settings, veto]);
          if (veto.veto) {
            return;
          }
          var mask = new Inputmask(data.inputMask, settings),
            plugin = mask.mask(elt);
          input.trigger('after-init.ams.inputmask', [input, plugin]);
        });
      });
    }

    //
    // Initialize select2 widgets
    //

    var selects = $('.select2');
    if (selects.length > 0) {
      __webpack_require__.e(/*! import() */ "vendors-node_modules_select2_dist_js_select2_js").then(__webpack_require__.t.bind(__webpack_require__, /*! select2 */ "./node_modules/select2/dist/js/select2.js", 23)).then(function () {
        selects.each(function (idx, elt) {
          var select = $(elt),
            data = select.data(),
            defaultOptions = {
              theme: data.amsSelect2Options || data.amsTheme || 'bootstrap',
              language: data.amsSelect2Language || data.amsLanguage || lang
            },
            ajaxUrl = data.amsSelect2AjaxUrl || data.amsAjaxUrl || data['ajax-Url'];
          if (ajaxUrl) {
            // check AJAX data helper function
            var ajaxParamsHelper;
            var ajaxParams = _utils__WEBPACK_IMPORTED_MODULE_4__["default"].getFunctionByName(data.amsSelect2AjaxParams || data.amsAjaxParams || data['ajax-Params']) || data.amsSelect2AjaxParams || data.amsAjaxParams || data['ajax-Params'];
            if (typeof ajaxParams === 'function') {
              ajaxParamsHelper = ajaxParams;
            } else if (ajaxParams) {
              ajaxParamsHelper = function ajaxParamsHelper(params) {
                return _select2Helpers.select2AjaxParamsHelper(params, ajaxParams);
              };
            }
            defaultOptions.ajax = {
              url: _utils__WEBPACK_IMPORTED_MODULE_4__["default"].getFunctionByName(data.amsSelect2AjaxUrl || data.amsAjaxUrl) || data.amsSelect2AjaxUrl || data.amsAjaxUrl,
              data: ajaxParamsHelper || _utils__WEBPACK_IMPORTED_MODULE_4__["default"].getFunctionByName(data.amsSelect2AjaxData || data.amsAjaxData) || data.amsSelect2AjaxData || data.amsAjaxData,
              processResults: _utils__WEBPACK_IMPORTED_MODULE_4__["default"].getFunctionByName(data.amsSelect2AjaxProcessResults || data.amsAjaxProcessResults) || data.amsSelect2AjaxProcessResults || data.amsAjaxProcessResults,
              transport: _utils__WEBPACK_IMPORTED_MODULE_4__["default"].getFunctionByName(data.amsSelect2AjaxTransport || data.amsAjaxTransport) || data.amsSelect2AjaxTransport || data.amsAjaxTransport
            };
            defaultOptions.minimumInputLength = data.amsSelect2MinimumInputLength || data.amsMinimumInputLength || data.minimumInputLength || 1;
          }
          var settings = $.extend({}, defaultOptions, data.amsSelect2Options || data.amsOptions || data.options),
            veto = {
              veto: false
            };
          select.trigger('before-init.ams.select2', [select, settings, veto]);
          if (veto.veto) {
            return;
          }
          var plugin = select.select2(settings);
          select.trigger('after-init.ams.select2', [select, plugin]);
        });
      });
    }

    //
    // Initialize datetime widgets
    //

    var dates = $('.datetime');
    if (dates.length > 0) {
      __webpack_require__.e(/*! import() */ "vendors-node_modules_tempusdominus-bootstrap-4_build_js_tempusdominus-bootstrap-4_js").then(__webpack_require__.t.bind(__webpack_require__, /*! tempusdominus-bootstrap-4 */ "./node_modules/tempusdominus-bootstrap-4/build/js/tempusdominus-bootstrap-4.js", 23)).then(function () {
        dates.each(function (idx, elt) {
          var input = $(elt),
            data = input.data(),
            defaultOptions = {
              locale: data.amsDatetimeLanguage || data.amsLanguage || lang,
              icons: {
                time: 'far fa-clock',
                date: 'far fa-calendar',
                up: 'fas fa-arrow-up',
                down: 'fas fa-arrow-down',
                previous: 'fas fa-chevron-left',
                next: 'fas fa-chevron-right',
                today: 'far fa-calendar-check-o',
                clear: 'far fa-trash',
                close: 'far fa-times'
              },
              date: input.val() || elt.defaultValue,
              format: data.amsDatetimeFormat || data.amsFormat
            },
            settings = $.extend({}, defaultOptions, data.datetimeOptions || data.options),
            veto = {
              veto: false
            };
          input.trigger('before-init.ams.datetime', [input, settings, veto]);
          if (veto.veto) {
            return;
          }
          input.datetimepicker(settings);
          var plugin = input.data('datetimepicker');
          if (data.amsDatetimeIsoTarget || data.amsIsoTarget) {
            input.on('change.datetimepicker', function (evt) {
              var source = $(evt.currentTarget),
                data = source.data(),
                target = $(data.amsDatetimeIsoTarget || data.amsIsoTarget);
              target.val(evt.date ? evt.date.toISOString(true) : null);
            });
          }
          input.trigger('after-init.ams.datetime', [input, plugin]);
        });
      });
    }

    //
    // Initialize forms
    //

    var defaultOptions = {
      submitHandler: PyAMS_form.submitHandler,
      messages: {}
    };
    var getFormOptions = function getFormOptions(form, options) {
      $('[data-ams-validate-messages]', form).each(function (idx, elt) {
        options.messages[$(elt).attr('name')] = $(elt).data('ams-validate-messages');
        options.errorClass = 'error d-block';
        options.errorPlacement = function (error, element) {
          element.parents('div:first').append(error);
        };
      });
      return options;
    };
    var validateForms = function validateForms() {
      $(forms).each(function (idx, form) {
        var options = $.extend({}, defaultOptions);
        $(form).validate(getFormOptions(form, options));
      });
    };
    if (lang === 'fr') {
      __webpack_require__.e(/*! import() */ "node_modules_jquery-validation_dist_localization_messages_fr_js").then(__webpack_require__.t.bind(__webpack_require__, /*! jquery-validation/dist/localization/messages_fr */ "./node_modules/jquery-validation/dist/localization/messages_fr.js", 23)).then(function () {
        validateForms();
      });
    } else {
      validateForms();
    }
  },
  /**
   * Show message extracted from JSON response
   */
  showMessage: function showMessage(errors, form) {
    var createMessages = function createMessages() {
      var header = errors.header || _utils__WEBPACK_IMPORTED_MODULE_4__["default"].i18n.SUCCESS,
        props = {
          status: 'success',
          header: header,
          message: errors.message || null
        };
      $(ERROR_TEMPLATE.render(props)).prependTo(form);
    };
    clearMessages(form);
    clearAlerts(form);
    createMessages();
    $.scrollTo('.alert', {
      offset: -15
    });
  },
  /**
   * Show errors extracted from JSON response
   */
  showErrors: function showErrors(errors, form) {
    var setInvalid = function setInvalid(form, input, message) {
      if (typeof input === 'string') {
        input = $("[name=\"".concat(input, "\"]"), form);
      }
      if (input.exists()) {
        var widget = input.closest('.form-widget');
        $('.invalid-feedback', widget).remove();
        $('<span>').text(message).addClass('is-invalid invalid-feedback').appendTo(widget);
        input.removeClass('valid').addClass('is-invalid');
      }
    };
    var createAlerts = function createAlerts() {
      var messages = [];
      var _iterator = _createForOfIteratorHelper(errors.messages || []),
        _step;
      try {
        for (_iterator.s(); !(_step = _iterator.n()).done;) {
          var message = _step.value;
          if (typeof message === 'string') {
            messages.push({
              header: null,
              message: message
            });
          } else {
            messages.push(message);
          }
        }
      } catch (err) {
        _iterator.e(err);
      } finally {
        _iterator.f();
      }
      var _iterator2 = _createForOfIteratorHelper(errors.widgets || []),
        _step2;
      try {
        for (_iterator2.s(); !(_step2 = _iterator2.n()).done;) {
          var widget = _step2.value;
          messages.push({
            header: widget.label,
            message: widget.message
          });
        }
      } catch (err) {
        _iterator2.e(err);
      } finally {
        _iterator2.f();
      }
      var header = errors.header || (messages.length > 1 ? _utils__WEBPACK_IMPORTED_MODULE_4__["default"].i18n.ERRORS_OCCURRED : _utils__WEBPACK_IMPORTED_MODULE_4__["default"].i18n.ERROR_OCCURRED),
        props = {
          status: 'danger',
          header: header,
          message: errors.error || null,
          messages: messages
        };
      $(ERROR_TEMPLATE.render(props)).prependTo(form);
      // update status of invalid widgets
      var _iterator3 = _createForOfIteratorHelper(errors.widgets || []),
        _step3;
      try {
        for (_iterator3.s(); !(_step3 = _iterator3.n()).done;) {
          var _widget = _step3.value;
          var input = void 0;
          if (_widget.id) {
            input = $("#".concat(_widget.id), form);
          } else {
            input = $("[name=\"".concat(_widget.name, "\"]"), form);
          }
          if (input.exists()) {
            setInvalid(form, input, _widget.message);
          }
          // open parent fieldsets switchers
          var fieldsets = input.parents('fieldset.switched');
          fieldsets.each(function (idx, elt) {
            $('legend.switcher', elt).click();
          });
          // open parent tab panels
          var panels = input.parents('.tab-pane');
          panels.each(function (idx, elt) {
            var panel = $(elt),
              tabs = panel.parents('.tab-content').siblings('.nav-tabs');
            $("li:nth-child(".concat(panel.index() + 1, ")"), tabs).addClass('is-invalid');
            $('li.is-invalid:first a', tabs).click();
          });
        }
      } catch (err) {
        _iterator3.e(err);
      } finally {
        _iterator3.f();
      }
    };
    clearMessages(form);
    clearAlerts(form);
    createAlerts();
    $.scrollTo('.alert', {
      offset: -15
    });
  },
  submitHandler: function submitHandler(form) {
    var doSubmit = function doSubmit(form) {
      // record submit button as hidden input
      var button = $('button[type="submit"]', form),
        name = button.attr('name'),
        input = $('input[name="' + name + '"]', form);
      if (input.length === 0) {
        $('<input />').attr('type', 'hidden').attr('name', name).attr('value', button.attr('value')).appendTo(form);
      } else {
        input.val(button.attr('value'));
      }
      // record CSRF token as hidden input
      var csrf_param = $('meta[name=csrf-param]').attr('content'),
        csrf_token = $('meta[name=csrf-token]').attr('content'),
        csrf_input = $("input[name=\"".concat(csrf_param, "\"]"), form);
      if (csrf_input.length === 0) {
        $('<input />').attr('type', 'hidden').attr('name', csrf_param).attr('value', csrf_token).appendTo(form);
      } else {
        csrf_input.val(csrf_token);
      }
      // submit form!
      $(form).ajaxSubmit({
        // success handler
        success: function success(result, status, response, form) {
          var contentType = response.getResponseHeader('content-type');
          if (contentType === 'application/json') {
            var _status = result.status;
            switch (_status) {
              case 'success':
                PyAMS_form.showMessage(result, form);
                break;
              case 'error':
                PyAMS_form.showErrors(result, form);
                break;
              case 'reload':
              case 'redirect':
                var location = result.location;
                if (window.location.href === location) {
                  window.location.reload();
                } else {
                  window.location.replace(location);
                }
                break;
              default:
                if (window.console) {
                  window.console.warn("Unhandled JSON status: ".concat(_status));
                  window.console.warn(" > ".concat(result));
                }
            }
          } else if (contentType === 'text/html') {
            var target = $('#main');
            target.html(result);
          }
        },
        // error handler
        error: function error(response, status, message, form) {
          clearAlerts(form);
          var header = _utils__WEBPACK_IMPORTED_MODULE_4__["default"].i18n.ERROR_OCCURRED,
            props = {
              status: 'danger',
              header: header,
              message: message
            };
          $(ERROR_TEMPLATE.render(props)).prependTo(form);
          $.scrollTo('.alert', {
            offset: -15
          });
        }
      });
    };
    if (window.grecaptcha) {
      // check if recaptcha was loaded
      var captcha_key = $(form).data('ams-form-captcha-key');
      grecaptcha.execute(captcha_key, {
        action: 'form_submit'
      }).then(function (token) {
        $('.state-error', form).removeClass('state-error');
        $('input[name="g-recaptcha-response"]', form).val(token);
        doSubmit(form);
      });
    } else {
      doSubmit(form);
    }
  }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (PyAMS_form);

/***/ })

}]);
//# sourceMappingURL=pkg_js__form_js.js.map