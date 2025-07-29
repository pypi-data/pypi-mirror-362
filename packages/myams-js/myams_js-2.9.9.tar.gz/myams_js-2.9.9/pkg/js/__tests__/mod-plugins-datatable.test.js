/* global describe, jest, test, beforeAll, afterAll, expect */
/**
 * MyAMS.plugins "datatables" plug-in tests
 */

import $ from "jquery";
window.$ = window.jQuery = $;
global.$ = global.jQuery = $;

import MyAMS, { init } from "../ext-base";
import { ajax } from "../mod-ajax";
import { alert } from "../mod-alert";
import { helpers } from "../mod-helpers";
import { i18n } from "../mod-i18n";

import { datatables as modDatatables } from "../mod-plugins";

import myams_require from "../ext-require";


init($);

if (!MyAMS.ajax) {
	MyAMS.ajax = ajax;
	MyAMS.config.modules.push('ajax');
}
if (!MyAMS.alert) {
	MyAMS.alert = alert;
	MyAMS.config.modules.push('alert');
}
if (!MyAMS.helpers) {
	MyAMS.helpers = helpers;
	MyAMS.config.modules.push('helpers');
}
if (!MyAMS.i18n) {
	MyAMS.i18n = i18n;
	MyAMS.config.modules.push('i18n');
}
if (!MyAMS.plugins) {
	MyAMS.config.modules.push('plugins');
}
MyAMS.require = myams_require;


describe("MyAMS.plugins.datatables unit tests", () => {

	let oldOpen = null,
		oldAlert = null,
		oldLocation = null,
		oldAjax = null;

	beforeAll(() => {
		oldOpen = window.open;
		window.open = jest.fn();

		oldAlert = window.alert;
		window.alert = jest.fn();

		oldLocation = window.location;
		delete window.location;
		window.location = {
			protocol: oldLocation.protocol,
			href: oldLocation.href,
			hash: oldLocation.hash,
			reload: jest.fn()
		}

		oldAjax = $.ajax;
		$.ajax = jest.fn().mockImplementation((settings) => {
			return Promise.resolve({settings: settings, status: 'success'});
		});
	});

	afterAll(() => {
		window.open = oldOpen;
		window.alert = oldAlert;
		window.location = oldLocation;
		$.ajax = oldAjax;
	});


	// Test MyAMS.plugins without any datatable
	test("Test MyAMS.plugins without datatable", () => {

		document.body.innerHTML = `<div></div>`;

		const body = $(document.body);

		return modDatatables(body).then((result) => {
			expect(result).toBeNull();
		});
	});

});
