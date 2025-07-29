/* global describe, beforeAll, afterAll, jest, test, expect */
/**
 * MyAMS alert module tests
 */

import $ from "jquery";

import MyAMS, { init } from "../ext-base";
import { alert } from "../mod-alert";
import { ajax } from "../mod-ajax";
import { events } from "../mod-events";
import { i18n } from "../mod-i18n";
import { modal } from "../mod-modal";
import { nav } from "../mod-nav";
import { skin } from "../mod-skin";

import myams_require from "../ext-require";

import { MockXHR } from "../__mocks__/xhr";

const bs = require("bootstrap");

// tooltips are required
$.fn.tooltip = bs.Tooltip._jQueryInterface;
$.fn.tooltip.Constructor = bs.Tooltip;


init($);

if (!MyAMS.i18n) {
	MyAMS.i18n = i18n;
	MyAMS.config.modules.push('i18n');
}
if (!MyAMS.ajax) {
	MyAMS.ajax = ajax;
	MyAMS.config.modules.push('ajax');
}
if (!MyAMS.alert) {
	MyAMS.alert = alert;
	MyAMS.config.modules.push('alert');
}
if (!MyAMS.events) {
	MyAMS.events = events;
	MyAMS.config.modules.push('events');
}
if (!MyAMS.modal) {
	MyAMS.modal = modal;
	MyAMS.config.modules.push('modal');
}
if (!MyAMS.nav) {
	MyAMS.nav = nav;
	MyAMS.config.modules.push('nav');
}
if (!MyAMS.skin) {
	MyAMS.skin = skin;
	MyAMS.config.modules.push('skin');
}
MyAMS.require = myams_require;


describe("Test MyAMS.skin module", () => {

	let oldOpen = null,
		oldAlert = null,
		oldLocation = null;

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
			reload: jest.fn(),
			replace: jest.fn()
		}
	});

	afterAll(() => {
		window.open = oldOpen;
		window.alert = oldAlert;
		window.location = oldLocation;
	});

	// Test MyAMS.skin init function
	test("Test MyAMS.skin init function", () => {

		const body = $(document.body);

		MyAMS.dom = {
			root: body
		};

		MyAMS.skin.init();

	});


	// Test MyAMS.skin initElement
	test("Test MyAMS.js initElement function", () => {

		document.body.innerHTML = `<div>
			<i class="hint" title="Title"></i>
		</div>`;

		const body = $(document.body);

		MyAMS.config.enableTooltips = false;
		MyAMS.skin.initElement(body);

	});


	// Test MyAMS.skin checkURL event handler
	test("Test MyAMS.skin checkURL event handler with JSON content", () => {

		const
			response = {
				contentType: 'application/json',
				status: 'success',
				content: '<div class="result">This is my result</div>'
			},
			oldAjax = $.ajax,
			oldXHR = window.XMLHttpRequest;

		window.XMLHttpRequest = jest.fn(() => {
			return MockXHR(response);
		});

		$.ajax = jest.fn().mockImplementation(() => {
			const request = XMLHttpRequest();
			return Promise.all([response, 'success', request]);
		});

		document.body.innerHTML = `<div>
			<nav>
				<ul>
					<li><a href="#test.html">Test link</a></li>
				</ul>
			</nav>
			<div id="content"></div>
		</div>`;

		const
			body = $(document.body);

		MyAMS.dom = {
			root: body,
			nav: $('nav', body)
		};

		window.location.hash = '#test.html!content';
		MyAMS.skin.checkURL();  //.then(() => {
		// 	expect($('#content').text().trim()).toBe("This is my result");
		$.ajax = oldAjax;
		window.XMLHttpRequest = oldXHR;
		// });
	});

	test("Test MyAMS.skin checkURL event handler with JSON without content", () => {

		const
			response = {
				contentType: 'application/json',
				status: 'success',
				content: '<div class="result">This is my result</div>'
			},
			oldAjax = $.ajax,
			oldXHR = window.XMLHttpRequest;

		window.XMLHttpRequest = jest.fn(() => {
			return MockXHR(response);
		});

		$.ajax = jest.fn().mockImplementation(() => {
			const request = XMLHttpRequest();
			return Promise.all([response, 'success', request]);
		});

		document.body.innerHTML = `<div>
			<nav>
				<ul>
					<li><a href="#test.html">Test link</a></li>
				</ul>
			</nav>
			<div id="ignored"></div>
		</div>`;

		const
			body = $(document.body);

		MyAMS.dom = {
			root: body,
			nav: $('nav', body)
		};

		window.location.hash = '#test.html!content';
		MyAMS.skin.checkURL();  //.then(() => {
		// 	expect($('#content').text().trim()).toBe("This is my result");
		$.ajax = oldAjax;
		window.XMLHttpRequest = oldXHR;
		// });
	});


	// Test MyAMS.skin loadURL function
	test("Test MyAMS.skin loadURL function", () => {

		const
			response = {
				contentType: 'application/json',
				status: 'success',
				content: '<div class="result">This is my result</div>'
			},
			oldAjax = $.ajax,
			oldXHR = window.XMLHttpRequest;

		window.XMLHttpRequest = jest.fn(() => {
			return MockXHR(response);
		});

		$.ajax = jest.fn().mockImplementation((settings) => {
			settings.beforeSend();
			const request = XMLHttpRequest();
			return Promise.all([response, 'success', request]);
		});

		document.body.innerHTML = `<div>
			<nav>
				<ul>
					<li><a href="#test.html">Test link</a></li>
				</ul>
			</nav>
			<div id="content"></div>
		</div>`;

		const
			body = $(document.body);

		MyAMS.dom = {
			root: body,
			nav: $('nav', body)
		};

		return MyAMS.skin.loadURL('#test.html', '#content', {}).then(() => {
			expect($('.fa-cog').exists()).toBe(false);
			$.ajax = oldAjax;
			window.XMLHttpRequest = oldXHR;
		});
	});

});
