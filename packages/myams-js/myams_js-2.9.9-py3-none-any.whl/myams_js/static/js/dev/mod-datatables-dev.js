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
    global.modDatatables = mod.exports;
  }
})(typeof globalThis !== "undefined" ? globalThis : typeof self !== "undefined" ? self : this, function (_exports) {
  "use strict";

  Object.defineProperty(_exports, "__esModule", {
    value: true
  });
  _exports._mod = void 0;

  /**
   * MyAMS
   */
  if (!window.jQuery) {
    window.$ = window.jQuery = require('jquery');
  }

  var _mod = {};
  /**
   * Global module initialization
   */

  _exports._mod = _mod;

  if (window.MyAMS) {
    if (MyAMS.env.bundle) {
      MyAMS.config.modules.push('_mod');
    } else {
      MyAMS._mod = _mod;
      console.debug("MyAMS: _mod module loaded...");
    }
  }
});
//# sourceMappingURL=mod-datatables-dev.js.map
