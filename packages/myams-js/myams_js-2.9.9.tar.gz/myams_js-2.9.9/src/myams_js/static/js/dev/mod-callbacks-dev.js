(function (global, factory) {
  if (typeof define === "function" && define.amd) {
    define(["exports"], factory);
  } else if (typeof exports !== "undefined") {
    factory(exports);
  } else {
    var mod = {
      exports: {}
    };
    factory(mod.exports);
    global.modCallbacks = mod.exports;
  }
})(typeof globalThis !== "undefined" ? globalThis : typeof self !== "undefined" ? self : this, function (_exports) {
  "use strict";

  Object.defineProperty(_exports, "__esModule", {
    value: true
  });
  _exports.callbacks = void 0;
  /* global MyAMS */
  /**
   * MyAMS callbacks management
   */

  const $ = MyAMS.$;
  let _initialized = false;
  const callbacks = _exports.callbacks = {
    init: () => {
      if (_initialized) {
        return;
      }
      _initialized = true;
    },
    initElement: element => {
      return new Promise((resolve, reject) => {
        const deferred = [];
        $('[data-ams-callback]', element).each((idx, elt) => {
          const data = $(elt).data();
          let callbacks = data.amsCallback;
          if (typeof callbacks === 'string') {
            try {
              callbacks = JSON.parse(data.amsCallback);
            } catch (e) {
              callbacks = data.amsCallback.split(/[\s,;]+/);
            }
          }
          if (!$.isArray(callbacks)) {
            callbacks = [callbacks];
          }
          for (const callback of callbacks) {
            let callname, callable, source, options;
            if (typeof callback === 'string') {
              callname = callback;
              callable = MyAMS.core.getFunctionByName(callname);
              source = data.amsCallbackOptions;
              options = data.amsCallbackOptions;
              if (typeof options === 'string') {
                options = options.unserialize();
              }
            } else {
              // JSON object
              callname = callback.callback;
              callable = MyAMS.core.getFunctionByName(callname);
              source = callback.source;
              options = callback.options;
            }
            if (typeof callable === 'undefined') {
              if (source) {
                deferred.push(MyAMS.core.getScript(source).then(() => {
                  callable = MyAMS.core.getFunctionByName(callname);
                  if (typeof callable === 'undefined') {
                    console.warn(`Missing callback ${callname}!`);
                  } else {
                    callable.call(document, elt, options);
                  }
                }));
              } else {
                console.warn(`Missing source for undefined callback ${callback}!`);
              }
            } else {
              deferred.push(Promise.resolve(callable.call(document, elt, options)));
            }
          }
        });
        $.when.apply($, deferred).then(resolve, reject);
      });
    }
  };

  /**
   * Global module initialization
   */
  if (window.MyAMS) {
    if (MyAMS.env.bundle) {
      MyAMS.config.modules.push('callbacks');
    } else {
      MyAMS.callbacks = callbacks;
      console.debug("MyAMS: callbacks module loaded...");
    }
  }
});
//# sourceMappingURL=mod-callbacks-dev.js.map
