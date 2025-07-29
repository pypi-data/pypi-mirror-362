/* global describe, jest, test, beforeAll, afterAll, expect */
/**
 * MyAMS.plugins "draggable/droppable" plug-ins tests
 */

import $ from "jquery";
window.$ = window.jQuery = $;
global.$ = global.jQuery = $;

import MyAMS, { init } from "../ext-base";
import { ajax } from "../mod-ajax";
import { alert } from "../mod-alert";
import { form } from "../mod-form";
import { i18n } from "../mod-i18n";
import { menu } from "../mod-menu";
import { skin } from "../mod-skin";


import { contextMenu } from "../mod-plugins";

import myams_require from "../ext-require";

const bs = require("bootstrap");


init($);

if (!MyAMS.ajax) {
	MyAMS.ajax = ajax;
	MyAMS.config.modules.push('ajax');
}
if (!MyAMS.alert) {
	MyAMS.alert = alert;
	MyAMS.config.modules.push('alert');
}
if (!MyAMS.form) {
	MyAMS.form = form;
	MyAMS.config.modules.push('form');
}
if (!MyAMS.i18n) {
	MyAMS.i18n = i18n;
	MyAMS.config.modules.push('i18n');
}
if (!MyAMS.menu) {
	MyAMS.menu = menu;
	MyAMS.config.modules.push('menu');
}
if (!MyAMS.skin) {
	MyAMS.skin = skin;
	MyAMS.config.modules.push('skin');
}
if (!MyAMS.plugins) {
	MyAMS.config.modules.push('plugins');
}
MyAMS.require = myams_require;


describe("MyAMS.plugins.contextmenu unit tests", () => {

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

		// Bootstrap drop-downs are required...
		$.fn.dropdown = bs.Dropdown._jQueryInterface;
		$.fn.dropdown.Constructor = bs.Dropdown;

		MyAMS.menu.init();
	});

	afterAll(() => {
		window.open = oldOpen;
		window.alert = oldAlert;
		window.location = oldLocation;
		$.ajax = oldAjax;
	});


	// Test MyAMS.plugins without any context menu
	test("Test MyAMS.plugins without context menu", () => {

		document.body.innerHTML = `<div></div>`;

		const body = $(document.body);

		return contextMenu(body).then((result) => {
			expect(result).toBeNull();
		});
	});


	// Test MyAMS.plugins dropdown
	test("Test MyAMS.plugins contextMenu plug-in", () => {

		document.body.innerHTML = `<div>
			<div class="context-menu"></div>
		</div>`;

		const
			body = $(document.body),
			menu = $('.context-menu', body);

		menu.on('after-init.ams.contextmenu', (evt, item) => {
			menu.data('after-init', true);
		});

		return contextMenu(body).then((result) => {
			expect(result.length).toBe(1);
			expect(menu.data('after-init')).toBe(true);
		});
	});

	test("Test MyAMS.plugins contextMenu plug-in with initialization veto", () => {

		document.body.innerHTML = `<div>
			<div class="context-menu"></div>
		</div>`;

		const
			body = $(document.body),
			menu = $('.context-menu', body);

		menu.on('before-init.ams.contextmenu', (evt, item, settings, veto) => {
			veto.veto = true;
		});
		menu.on('after-init.ams.contextmenu', (evt, item) => {
			menu.data('after-init', true);
		});

		return contextMenu(body).then((result) => {
			expect(result.length).toBe(1);
			expect(menu.data('after-init')).toBeUndefined();
		});
	});

	test("Test MyAMS.plugins contextMenu handle", () => {

		document.body.innerHTML = `<div>
			<div class="context-menu">
				<a class="dropdown-item">Menu item</a>
			</div>
		</div>`;

		const
			body = $(document.body),
			menu = $('.context-menu', body),
			item = $('.dropdown-item', menu);

		return contextMenu(body).then((result) => {
			menu.trigger('contextmenu');
			item.trigger('click');
		});
	});
});
