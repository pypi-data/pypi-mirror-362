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
    global.modXmlrpc = mod.exports;
  }
})(typeof globalThis !== "undefined" ? globalThis : typeof self !== "undefined" ? self : this, function (_exports) {
  "use strict";

  Object.defineProperty(_exports, "__esModule", {
    value: true
  });
  _exports.xmlrpc = void 0;
  /* global MyAMS */
  /**
   * MyAMS XML-RPC protocol support
   */

  const $ = MyAMS.$;
  const xmlrpc = _exports.xmlrpc = {};

  /**
   * Global module initialization
   */
  if (window.MyAMS) {
    if (MyAMS.env.bundle) {
      MyAMS.config.modules.push('xmlrpc');
    } else {
      MyAMS.xmlrpc = xmlrpc;
      console.debug("MyAMS: xmlrpc module loaded...");
    }
  }
});
//# sourceMappingURL=mod-xmlrpc-dev.js.map
