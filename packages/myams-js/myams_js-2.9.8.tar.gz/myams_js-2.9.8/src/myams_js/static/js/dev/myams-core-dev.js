/******/ (function() { // webpackBootstrap
/******/ 	"use strict";
/******/ 	var __webpack_modules__ = ({

/***/ "./pkg/js/ext-base.js":
/*!****************************!*\
  !*** ./pkg/js/ext-base.js ***!
  \****************************/
/***/ (function(__unused_webpack_module, __webpack_exports__, __webpack_require__) {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   clearContent: function() { return /* binding */ clearContent; },
/* harmony export */   executeFunctionByName: function() { return /* binding */ executeFunctionByName; },
/* harmony export */   generateId: function() { return /* binding */ generateId; },
/* harmony export */   generateUUID: function() { return /* binding */ generateUUID; },
/* harmony export */   getCSS: function() { return /* binding */ getCSS; },
/* harmony export */   getFunctionByName: function() { return /* binding */ getFunctionByName; },
/* harmony export */   getModules: function() { return /* binding */ getModules; },
/* harmony export */   getObject: function() { return /* binding */ getObject; },
/* harmony export */   getQueryVar: function() { return /* binding */ getQueryVar; },
/* harmony export */   getScript: function() { return /* binding */ getScript; },
/* harmony export */   getSource: function() { return /* binding */ getSource; },
/* harmony export */   init: function() { return /* binding */ init; },
/* harmony export */   initContent: function() { return /* binding */ initContent; },
/* harmony export */   initData: function() { return /* binding */ initData; },
/* harmony export */   initPage: function() { return /* binding */ initPage; },
/* harmony export */   switchIcon: function() { return /* binding */ switchIcon; }
/* harmony export */ });
/* harmony import */ var _ext_registry__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./ext-registry */ "./pkg/js/ext-registry.js");
/* global $, FontAwesome */
/**
 * MyAMS base features
 */

if (!window.jQuery) {
  window.$ = window.jQuery = __webpack_require__(/*! jquery */ "jquery");
}


/**
 * Init JQuery extensions
 */
function init($) {
  /**
   * String prototype extensions
   */
  $.extend(String.prototype, {
    /**
     * Replace dashed names with camelCase variation
     */
    camelCase: function () {
      if (!this) {
        return this;
      }
      return this.replace(/-(.)/g, (dash, rest) => {
        return rest.toUpperCase();
      });
    },
    /**
     * Replace camelCase string with dashed name
     */
    deCase: function () {
      if (!this) {
        return this;
      }
      return this.replace(/[A-Z]/g, cap => {
        return `-${cap.toLowerCase()}`;
      });
    },
    /**
     * Convert first letter only to lowercase
     */
    initLowerCase: function () {
      if (!this) {
        return this;
      }
      return this.charAt(0).toLowerCase() + this.slice(1);
    },
    /**
     * Convert URL params to object
     */
    unserialize: function () {
      if (!this) {
        return this;
      }
      const str = decodeURIComponent(this),
        chunks = str.split('&'),
        obj = {};
      for (const chunk of chunks) {
        const [key, val] = chunk.split('=', 2);
        obj[key] = val;
      }
      return obj;
    }
  });

  /**
   * Array class prototype extension
   */
  $.extend(Array.prototype, {
    /**
     * Extend an array with another one
     */
    extendWith: function (source) {
      for (const element of source) {
        this.push(element);
      }
    }
  });

  /**
   * Global JQuery object extensions
   */
  $.extend($, {
    /**
     * Extend source object with given extensions, but only for properties matching
     * given prefix.
     *
     * @param source: source object, which will be updated in-place
     * @param prefix: property names prefix selector
     * @param getter: optional getter used to extract final value
     * @param extensions: list of extensions object
     * @returns {*}: modified source object
     */
    extendPrefix: function (source, prefix, getter) {
      for (var _len = arguments.length, extensions = new Array(_len > 3 ? _len - 3 : 0), _key = 3; _key < _len; _key++) {
        extensions[_key - 3] = arguments[_key];
      }
      for (const extension of extensions) {
        for (const [key, value] of Object.entries(extension)) {
          if (key.startsWith(prefix)) {
            source[key.substring(prefix.length).initLowerCase()] = getter === null ? value : getter(value);
          }
        }
      }
      return source;
    },
    /**
     * Extend source with given extensions, but only for existing attributes
     *
     * @param source: source object, which will be updated in-place
     * @param getter: optional getter used to extract final value
     * @param extensions: list of extensions object
     * @returns {*}: modified source object
     */
    extendOnly: function (source, getter) {
      for (var _len2 = arguments.length, extensions = new Array(_len2 > 2 ? _len2 - 2 : 0), _key2 = 2; _key2 < _len2; _key2++) {
        extensions[_key2 - 2] = arguments[_key2];
      }
      for (const extension of extensions) {
        for (const [key, value] of Object.entries(extension)) {
          if (Object.prototype.hasOwnProperty.call(source, key)) {
            source[key] = getter === null ? value : getter(value);
          }
        }
      }
      return source;
    }
  });

  /**
   * New JQuery functions
   */
  $.fn.extend({
    /**
     * Check if current object is empty or not
     */
    exists: function () {
      return $(this).length > 0;
    },
    /**
     * Get object if it supports given CSS class,
     * otherwise look for parents
     */
    objectOrParentWithClass: function (klass) {
      if (this.hasClass(klass)) {
        return this;
      }
      return this.parents(`.${klass}`);
    },
    /**
     * Build an array of attributes of the given selection
     */
    listattr: function (attr) {
      const result = [];
      this.each((index, element) => {
        result.push($(element).attr(attr));
      });
      return result;
    },
    /**
     * CSS style function - get or set object style attribute
     * Code from Aram Kocharyan on stackoverflow.com
     */
    style: function (styleName, value, priority) {
      let result = this;
      this.each((idx, node) => {
        // Ensure we have a DOM node
        if (typeof node === 'undefined') {
          return false;
        }
        // CSSStyleDeclaration
        const style = node.style;
        // Getter/Setter
        if (typeof styleName !== 'undefined') {
          if (typeof value !== 'undefined') {
            // Set style property
            priority = typeof priority !== 'undefined' ? priority : '';
            style.setProperty(styleName, value, priority);
          } else {
            // Get style property
            result = style.getPropertyValue(styleName);
            return false;
          }
        } else {
          // Get CSSStyleDeclaration
          result = style;
          return false;
        }
      });
      return result;
    },
    /**
     * Remove CSS classes starting with a given prefix
     */
    removeClassPrefix: function (prefix) {
      this.each(function (i, it) {
        const classes = it.className.split(/\s+/).map(item => {
          return item.startsWith(prefix) ? "" : item;
        });
        it.className = $.trim(classes.join(" "));
      });
      return this;
    }
  });

  /**
   * JQuery 'hasvalue' function expression
   * Filter inputs containing value:
   *
   *     $('span:hasvalue("value")')
   */
  $.expr[":"].hasvalue = function (obj, index, meta /*, stack*/) {
    return $(obj).val() !== "";
  };

  /**
   * JQuery 'econtains' function expression
   * Case insensitive contains expression:
   *
   *     $('span:econtains("text")')
   */
  $.expr[":"].econtains = function (obj, index, meta /*, stack*/) {
    return (obj.textContent || obj.innerText || $(obj).text() || "").toLowerCase() === meta[3].toLowerCase();
  };

  /**
   * JQuery 'withtext' expression
   * Case sensitive exact search expression.
   * For example:
   *
   *    $('span:withtext("text")')
   */
  $.expr[":"].withtext = function (obj, index, meta /*, stack*/) {
    return (obj.textContent || obj.innerText || $(obj).text() || "") === meta[3];
  };

  /**
   * JQuery filter on parents class
   * This filter is often combined with ":not()" to select DOM objects which don't have
   * parents of a given class.
   * For example:
   *
   *   $('.hint:not(:parents(.nohints))', element);
   *
   * will select all elements with ".hint" class which don't have a parent with '.nohints' class.
   */
  $.expr[':'].parents = function (obj, index, meta /*, stack*/) {
    return $(obj).parents(meta[3]).length > 0;
  };
  $(document).ready(() => {
    const html = $('html');
    html.removeClass('no-js').addClass('js');
    MyAMS.core.executeFunctionByName(html.data('ams-init-page') || MyAMS.config.initPage);
  });
}

/**
 * Get list of modules names required by given element
 *
 * @param element: parent element
 * @returns {*[]}
 */
function getModules(element) {
  let modules = [];
  const mods = element.data('ams-modules');
  if (typeof mods === 'string') {
    modules = modules.concat(mods.trim().split(/[\s,;]+/));
  } else if (mods) {
    for (const [name, props] of Object.entries(mods)) {
      if (modules.find(elt => elt === name || elt[name]) === undefined) {
        const entry = {};
        entry[name] = props;
        modules.push(entry);
      }
    }
  }
  $('[data-ams-modules]', element).each((idx, elt) => {
    const mods = $(elt).data('ams-modules');
    if (typeof mods === 'string') {
      modules = modules.concat(mods.trim().split(/[\s,;]+/));
    } else if (mods) {
      for (const [name, props] of Object.entries(mods)) {
        if (modules.find(elt => elt === name || elt[name]) === undefined) {
          const entry = {};
          entry[name] = props;
          modules.push(entry);
        }
      }
    }
  });
  return [...new Set(modules)];
}

/**
 * Main page initialization
 */
function initPage() {
  return MyAMS.require('i18n').then(() => {
    MyAMS.dom = getDOM();
    MyAMS.theme = getTheme();
    executeFunctionByName(MyAMS.config.initData, window, MyAMS.dom.root);
    const modules = getModules(MyAMS.dom.root);
    MyAMS.require(...modules).then(() => {
      for (const moduleName of MyAMS.config.modules) {
        executeFunctionByName(`MyAMS.${moduleName}.init`);
      }
      executeFunctionByName(MyAMS.dom.page.data('ams-init-content') || MyAMS.config.initContent);
    });
  });
}

/**
 * Data attributes initializer
 *
 * This function converts a single "data-ams-data" attribute into a set of several "data-*"
 * attributes.
 * This can be used into HTML templates engines which don't allow creating dynamic attributes
 * easily.
 *
 * @param element: parent element
 */
function initData(element) {
  $('[data-ams-data]', element).each((idx, elt) => {
    const $elt = $(elt),
      data = $elt.data('ams-data');
    if (data) {
      for (const name in data) {
        if (!Object.prototype.hasOwnProperty.call(data, name)) {
          continue;
        }
        let elementData = data[name];
        if (typeof elementData !== 'string') {
          elementData = JSON.stringify(elementData);
        }
        $elt.attr(`data-${name}`, elementData);
      }
    }
    $elt.removeAttr('data-ams-data');
  });
}

/**
 * Main content initialization; this function will initialize all plug-ins, callbacks and
 * events listeners in the selected element
 *
 * @param element: source element to initialize
 */
function initContent() {
  let element = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : null;
  if (element === null) {
    element = $('body');
  }
  element = $(element);
  function initElementModules() {
    for (const moduleName of MyAMS.config.modules) {
      executeFunctionByName(`MyAMS.${moduleName}.initElement`, document, element);
    }
  }
  return new Promise((resolve, reject) => {
    executeFunctionByName(MyAMS.config.initData, window, element);
    const modules = getModules(element);
    return MyAMS.require(...modules).then(() => {
      element.trigger('before-init.ams.content');
      if (MyAMS.config.useRegistry && !element.data('ams-disable-registry')) {
        MyAMS.registry.initElement(element).then(() => {
          initElementModules();
        }).then(() => {
          MyAMS.registry.run(element);
          element.trigger('after-init.ams.content');
        }).then(resolve);
      } else {
        initElementModules();
        resolve();
      }
    }, () => {
      reject("Missing MyAMS modules!");
    });
  });
}

/**
 * Container clearing function.
 *
 * This function is called before replacing an element contents with new DOM elements;
 * an 'ams.container.before-cleaning' event is triggered, with arguments which are the
 * container and a "veto" object containing a single boolean "veto" property; if any
 * handler attached to this event set the "veto" property to *true*,
 *
 * The function returns a Promise which is resolved with the opposite value of the "veto"
 * property.
 *
 * @param element: the parent element which may be cleaned
 * @returns {Promise<boolean>}
 */
function clearContent(element) {
  if (typeof element === 'string') {
    element = $(element);
  }
  return new Promise((resolve, reject) => {
    const veto = {
      veto: false
    };
    $(document).trigger('clear.ams.content', [veto, element]);
    if (!veto.veto) {
      MyAMS.require('events').then(() => {
        $(MyAMS.events.getHandlers(element, 'clear.ams.content')).each((idx, elt) => {
          $(elt).trigger('clear.ams.content', [veto]);
          if (veto.veto) {
            return false;
          }
        });
        if (!veto.veto) {
          $(MyAMS.events.getHandlers(element, 'cleared.ams.content')).each((idx, elt) => {
            $(elt).trigger('cleared.ams.content');
          });
          $(document).trigger('cleared.ams.content', [element]);
        }
        resolve(!veto.veto);
      }, () => {
        reject("Missing MyAMS.events module!");
      });
    } else {
      resolve(!veto.veto);
    }
  });
}

/**
 * Get an object given by name
 *
 * @param objectName: dotted name of the object
 * @param context: source context, or window if undefined
 * @returns {Object|undefined}
 */
function getObject(objectName, context) {
  if (!objectName) {
    return undefined;
  }
  if (typeof objectName !== 'string') {
    return objectName;
  }
  const namespaces = objectName.split('.');
  context = context === undefined || context === null ? window : context;
  for (const name of namespaces) {
    try {
      context = context[name];
    } catch (exc) {
      return undefined;
    }
  }
  return context;
}

/**
 * Get function object from name
 *
 * @param functionName: dotted name of the function
 * @param context: source context; window if undefined
 * @returns {function|undefined}
 */
function getFunctionByName(functionName, context) {
  if (functionName === null || typeof functionName === 'undefined') {
    return undefined;
  } else if (typeof functionName === 'function') {
    return functionName;
  } else if (typeof functionName !== 'string') {
    return undefined;
  }
  const namespaces = functionName.split("."),
    func = namespaces.pop();
  context = context === undefined || context === null ? window : context;
  for (const name of namespaces) {
    try {
      context = context[name];
    } catch (e) {
      return undefined;
    }
  }
  try {
    return context[func];
  } catch (e) {
    return undefined;
  }
}

/**
 * Execute a function, given by it's name
 *
 * @param functionName: dotted name of the function
 * @param context: parent context, or window if undefined
 * @param args...: optional function arguments
 * @returns {*}: result of the called function
 */
function executeFunctionByName(functionName, context /*, args */) {
  const func = getFunctionByName(functionName, window);
  if (typeof func === 'function') {
    const args = Array.prototype.slice.call(arguments, 2);
    return func.apply(context, args);
  }
}

/**
 * Get target URL matching given source
 *
 * Given URL can include variable names (with their namespace), given between braces,
 * as in {MyAMS.env.baseURL}
 */
function getSource(url) {
  return url.replace(/{[^{}]*}/g, match => {
    return getObject(match.substr(1, match.length - 2));
  });
}

/**
 * Dynamic script loader function
 *
 * @param url: script URL
 * @param options: a set of options to be added to AJAX call
 */
function getScript(url) {
  let options = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : {};
  return new Promise((resolve, reject) => {
    const defaults = {
      dataType: 'script',
      url: MyAMS.core.getSource(url),
      cache: !MyAMS.env.devmode,
      async: true
    };
    const settings = $.extend({}, defaults, options);
    $.ajax(settings).then(() => {
      resolve(url);
    }, (xhr, status, error) => {
      reject(error);
    });
  });
}

/**
 * Get CSS matching given URL
 *
 * @param url: CSS source URL
 * @param name: name of the given CSS
 */
function getCSS(url, name) {
  return new Promise((resolve /*, reject */) => {
    const head = $('HEAD');
    let style = $(`style[data-ams-id="${name}"]`, head);
    if (style.length === 0) {
      style = $('<style>').attr('data-ams-id', name).text(`@import "${getSource(url)}";`).appendTo(head);
      const styleInterval = setInterval(() => {
        try {
          // eslint-disable-next-line no-unused-vars
          const _check = style[0].sheet.cssRules; // Is only populated when file is loaded
          clearInterval(styleInterval);
          resolve(true);
        } catch (e) {
          // CSS is not loaded yet, just wait...
        }
      }, 10);
    } else {
      resolve(false);
    }
  });
}

/**
 * Extract parameter value from given query string
 *
 * @param src: source URL
 * @param varName: variable name
 * @returns {boolean|*}
 */
function getQueryVar(src, varName) {
  // Check src
  if (typeof src !== 'string' || src.indexOf('?') < 0) {
    return undefined;
  }
  if (!src.endsWith('&')) {
    src += '&';
  }
  // Dynamic replacement RegExp
  const regex = new RegExp(`.*?[&\\?]${varName}=(.*?)&.*`);
  // Apply RegExp to the query string
  const val = src.replace(regex, "$1");
  // If the string is the same, we didn't find a match - return null
  return val === src ? null : val;
}

/**
 * Generate a random ID
 */
function generateId() {
  function s4() {
    return Math.floor((1 + Math.random()) * 0x10000).toString(16).substring(1);
  }
  return s4() + s4() + s4() + s4();
}

/**
 * Generate a random unique UUID
 */
function generateUUID() {
  let d = new Date().getTime();
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
    const r = (d + Math.random() * 16) % 16 | 0;
    d = Math.floor(d / 16);
    return (c === 'x' ? r : r & 0x3 | 0x8).toString(16);
  });
}

/**
 * Switch a FontAwesome icon.
 * Use FontAwesome API to get image as SVG, if FontAwesome is loaded from Javascript and is using
 * SVG auto-replace, otherwise just switch CSS class.
 *
 * @param element: source element
 * @param fromClass: initial CSS class (without "fa-" prefix)
 * @param toClass: new CSS class (without "fa-" prefix)
 * @param prefix: icon prefix (defaults to "fa")
 */
function switchIcon(element, fromClass, toClass) {
  let prefix = arguments.length > 3 && arguments[3] !== undefined ? arguments[3] : 'fa';
  if (typeof element === 'string') {
    element = $(element);
  }
  if (MyAMS.config.useSVGIcons) {
    const iconDef = FontAwesome.findIconDefinition({
      iconName: toClass,
      prefix: prefix
    });
    if (iconDef) {
      element.html(FontAwesome.icon(iconDef).html);
    }
  } else {
    element.removeClass(`fa-${fromClass}`).addClass(`fa-${toClass}`);
  }
}

/**
 * MyAMS base environment getter
 *
 * @type {Object}
 *
 * Returns an object with the following attributes matching MyAMS environment:
 * - bundle: boolean; true if MyAMS is published using modules bundle
 * - devmode: boolean; true if MyAMS is published in development mode
 * - devext: string: extension used in development mode
 * - extext: string: extension used for external extensions
 * - theme: string: current MyAMS theme name
 * - baseURL: string: base MyAMS URL
 * }}
 */
function getEnv($) {
  const script = $('script[src*="/myams.js"], script[src*="/myams-dev.js"], ' + 'script[src*="/emerald.js"], script[src*="/emerald-dev.js"], ' + 'script[src*="/darkmode.js"], script[src*="/darkmode-dev.js"], ' + 'script[src*="/lightmode.js"], script[src*="/lightmode-dev.js"], ' + 'script[src*="/myams-core.js"], script[src*="/myams-core-dev.js"], ' + 'script[src*="/myams-mini.js"], script[src*="/myams-mini-dev.js"]'),
    src = script.attr('src'),
    devmode = src ? src.indexOf('-dev.js') >= 0 : true,
    // testing mode
    bundle = src ? src.indexOf('-core') < 0 : true; // MyAMS modules not included in 'core' package
  return {
    bundle: bundle,
    devmode: devmode,
    devext: devmode ? '-dev' : '',
    extext: devmode ? '' : '.min',
    baseURL: src ? src.substring(0, src.lastIndexOf('/') + 1) : '/'
  };
}

/**
 * MyAMS theme getter
 */
function getTheme() {
  let theme = MyAMS.theme;
  if (!theme) {
    const css = $('link[href*="/myams.css"], ' + 'link[href*="/emerald.css"], ' + 'link[href*="/darkmode.css"], ' + 'link[href*="/lightmode.css"]');
    theme = css.length > 0 ? /.*\/([a-z]+).css/.exec(css.attr('href'))[1] : 'unknown';
  }
  return theme;
}

/**
 * Get base DOM elements
 */
function getDOM() {
  return {
    page: $('html'),
    root: $('body'),
    nav: $('nav'),
    main: $('#main'),
    leftPanel: $('#left-panel'),
    shortcuts: $('#shortcuts')
  };
}

/**
 * MyAMS default configuration
 *
 * @type {Object}
 *
 * Returns an object matching current MyAMS configuration:
 * - modules: array of loaded extension modules
 * - ajaxNav: true if AJAX navigation is enabled
 * - enableFastclick: true is "smart-click" extension is to be activated on mobile devices
 * - menuSpeed: menu speed, in miliseconds
 * - initPage: dotted name of MyAMS global init function
 * - initContent: dotted name of MyAMS content init function
 * - alertContainerCLass: class of MyAMS alerts container
 * - safeMethods: HTTP methods which can be used without CSRF cookie verification
 * - csrfCookieName: CSRF cookie name
 * - csrfHeaderName: CSRF header name
 * - enableTooltips: global tooltips enable flag
 * - enableHtmlTooltips: allow HTML code in tooltips
 * - warnOnFormChange: flag to specify if form changes should be warned
 * - formChangeCallback: global form change callback
 * - isMobile: boolean, true if device is detected as mobile
 * - device: string: 'mobile' or 'desktop'
 */
const isMobile = /iphone|ipad|ipod|android|blackberry|mini|windows\sce|palm/i.test(navigator.userAgent.toLowerCase()),
  config = {
    modules: [],
    ajaxNav: true,
    enableFastclick: true,
    useSVGIcons: window.FontAwesome !== undefined && FontAwesome.config.autoReplaceSvg === 'nest',
    menuSpeed: 235,
    initPage: 'MyAMS.core.initPage',
    initData: 'MyAMS.core.initData',
    initContent: 'MyAMS.core.initContent',
    clearContent: 'MyAMS.core.clearContent',
    useRegistry: true,
    alertsContainerClass: 'toast-wrapper',
    safeMethods: ['GET', 'HEAD', 'OPTIONS', 'TRACE'],
    csrfCookieName: 'csrf_token',
    csrfHeaderName: 'X-CSRF-Token',
    enableTooltips: true,
    enableHtmlTooltips: true,
    warnOnFormChange: true,
    formChangeCallback: null,
    isMobile: isMobile,
    device: isMobile ? 'mobile' : 'desktop'
  },
  core = {
    getObject: getObject,
    getFunctionByName: getFunctionByName,
    executeFunctionByName: executeFunctionByName,
    getSource: getSource,
    getScript: getScript,
    getCSS: getCSS,
    getQueryVar: getQueryVar,
    generateId: generateId,
    generateUUID: generateUUID,
    switchIcon: switchIcon,
    initPage: initPage,
    initData: initData,
    initContent: initContent,
    clearContent: clearContent
  };
const MyAMS = {
  $: $,
  env: getEnv($),
  config: config,
  core: core,
  registry: _ext_registry__WEBPACK_IMPORTED_MODULE_0__.registry
};
window.MyAMS = MyAMS;
/* harmony default export */ __webpack_exports__["default"] = (MyAMS);

/***/ }),

/***/ "./pkg/js/ext-registry.js":
/*!********************************!*\
  !*** ./pkg/js/ext-registry.js ***!
  \********************************/
/***/ (function(__unused_webpack_module, __webpack_exports__, __webpack_require__) {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   registry: function() { return /* binding */ registry; }
/* harmony export */ });
/* global $, MyAMS */
/**
 * MyAMS dynamic plug-ins loading management
 */

/**
 * Plug-ins loading order
 *  - initialize registry
 *  - initialize DOM data attributes
 *  - register all plug-ins from given DOM element
 *  - load all plug-ins from given DOM element
 *  - get list of disabled plug-ins into given DOM element
 *  - call callbacks for all enabled plug-ins
 *  - call callbacks for enabled "async" plug-ins
 */

/**
 * Base plug-in class
 */
class Plugin {
  constructor(name) {
    let props = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : {};
    let loaded = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : false;
    // plug-in name
    this.name = name;
    // plug-in source URL
    this.src = props.src;
    // plug-in associated CSS
    this.css = props.css;
    // plug-in callbacks
    this.callbacks = [];
    if (props.callback) {
      this.callbacks.push({
        callback: props.callback,
        context: props.context || 'body'
      });
    }
    // async plug-ins are loaded simultaneously; sync ones are loaded and called after...
    this.async = props.async === undefined ? true : props.async;
    // loaded flag
    this.loaded = loaded;
  }

  /**
   * Load plug-in from remote script
   *
   * @returns {Promise<void>|*}
   */
  load() {
    return new Promise((resolve, reject) => {
      if (!this.loaded) {
        const deferred = [];
        if (this.src) {
          deferred.push(MyAMS.core.getScript(this.src));
        }
        if (this.css) {
          deferred.push(MyAMS.core.getCSS(this.css, `${this.name}_css`));
        }
        $.when.apply($, deferred).then(() => {
          this.loaded = true;
          resolve();
        }, reject);
      } else {
        resolve();
      }
    });
  }

  /**
   * Run plug-in
   *
   * @param element: plug-in execution context
   */
  run(element) {
    const results = [];
    for (const callback of this.callbacks) {
      if (typeof callback.callback === 'string') {
        console.debug(`Resolving callback ${callback.callback}`);
        callback.callback = MyAMS.core.getFunctionByName(callback.callback) || callback.callback;
      }
      results.push(callback.callback(element, callback.context));
    }
    return Promise.all(results);
  }
}

/**
 * Plug-ins registry class
 */
class PluginsRegistry {
  constructor() {
    this.plugins = new Map();
  }

  /**
   * Register new plug-in
   *
   * @param props: plugin function caller, or object containing plug-in properties
   * @param name: plug-in unique name
   */
  register(props, name) {
    // check arguments
    if (!name && Object.prototype.hasOwnProperty.call(props, 'name')) {
      name = props.name;
    }
    // check for already registered plug-in
    const plugins = this.plugins;
    if (plugins.has(name)) {
      if (window.console) {
        console.debug && console.debug(`Plug-in ${name} is already registered!`);
      }
      const plugin = plugins.get(name);
      let addContext = true;
      for (const callback of plugin.callbacks) {
        if (callback.callback === props.callback && callback.context === props.context) {
          addContext = false;
          break;
        }
      }
      if (addContext) {
        plugin.callbacks.push({
          callback: props.callback,
          context: props.context || 'body'
        });
      }
      return plugin;
    }
    // register new plug-in
    if (typeof props === 'string') {
      // callable name
      props = MyAMS.core.getFunctionByName(props);
    }
    if (typeof props === 'function') {
      // callable object
      plugins.set(name, new Plugin(name, {
        callback: props
      }, true));
    } else if (typeof props === 'object') {
      // plug-in properties object
      plugins.set(name, new Plugin(name, props, !(props.src || props.css)));
    }
    // check callback
    return plugins.get(name);
  }

  /**
   * Load plug-ins declared into DOM element
   *
   * @param element
   */
  load(element) {
    // scan element for new plug-ins
    const asyncPlugins = [],
      syncPlugins = [];
    $('[data-ams-plugins]', element).each((idx, elt) => {
      const source = $(elt),
        names = source.data('ams-plugins');
      let plugin, props;
      if (typeof names === 'string') {
        for (const name of names.split(/[\s,;]+/)) {
          const lowerName = name.toLowerCase();
          props = {
            src: source.data(`ams-plugin-${lowerName}-src`),
            css: source.data(`ams-plugin-${lowerName}-css`),
            callback: source.data(`ams-plugin-${lowerName}-callback`),
            context: source,
            async: source.data(`ams-plugin-${lowerName}-async`)
          };
          plugin = this.register(props, name);
          if (!plugin.loaded) {
            if (props.async === false) {
              syncPlugins.push(plugin.load());
            } else {
              asyncPlugins.push(plugin.load());
            }
          }
        }
      } else {
        // JSON plug-in declaration
        for (props of $.isArray(names) ? names : [names]) {
          $.extend(props, {
            context: source
          });
          plugin = this.register(props);
          if (!plugin.loaded) {
            if (plugin.async === false) {
              syncPlugins.push(plugin.load());
            } else {
              asyncPlugins.push(plugin.load());
            }
          }
        }
      }
    });
    // load plug-ins
    let result = $.when.apply($, asyncPlugins);
    // eslint-disable-next-line no-unused-vars
    for (const plugin of syncPlugins) {
      result = result.done(() => {});
    }
    return result;
  }

  /**
   * Run registered plug-ins on given element
   *
   * @param element: source element
   * @param names: array list of plug-ins to activate, or all registered plug-ins if null
   */
  run(element) {
    let names = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : null;
    // check for disabled plug-ins
    const disabled = new Set();
    $('[data-ams-plugins-disabled]', element).each((idx, elt) => {
      const names = $(elt).data('ams-plugins-disabled').split(/[\s,;]+/);
      for (const name of names) {
        disabled.add(name);
      }
    });
    const plugins = this.plugins;
    if (names) {
      // only run given plug-ins, EVEN DISABLED ONES
      for (const name of names) {
        if (plugins.has(name)) {
          plugins.get(name).run(element);
        }
      }
    } else {
      // run all plug-ins, except disabled ones
      for (const [name, plugin] of plugins.entries()) {
        if (disabled.has(name)) {
          continue;
        }
        plugin.run(element);
      }
    }
  }
}
const plugins = new PluginsRegistry();
const registry = {
  /**
   * Plug-ins registry
   */
  plugins: plugins,
  /**
   * Initialize plug-ins registry from DOM
   *
   * @param element: source element to initialize from
   */
  initElement: function () {
    let element = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : '#content';
    // populate data attributes
    MyAMS.core.executeFunctionByName(MyAMS.config.initData, window, element);
    // load plug-ins from given DOM element
    return plugins.load(element);
  },
  /**
   * Register a new plug-in through Javascript instead of HTML data attributes
   *
   * @param plugin: callable object, or object containing plug-in properties
   * @param name: plug-in name, used if @plugin is a function
   * @param callback: callback function which can be called after plug-in registration
   */
  register: function (plugin, name, callback) {
    return plugins.register(plugin, name, callback);
  },
  /**
   * Run registered plug-ins on given element
   *
   * @param element: DOM element
   * @param names: names of plug-in to run on given element; all if null
   */
  run: function (element) {
    let names = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : null;
    return plugins.run(element, names);
  }
};

/***/ }),

/***/ "./pkg/js/ext-require.js":
/*!*******************************!*\
  !*** ./pkg/js/ext-require.js ***!
  \*******************************/
/***/ (function(__unused_webpack_module, __webpack_exports__, __webpack_require__) {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": function() { return /* binding */ myams_require; }
/* harmony export */ });
/* global MyAMS */
/**
 * MyAMS dynamic module loader
 */

const $ = MyAMS.$;
function getModule(module, name) {
  let moduleSrc, moduleCss;
  if (typeof module === 'object') {
    moduleSrc = module.src;
    moduleCss = module.css;
  } else {
    if (module.startsWith('http://') || module.startsWith('https://')) {
      moduleSrc = module;
    } else if (module.endsWith('.js')) {
      // custom module with relative path
      moduleSrc = module;
    } else {
      // standard MyAMS module
      moduleSrc = `${MyAMS.env.baseURL}mod-${module}${MyAMS.env.devext}.js`;
    }
  }
  const deferred = [MyAMS.core.getScript(moduleSrc, {
    async: true
  }, console.error)];
  if (moduleCss) {
    deferred.push(MyAMS.core.getCSS(moduleCss, `${name}_css`));
  }
  return deferred;
}

/**
 * Dynamic loading of MyAMS modules
 *
 * @param modules: single module name, or array of modules names
 * @returns Promise
 */
function myams_require() {
  for (var _len = arguments.length, modules = new Array(_len), _key = 0; _key < _len; _key++) {
    modules[_key] = arguments[_key];
  }
  return new Promise((resolve, reject) => {
    const names = [],
      deferred = [],
      loaded = MyAMS.config.modules;
    for (const module of modules) {
      if (typeof module === 'string') {
        if (loaded.indexOf(module) < 0) {
          names.push(module);
          deferred.extendWith(getModule(module));
        }
      } else if ($.isArray(module)) {
        // strings array
        for (const name of module) {
          if (loaded.indexOf(name) < 0) {
            names.push(name);
            deferred.extendWith(getModule(name));
          }
        }
      } else {
        // object
        for (const [name, props] of Object.entries(module)) {
          if (loaded.indexOf(name) < 0) {
            names.push(name);
            deferred.extendWith(getModule(props, name));
          }
        }
      }
    }
    $.when.apply($, deferred).then(() => {
      for (const moduleName of names) {
        if (loaded.indexOf(moduleName) < 0) {
          loaded.push(moduleName);
          MyAMS.core.executeFunctionByName(`MyAMS.${moduleName}.init`);
        }
      }
      resolve();
    }, () => {
      reject(`Can't load requested modules (${names})!`);
    });
  });
}

/***/ }),

/***/ "jquery":
/*!*************************!*\
  !*** external "jquery" ***!
  \*************************/
/***/ (function(module) {

module.exports = jquery;

/***/ })

/******/ 	});
/************************************************************************/
/******/ 	// The module cache
/******/ 	var __webpack_module_cache__ = {};
/******/ 	
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/ 		// Check if module is in cache
/******/ 		var cachedModule = __webpack_module_cache__[moduleId];
/******/ 		if (cachedModule !== undefined) {
/******/ 			return cachedModule.exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = __webpack_module_cache__[moduleId] = {
/******/ 			// no module.id needed
/******/ 			// no module.loaded needed
/******/ 			exports: {}
/******/ 		};
/******/ 	
/******/ 		// Execute the module function
/******/ 		__webpack_modules__[moduleId](module, module.exports, __webpack_require__);
/******/ 	
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/ 	
/************************************************************************/
/******/ 	/* webpack/runtime/define property getters */
/******/ 	!function() {
/******/ 		// define getter functions for harmony exports
/******/ 		__webpack_require__.d = function(exports, definition) {
/******/ 			for(var key in definition) {
/******/ 				if(__webpack_require__.o(definition, key) && !__webpack_require__.o(exports, key)) {
/******/ 					Object.defineProperty(exports, key, { enumerable: true, get: definition[key] });
/******/ 				}
/******/ 			}
/******/ 		};
/******/ 	}();
/******/ 	
/******/ 	/* webpack/runtime/hasOwnProperty shorthand */
/******/ 	!function() {
/******/ 		__webpack_require__.o = function(obj, prop) { return Object.prototype.hasOwnProperty.call(obj, prop); }
/******/ 	}();
/******/ 	
/******/ 	/* webpack/runtime/make namespace object */
/******/ 	!function() {
/******/ 		// define __esModule on exports
/******/ 		__webpack_require__.r = function(exports) {
/******/ 			if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 				Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 			}
/******/ 			Object.defineProperty(exports, '__esModule', { value: true });
/******/ 		};
/******/ 	}();
/******/ 	
/************************************************************************/
var __webpack_exports__ = {};
// This entry need to be wrapped in an IIFE because it need to be isolated against other modules in the chunk.
!function() {
/*!******************************!*\
  !*** ./pkg/js/myams-core.js ***!
  \******************************/
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _ext_base__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./ext-base */ "./pkg/js/ext-base.js");
/* harmony import */ var _ext_require__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./ext-require */ "./pkg/js/ext-require.js");
/**
 * MyAMS core features
 *
 * This script is used to build MyAMS core-package.
 *
 * This package only includes MyAMS core features, but not CSS or external modules
 * which can be loaded using MyAMS.require function.
 */



_ext_base__WEBPACK_IMPORTED_MODULE_0__["default"].$.extend(_ext_base__WEBPACK_IMPORTED_MODULE_0__["default"], {
  require: _ext_require__WEBPACK_IMPORTED_MODULE_1__["default"]
});
const html = _ext_base__WEBPACK_IMPORTED_MODULE_0__["default"].$('html');
if (html.data('ams-init') !== false) {
  (0,_ext_base__WEBPACK_IMPORTED_MODULE_0__.init)(_ext_base__WEBPACK_IMPORTED_MODULE_0__["default"].$);
}

/** Version: 2.9.6  */
}();
/******/ })()
;
//# sourceMappingURL=myams-core-dev.js.map