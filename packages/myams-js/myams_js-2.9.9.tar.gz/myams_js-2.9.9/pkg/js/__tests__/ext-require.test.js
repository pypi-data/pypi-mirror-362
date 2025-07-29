/**
 * MyAMS require tests
 */

import $ from "jquery";

import MyAMS, { init } from "../ext-base";

import myams_require from "../ext-require";


init($);

MyAMS.require = myams_require;


// Test MyAMS.require
test("Test MyAMS.require function (from string)", () => {

	const moduleName = 'ajax';
	let loaded = false;

	$.ajax = jest.fn().mockImplementation(() => {
		MyAMS.ajax = {
			init: () => {
				loaded = true;
			},
			callback: () => {
				return moduleName;
			}
		};
		MyAMS.config.modules.push(moduleName);
		return Promise.resolve();
	});
	return MyAMS.require('ajax').then(() => {
		expect(MyAMS.ajax).toBeInstanceOf(Object);
		expect(loaded).toBe(false);
		expect(MyAMS.ajax.callback()).toBe(moduleName);
	});
});

test("Test MyAMS.require function (from array names)", () => {

	const ajaxName = 'ajax';
	const formName = 'form';

	$.ajax = jest.fn().mockImplementation(() => {
		MyAMS.ajax = {
			callback: () => {
				return ajaxName;
			}
		};
		MyAMS.config.modules.push(ajaxName);
		MyAMS.form = {
			callback: () => {
				return formName;
			}
		}
		MyAMS.config.modules.push(formName);
		return Promise.resolve();
	});
	return MyAMS.require(['ajax','form']).then(() => {
		expect(MyAMS.ajax).toBeInstanceOf(Object);
		expect(MyAMS.ajax.callback()).toBe(ajaxName);
		expect(MyAMS.form).toBeInstanceOf(Object);
		expect(MyAMS.form.callback()).toBe(formName);
	});
});

test("Test MyAMS.require function (from object definition)", () => {

	const pluginName = 'app';
	$.ajax = jest.fn().mockImplementation(() => {
		MyAMS.app = {
			callback: () => {
				return pluginName;
			}
		}

		MyAMS.config.modules.push('app');
		return Promise.resolve();
	});
	return MyAMS.require({'app': 'resources/js/app.js'}).then(() => {
		expect(MyAMS.app).toBeInstanceOf(Object);
		expect(MyAMS.app.callback()).toBe(pluginName);
	});
});

test("Test MyAMS.require function (from URL)", () => {

	const pluginName = 'app';
	$.ajax = jest.fn().mockImplementation(() => {
		MyAMS.app = {
			callback: () => {
				return pluginName;
			}
		}

		MyAMS.config.modules.push('app');
		return Promise.resolve();
	});
	return MyAMS.require({'app': 'http://example.com/resources/js/app.js'}).then(() => {
		expect(MyAMS.app).toBeInstanceOf(Object);
		expect(MyAMS.app.callback()).toBe(pluginName);
	});
});
