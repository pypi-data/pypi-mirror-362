function _typeof(obj) { "@babel/helpers - typeof"; if (typeof Symbol === "function" && typeof Symbol.iterator === "symbol") { _typeof = function _typeof(obj) { return typeof obj; }; } else { _typeof = function _typeof(obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; }; } return _typeof(obj); }

(function (global, factory) {
  if (typeof define === "function" && define.amd) {
    define(["exports", "./ext-base"], factory);
  } else if (typeof exports !== "undefined") {
    factory(exports, require("./ext-base"));
  } else {
    var mod = {
      exports: {}
    };
    factory(mod.exports, global.extBase);
    global.modDialog = mod.exports;
  }
})(typeof globalThis !== "undefined" ? globalThis : typeof self !== "undefined" ? self : this, function (_exports, _extBase) {
  "use strict";

  Object.defineProperty(_exports, "__esModule", {
    value: true
  });
  _exports.dialog = void 0;
  _extBase = _interopRequireWildcard(_extBase);

  function _getRequireWildcardCache() { if (typeof WeakMap !== "function") return null; var cache = new WeakMap(); _getRequireWildcardCache = function _getRequireWildcardCache() { return cache; }; return cache; }

  function _interopRequireWildcard(obj) { if (obj && obj.__esModule) { return obj; } if (obj === null || _typeof(obj) !== "object" && typeof obj !== "function") { return { "default": obj }; } var cache = _getRequireWildcardCache(); if (cache && cache.has(obj)) { return cache.get(obj); } var newObj = {}; var hasPropertyDescriptor = Object.defineProperty && Object.getOwnPropertyDescriptor; for (var key in obj) { if (Object.prototype.hasOwnProperty.call(obj, key)) { var desc = hasPropertyDescriptor ? Object.getOwnPropertyDescriptor(obj, key) : null; if (desc && (desc.get || desc.set)) { Object.defineProperty(newObj, key, desc); } else { newObj[key] = obj[key]; } } } newObj["default"] = obj; if (cache) { cache.set(obj, newObj); } return newObj; }

  /**
   * MyAMS modal dialogs support
   */
  if (!window.jQuery) {
    window.$ = window.jQuery = require('jquery');
  }

  var shownCallbacks = [],
      hideCallbacks = [];
  var dialog = {
    registerShownCallback: function registerShownCallback(callback, element) {},
    registerHideCallback: function registerHideCallback(callback, element) {},
    open: function open(source, options, callbacks) {
      var sourceData = {},
          url = source;

      if (typeof source !== 'string') {
        sourceData = source.data();
        url = source.attr('href') || sourceData.amsUrl;
        var urlGetter = (0, _extBase.getFunctionByName)(url);

        if (typeof urlGetter === 'function') {
          url = urlGetter.call(source);
        }
      }

      if (!url) {
        return;
      }

      if (url.startsWith('#')) {
        // Open inner modal
        $(url).modal('show');
      } else {
        return $.ajax({
          type: 'get',
          url: url,
          cache: sourceData.amsAllowCache === undefined ? false : sourceData.amsAllowCache,
          data: options
        }).done(function (data, status, request) {
          _extBase["default"].require(['ajax'], function () {
            var response = _extBase["default"].ajax.getResponse(request),
                dataType = response.contentType,
                result = response.data;

            switch (dataType) {
              case 'json':
                _extBase["default"].ajax.handleJSON(result, $($(source).data('ams-json-target') || '#content'));

                break;

              case 'script':
              case 'xml':
                break;

              case 'html':
              case 'text':
              default:
                var content = $(result),
                    modal = $('.modal-dialog', content.wrap('<div></div>').parent()),
                    modalData = modal.data() || {},
                    modalOptions = {
                  backdrop: modalData.backdrop === undefined ? 'static' : modalData.backdrop
                };
                var settings = $.extend({}, modalOptions, modalData.amsModalOptions);
                settings = (0, _extBase.executeFunctionByName)(modalData.amsModalinitCallback, modal, settings) || settings;

                if (callbacks) {
                  if (callbacks.shown) {
                    config.registerShownCallback(callbacks.shown, content);
                  }

                  if (callbacks.hide) {
                    config.registerHideCallback(callbacks.hide, content);
                  }
                }

                $('<div>').addClass('modal fade').data('dynamic', true).append(content).on('shown.bs.modal', dialog.shown).on('hidden.bs.modal', dialog.hidden).modal(settings);

                if (_extBase["default"].stats && !(sourceData.amsLogEvent === false || modalData.amsLogEvent === false)) {
                  _extBase["default"].stats.logPageview(url);
                }

            }
          });
        });
      }
    },

    /**
     * Dynamic modal 'shown' callback
     * This callback is used to initialize modal's viewport size
     *
     * @param evt: source event
     */
    shown: function shown(evt) {
      var modal = evt.target;
      (0, _extBase.initContent)(modal);
    },

    /**
     * Close modal associated with given element
     *
     * @param element: the element contained into closed modal
     */
    close: function close(element) {
      if (typeof element === 'string') {
        element = $(element);
      }

      var modal = element.parents('.modal').data('bs.modal');

      if (modal) {
        modal.hide();
      }
    },

    /**
     * Dynamic modal 'hidden' callback
     * This callback is used to remove dynamic modals
     *
     * @param evt: source event
     */
    hidden: function hidden(evt) {
      var modal = $(evt.target);
      (0, _extBase.clearContent)(modal);

      if (modal.data('dynamic') === true) {
        modal.remove();
      }
    }
  };
  /**
   * Handle modal events to allow
   */

  _exports.dialog = dialog;
  var zIndexModal = 1100;
  $(document).on('shown.bs.modal', '.modal', function (e) {
    var visibleModalsCount = $('.modal:visible').length,
        zIndex = zIndexModal + 100 * visibleModalsCount;
    $(e.target).css('z-index', zIndex);
    setTimeout(function () {
      $('.modal-backdrop').not('.modal-stack').first().css('z-index', zIndex - 10).addClass('modal-stack');
    }, 0);
  });
  $(document).on('hidden.bs.modal', '.modal', function () {
    if ($('.modal:visible').length) {
      $.fn.modal.Constructor.prototype._checkScrollbar();

      $.fn.modal.Constructor.prototype._setScrollbar();

      $('body').addClass('modal-open');
    }
  });
  /**
   * Global module initialization
   */

  if (window.MyAMS) {
    if (_extBase["default"].env.bundle) {
      _extBase["default"].config.modules.push('dialog');
    } else {
      _extBase["default"].dialog = dialog;
      console.debug("MyAMS: dialog module loaded...");
    }
  }
});
//# sourceMappingURL=mod-dialog-dev.js.map
