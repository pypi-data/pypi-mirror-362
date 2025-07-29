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
    global.modJsonrpc = mod.exports;
  }
})(typeof globalThis !== "undefined" ? globalThis : typeof self !== "undefined" ? self : this, function (_exports) {
  "use strict";

  Object.defineProperty(_exports, "__esModule", {
    value: true
  });
  _exports.jsonrpc = void 0;
  /* global MyAMS */
  /**
   * MyAMS JSON-RPC protocol support
   */

  const $ = MyAMS.$;
  const jsonrpc = _exports.jsonrpc = {};

  /**
   * Global module initialization
   */
  if (window.MyAMS) {
    if (MyAMS.env.bundle) {
      MyAMS.config.modules.push('jsonrpc');
    } else {
      MyAMS.jsonrpc = jsonrpc;
      console.debug("MyAMS: jsonrpc module loaded...");
    }
  }
});
//# sourceMappingURL=mod-jsonrpc-dev.js.map
