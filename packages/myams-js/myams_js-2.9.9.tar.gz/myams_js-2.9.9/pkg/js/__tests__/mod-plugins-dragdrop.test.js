/* global describe, jest, test, beforeAll, afterAll, expect */
/**
 * MyAMS.plugins "draggable/droppable" plug-ins tests
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
import { i18n } from "../mod-i18n";

import { dragdrop } from "../mod-plugins";

import myams_require from "../ext-require";

const bs = require("bootstrap");

// Bootstrap toasts are required...
$.fn.toast = bs.Toast._jQueryInterface;
$.fn.toast.Constructor = bs.Toast;


init($);

if (!MyAMS.ajax) {
	MyAMS.ajax = ajax;
	MyAMS.config.modules.push('ajax');
}
if (!MyAMS.alert) {
	MyAMS.alert = alert;
	MyAMS.config.modules.push('alert');
}
if (!MyAMS.i18n) {
	MyAMS.i18n = i18n;
	MyAMS.config.modules.push('i18n');
}
if (!MyAMS.plugins) {
	MyAMS.config.modules.push('plugins');
}
MyAMS.require = myams_require;


describe("MyAMS.plugins.dragdrop unit tests", () => {

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


	// Test MyAMS.plugins without any draggable/droppable/sortable
	test("Test MyAMS.plugins without draggable", () => {

		document.body.innerHTML = `<div></div>`;

		const body = $(document.body);

		return dragdrop(body).then((result) => {
			expect(result).toBeNull();
		});
	});


	// Test MyAMS.plugins draggables
	test("Test MyAMS.plugins draggable plug-in", () => {

		document.body.innerHTML = `<div>
			<div class="draggable"></div>
		</div>`;

		const
			body = $(document.body),
			dragitem = $('.draggable', body);

		dragitem.on('after-init.ams.draggable', (evt, item) => {
			dragitem.data('after-init', true);
		});

		return dragdrop(body).then((result) => {
			expect(result.length).toBe(1);
			// expect(dragitem.data('after-init')).toBe(true);
		});
	});

	test("Test MyAMS.plugins draggable plug-in with initialization veto", () => {

		document.body.innerHTML = `<div>
			<div class="draggable"></div>
		</div>`;

		const
			body = $(document.body),
			dragitem = $('.draggable', body);

		dragitem.on('before-init.ams.draggable', (evt, item, settings, veto) => {
			veto.veto = true;
		});
		dragitem.on('after-init.ams.draggable', (evt, item) => {
			dragitem.data('after-init', true);
		});

		return dragdrop(body).then((result) => {
			expect(result.length).toBe(1);
			expect(dragitem.data('after-init')).toBeUndefined();
		});
	});


	// Test MyAMS.plugins droppables
	test("Test MyAMS.plugins droppable plug-in", () => {

		document.body.innerHTML = `<div>
			<div class="droppable"></div>
		</div>`;

		const
			body = $(document.body),
			dropitem = $('.droppable', body);

		dropitem.on('after-init.ams.droppable', (evt, item) => {
			dropitem.data('after-init', true);
		});

		return dragdrop(body).then((result) => {
			expect(result.length).toBe(1);
			expect(dropitem.data('after-init')).toBe(true);
		});
	});

	test("Test MyAMS.plugins droppable plug-in with initialization veto", () => {

		document.body.innerHTML = `<div>
			<div class="droppable"></div>
		</div>`;

		const
			body = $(document.body),
			dropitem = $('.droppable', body);

		dropitem.on('before-init.ams.droppable', (evt, item, settings, veto) => {
			veto.veto = true;
		});
		dropitem.on('after-init.ams.droppable', (evt, item) => {
			dropitem.data('after-init', true);
		});

		return dragdrop(body).then((result) => {
			expect(result.length).toBe(1);
			expect(dropitem.data('after-init')).toBeUndefined();
		});
	});


	// Test MyAMS.plugins sortables
	test("Test MyAMS.plugins sortable plug-in", () => {

		document.body.innerHTML = `<div>
			<div class="sortable">
				<div class="item"></div>
				<div class="item"></div>
				<div class="item"></div>
			</div>
		</div>`;

		const
			body = $(document.body),
			sortitem = $('.sortable', body);

		sortitem.on('after-init.ams.sortable', (evt, item) => {
			sortitem.data('after-init', true);
		});

		return dragdrop(body).then((result) => {
			expect(result.length).toBe(1);
			expect(sortitem.data('after-init')).toBe(true);
		});
	});

	test("Test MyAMS.plugins sortable plug-in with initialization veto", () => {

		document.body.innerHTML = `<div>
			<div class="sortable">
				<div class="item"></div>
				<div class="item"></div>
				<div class="item"></div>
			</div>
		</div>`;

		const
			body = $(document.body),
			sortitem = $('.sortable', body);

		sortitem.on('before-init.ams.sortable', (evt, item, settings, veto) => {
			veto.veto = true;
		});
		sortitem.on('after-init.ams.sortable', (evt, item) => {
			sortitem.data('after-init', true);
		});

		return dragdrop(body).then((result) => {
			expect(result.length).toBe(1);
			expect(sortitem.data('after-init')).toBeUndefined();
		});
	});


	// Test MyAMS.plugins draggable with droppable
	test("Test MyAMS.plugins draggable with droppable", () => {

		document.body.innerHTML = `<div>
			<div class="draggable"></div>
			<div class="droppable"
				 data-ams-droppable-accept=".draggable"></div>
		</div>`;

		const
			body = $(document.body),
			dragitem = $('.draggable', body),
			dropitem = $('.droppable', body);

		dragitem.on('after-init.ams.draggable', (evt, item) => {
			dragitem.data('after-init', true);
		});
		dropitem.on('after-init.ams.droppable', (evt, item) => {
			dropitem.data('after-init', true);
		});

		return dragdrop(body).then((result) => {
			expect(result.length).toBe(2);
			expect(dragitem.data('after-init')).toBe(true);
			expect(dropitem.data('after-init')).toBe(true);
		});
	});
});
