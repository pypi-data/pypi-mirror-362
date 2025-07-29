/* global $, FontAwesome */
/**
 * MyAMS base features
 */

if (!window.jQuery) {
	window.$ = window.jQuery = require('jquery');
}


import { registry } from "./ext-registry";


/**
 * Init JQuery extensions
 */
export function init($) {

	/**
	 * String prototype extensions
	 */
	$.extend(String.prototype, {

		/**
		 * Replace dashed names with camelCase variation
		 */
		camelCase: function() {
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
		deCase: function() {
			if (!this) {
				return this;
			}
			return this.replace(/[A-Z]/g, (cap) => {
				return `-${cap.toLowerCase()}`;
			});
		},

		/**
		 * Convert first letter only to lowercase
		 */
		initLowerCase: function() {
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
			const
				str = decodeURIComponent(this),
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
		extendWith: function(source) {
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
		extendPrefix: function(source, prefix, getter, ...extensions) {
			for (const extension of extensions) {
				for (const [key, value] of Object.entries(extension)) {
					if (key.startsWith(prefix)) {
						source[key.substring(prefix.length).initLowerCase()] =
							getter === null ? value : getter(value);
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
		extendOnly: function(source, getter, ...extensions) {
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
		exists: function() {
			return $(this).length > 0;
		},

		/**
		 * Get object if it supports given CSS class,
		 * otherwise look for parents
		 */
		objectOrParentWithClass: function(klass) {
			if (this.hasClass(klass)) {
				return this;
			}
			return this.parents(`.${klass}`);
		},

		/**
		 * Build an array of attributes of the given selection
		 */
		listattr: function(attr) {
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
		style: function(styleName, value, priority) {
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
						priority = typeof (priority) !== 'undefined' ? priority : '';
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
		removeClassPrefix: function(prefix) {
			this.each(function(i, it) {
				const classes = it.className.split(/\s+/).map((item) => {
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
		html.removeClass('no-js')
			.addClass('js');
		MyAMS.core.executeFunctionByName(html.data('ams-init-page') ||
			MyAMS.config.initPage);
	});
}


/**
 * Get list of modules names required by given element
 *
 * @param element: parent element
 * @returns {*[]}
 */
export function getModules(element) {
	let modules = [];
	const mods = element.data('ams-modules');
	if (typeof mods === 'string') {
		modules = modules.concat(mods.trim().split(/[\s,;]+/));
	} else if (mods) {
		for (const [name, props] of Object.entries(mods)) {
			if (modules.find((elt) => (elt === name) || elt[name]) === undefined) {
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
				if (modules.find((elt) => (elt === name) || elt[name]) === undefined) {
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
export function initPage() {
	return MyAMS.require('i18n').then(() => {
		MyAMS.dom = getDOM();
		MyAMS.theme = getTheme();
		executeFunctionByName(MyAMS.config.initData, window, MyAMS.dom.root);
		const modules = getModules(MyAMS.dom.root);
		MyAMS.require(...modules).then(() => {
			for (const moduleName of MyAMS.config.modules) {
				executeFunctionByName(`MyAMS.${moduleName}.init`);
			}
			executeFunctionByName(MyAMS.dom.page.data('ams-init-content') ||
				MyAMS.config.initContent);
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
export function initData(element) {
	$('[data-ams-data]', element).each((idx, elt) => {
		const
			$elt = $(elt),
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
export function initContent(element=null) {

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
export function clearContent(element) {
	if (typeof element === 'string') {
		element = $(element);
	}
	return new Promise((resolve, reject) => {
		const veto = { veto: false };
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
export function getObject(objectName, context) {
	if (!objectName) {
		return undefined;
	}
	if (typeof objectName !== 'string') {
		return objectName;
	}
	const namespaces = objectName.split('.');
	context = (context === undefined || context === null) ? window : context;
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
export function getFunctionByName(functionName, context) {
	if ((functionName === null) || (typeof functionName === 'undefined')) {
		return undefined;
	} else if (typeof functionName === 'function') {
		return functionName;
	} else if (typeof functionName !== 'string') {
		return undefined;
	}
	const
		namespaces = functionName.split("."),
		func = namespaces.pop();
	context = (context === undefined || context === null) ? window : context;
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
export function executeFunctionByName(functionName, context /*, args */) {
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
export function getSource(url) {
	return url.replace(/{[^{}]*}/g, (match) => {
		return getObject(match.substr(1, match.length - 2));
	});
}


/**
 * Dynamic script loader function
 *
 * @param url: script URL
 * @param options: a set of options to be added to AJAX call
 */
export function getScript(url, options={}) {

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
		})
	});
}


/**
 * Get CSS matching given URL
 *
 * @param url: CSS source URL
 * @param name: name of the given CSS
 */
export function getCSS(url, name) {

	return new Promise((resolve /*, reject */) => {
		const head = $('HEAD');
		let style = $(`style[data-ams-id="${name}"]`, head);
		if (style.length === 0) {
			style = $('<style>').attr('data-ams-id', name)
								.text(`@import "${getSource(url)}";`)
								.appendTo(head);
			const styleInterval = setInterval(() => {
				try {
					// eslint-disable-next-line no-unused-vars
					const _check = style[0].sheet.cssRules;  // Is only populated when file is loaded
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
export function getQueryVar(src, varName) {
	// Check src
	if ((typeof src !== 'string') || (src.indexOf('?') < 0)) {
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
export function generateId() {

	function s4() {
		return Math.floor((1 + Math.random()) * 0x10000).toString(16).substring(1);
	}

	return s4() + s4() + s4() + s4();
}


/**
 * Generate a random unique UUID
 */
export function generateUUID() {
	let d = new Date().getTime();
	return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
		const r = (d + Math.random() * 16) % 16 | 0;
		d = Math.floor(d / 16);
		return (c === 'x' ? r : (r & 0x3 | 0x8)).toString(16);
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
export function switchIcon(element, fromClass, toClass, prefix='fa') {
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
		element.removeClass(`fa-${fromClass}`)
			.addClass(`fa-${toClass}`);
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
	const
		script = $(
			'script[src*="/myams.js"], script[src*="/myams-dev.js"], ' +
			'script[src*="/emerald.js"], script[src*="/emerald-dev.js"], ' +
			'script[src*="/darkmode.js"], script[src*="/darkmode-dev.js"], ' +
			'script[src*="/lightmode.js"], script[src*="/lightmode-dev.js"], ' +
			'script[src*="/myams-core.js"], script[src*="/myams-core-dev.js"], ' +
			'script[src*="/myams-mini.js"], script[src*="/myams-mini-dev.js"]'),
		src = script.attr('src'),
		devmode = src ? src.indexOf('-dev.js') >= 0 : true,  // testing mode
		bundle = src ? src.indexOf('-core') < 0 : true;  // MyAMS modules not included in 'core' package
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
		const css = $(
			'link[href*="/myams.css"], ' +
			'link[href*="/emerald.css"], ' +
			'link[href*="/darkmode.css"], ' +
			'link[href*="/lightmode.css"]'
		);
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
	}
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
const
	isMobile = /iphone|ipad|ipod|android|blackberry|mini|windows\sce|palm/i.test(
					navigator.userAgent.toLowerCase()),
	config = {
		modules: [],
		ajaxNav: true,
		enableFastclick: true,
		useSVGIcons:
			(window.FontAwesome !== undefined) && (FontAwesome.config.autoReplaceSvg === 'nest'),
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
	registry: registry
};
window.MyAMS = MyAMS;

export default MyAMS;
