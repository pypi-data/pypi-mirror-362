/* global describe, jest, test, beforeAll, afterAll, expect */
/**
 * MyAMS.plugins "fileinput" plug-in tests
 */

import $ from "jquery";
window.$ = window.jQuery = $;
global.$ = global.jQuery = $;

import bsCustomFileInput from "bs-custom-file-input";
global.bsCustomFileInput = bsCustomFileInput;

import MyAMS, { init } from "../ext-base";
import { ajax } from "../mod-ajax";
import { alert } from "../mod-alert";
import { i18n } from "../mod-i18n";


import { fileInput } from "../mod-plugins";

import myams_require from "../ext-require";


init($);

if (!MyAMS.ajax) {
	MyAMS.ajax = ajax;
	MyAMS.config.modules.push('ajax');
}
if (!MyAMS.i18n) {
	MyAMS.i18n = i18n;
	MyAMS.config.modules.push('i18n');
}
if (!MyAMS.alert) {
	MyAMS.alert = alert;
	MyAMS.config.modules.push('alert');
}
MyAMS.require = myams_require;


describe("MyAMS.plugins.fileinput unit tests", () => {

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


	// Test MyAMS.plugins without any file input
	test("Test MyAMS.plugins without file input", () => {

		document.body.innerHTML = `<div></div>`;

		const body = $(document.body);

		return fileInput(body).then((result) => {
			expect(result).toBeNull();
		});
	});


	// Test MyAMS.plugins with default file input
	test("Test MyAMS.plugins fileInput plug-in", () => {

		document.body.innerHTML = `<div>
			<form novalidate>
				<input class="custom-file-input" />
			</form>
		</div>`;

		const
			body = $(document.body),
			fileinput = $('.custom-file-input', body);

		fileinput.on('after-init.ams.fileinput', (evt, item) => {
			fileinput.data('after-init', true);
		});

		return fileInput(body).then((result) => {
			expect(result.length).toBe(1);
			expect(fileinput.data('after-init')).toBe(true);
		});
	});

	test("Test MyAMS.plugins fileInput plug-in with initialization veto", () => {

		document.body.innerHTML = `<div>
			<form novalidate>
				<input class="custom-file-input" />
			</form>
		</div>`;

		const
			body = $(document.body),
			fileinput = $('.custom-file-input', body);

		fileinput.on('before-init.ams.fileinput', (evt, item, veto) => {
			veto.veto = true;
		});
		fileinput.on('after-init.ams.fileinput', (evt, item) => {
			fileinput.data('after-init', true);
		});

		return fileInput(body).then((result) => {
			expect(result.length).toBe(1);
			expect(fileinput.data('after-init')).toBeUndefined();
		});
	});
});
