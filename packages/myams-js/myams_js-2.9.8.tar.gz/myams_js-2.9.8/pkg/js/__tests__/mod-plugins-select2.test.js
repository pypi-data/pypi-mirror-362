/* global describe, jest, test, beforeAll, afterAll, expect */
/**
 * MyAMS.plugins "select2" plug-in tests
 */

import $ from "jquery";
window.$ = window.jQuery = $;
global.$ = global.jQuery = $;

require("jquery-ui");
require("jquery-ui/ui/version");
require("jquery-ui/ui/disable-selection");
require("jquery-ui/ui/plugin");
require("jquery-ui/ui/widgets/mouse");
require("jquery-ui/ui/widgets/draggable");
require("jquery-ui/ui/widgets/droppable");
require("jquery-ui/ui/widgets/sortable");

import MyAMS, { init } from "../ext-base";
import { ajax } from "../mod-ajax";
import { alert } from "../mod-alert";
import { helpers } from "../mod-helpers";
import { i18n } from "../mod-i18n";

import { select2 as modSelect2 } from "../mod-plugins";
import select2 from "select2";
$.fn.select2 = select2;

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


describe("MyAMS.plugins.select2 unit tests", () => {

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


	// Test MyAMS.plugins without any select
	test("Test MyAMS.plugins without select", () => {

		document.body.innerHTML = `<div></div>`;

		const body = $(document.body);

		return modSelect2(body).then((result) => {
			expect(result).toBeNull();
		});
	});


	// Test MyAMS.plugins with select2
	test("Test MyAMS.plugins with select2", () => {

		document.body.innerHTML = `<div>
			<select class="select2">
				<option value="1">Option 1</option>
			</select>
		</div>`;

		const
			body = $(document.body),
			select = $('.select2', body);

		select.on('after-init.ams.select2', (evt, select) => {
			select.data('after-init', true);
		});

		return modSelect2(body).then((result) => {
			expect(result.length).toBe(1);
			expect(select.data('after-init')).toBe(true);
		});
	});

	test("Test MyAMS.plugins with select2 with veto", () => {

		document.body.innerHTML = `<div>
			<select class="select2">
				<option value="1">Option 1</option>
			</select>
		</div>`;

		const
			body = $(document.body),
			select = $('.select2', body);

		select.on('before-init.ams.select2', (evt, select, settings, veto) => {
			select.data('before-init', true);
			veto.veto = true;
		})
		select.on('after-init.ams.select2', (evt, select) => {
			select.data('after-init', true);
		});

		return modSelect2(body).then((result) => {
			expect(result.length).toBe(1);
			expect(select.data('before-init')).toBe(true);
			expect(select.data('after-init')).toBeUndefined();
		});
	});

	test("Test MyAMS.plugins with sortable select2", () => {

		document.body.innerHTML = `<div>
			<select class="select2 sortable" name="mySelect">
				<option value="1" selected>Option 1</option>
				<option value="2">Option 2</option>
			</select>
		</div>`;

		const
			body = $(document.body),
			select = $('.select2', body);

		return modSelect2(body).then((result) => {
			expect(result.length).toBe(1);
			const hidden = $('input[type="hidden"]', body)
			expect(hidden.length).toBe(1);
			expect(hidden.attr('name')).toBe('mySelect');
			expect(select.attr('name')).toBeUndefined();
		});
	});
});