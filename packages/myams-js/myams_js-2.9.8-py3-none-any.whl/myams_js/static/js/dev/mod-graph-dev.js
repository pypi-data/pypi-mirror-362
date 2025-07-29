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
    global.modGraph = mod.exports;
  }
})(typeof globalThis !== "undefined" ? globalThis : typeof self !== "undefined" ? self : this, function (_exports) {
  "use strict";

  Object.defineProperty(_exports, "__esModule", {
    value: true
  });
  _exports.graph = void 0;
  /* global MyAMS */
  /**
   * MyAMS graphs management
   */

  const $ = MyAMS.$;
  const graph = _exports.graph = {};

  /**
   * Global module initialization
   */
  if (window.MyAMS) {
    if (MyAMS.env.bundle) {
      MyAMS.config.modules.push('graph');
    } else {
      MyAMS.graph = graph;
      console.debug("MyAMS: graph module loaded...");
    }
  }
});
//# sourceMappingURL=mod-graph-dev.js.map
