/* global describe, jest, test, beforeAll, afterAll, expect */
/**
 * MyAMS helpers module test
 */

import $ from 'jquery';

import MyAMS, { init } from "../ext-base";
import { ajax } from "../mod-ajax";
import { alert } from "../mod-alert";
import { helpers } from "../mod-helpers";
import { i18n } from "../mod-i18n";
import { events } from "../mod-events";

import { datetime as modDatetime } from "../mod-plugins";

import myams_require from "../ext-require";
import { MockXHR } from "../__mocks__/xhr";

const moment = require("moment");
window.moment = moment;

const bs = require("bootstrap");
const td = require("tempusdominus-bootstrap-4");


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
if (!MyAMS.events) {
	MyAMS.events = events;
	MyAMS.config.modules.push('events');
}
if (!MyAMS.plugins) {
	MyAMS.config.modules.push('plugins');
}

MyAMS.require = myams_require;


describe("MyAMS.helpers unit tests", () => {

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

	// Test MyAMS.helpers.clearValue
	test("Test MyAMS.helpers clearValue", () => {

		document.body.innerHTML = `<div>
			<input id="source" type="checkbox" data-target="#target" />
			<input id="target" type="text" value="current value" />
		</div>`;

		const
			source = $('#source'),
			target = $('#target');
		const event = $.Event('click', {
			currentTarget: source
		});

		expect(target.val()).toBe('current value');
		MyAMS.helpers.clearValue(event);
		expect(target.val()).toBe('');

	});


	// Test MyAMS.helpers.clearDatetimeValue
	test("Test MyAMS.helpers clearDatetimeValue", () => {

		document.body.innerHTML = `<div>
			<input id="source" type="button" data-target="#target" />
			<input id="target" type="text" class="datetime" value="2023/01/01" />
		</div>`;

		const
			source = $('#source'),
			target = $('#target');
		const event = $.Event('click', {
			currentTarget: source
		});

		expect(target.val()).toBe('2023/01/01');

		return modDatetime(document.body).then(() => {
			expect(target.data('datetimepicker')).toBeInstanceOf(Object);
			MyAMS.helpers.clearDatetimeValue(event);
			expect(target.val()).toBe('');
		});
	});


	// Test MyAMS.helpers setSEOStatus
	test("Test MyAMS.helpers testSEOStatus", () => {

		document.body.innerHTML = `<div>
			<input id="title" type="text" />
			<div class="progress">
				<div class="progress-bar"></div>
			</div>
		</div>`;

		const
			target = $('#title'),
			progress = $('.progress-bar');
		const event = $.Event('click', {
			target: target
		});

		target.val('Test');  // < 20 characters
		MyAMS.helpers.setSEOStatus(event);
		expect(progress.hasClass('bg-danger')).toBe(true);
		expect(progress.css('width')).toBe('4%');

		target.val('Test with 20 to 40 characters');
		MyAMS.helpers.setSEOStatus(event);
		expect(progress.hasClass('bg-warning')).toBe(true);
		expect(progress.css('width')).toBe('29%');

		target.val('Test with 40 to 60 characters - xxxxxxxxxxxxxxxxxx');
		MyAMS.helpers.setSEOStatus(event);
		expect(progress.hasClass('bg-success')).toBe(true);
		expect(progress.css('width')).toBe('50%');

		target.val('Test with 60 to 80 characters - xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx');
		MyAMS.helpers.setSEOStatus(event);
		expect(progress.hasClass('bg-warning')).toBe(true);
		expect(progress.css('width')).toBe('70%');

		target.val('Test with 80 to 100 characters - xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx');
		MyAMS.helpers.setSEOStatus(event);
		expect(progress.hasClass('bg-danger')).toBe(true);
		expect(progress.css('width')).toBe('90%');

		target.val('Test with more than 100 characters - xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx');
		MyAMS.helpers.setSEOStatus(event);
		expect(progress.hasClass('bg-danger')).toBe(true);
		expect(progress.css('width')).toBe('100%');

	});


	// Test MyAMS.helpers select2ChangeHelper
	test("Test MyAMS.helpers select2ChangeHelper", () => {

		const
			response = `<p>This is the response.</p>`,
			oldAjax = $.ajax,
			oldXHR = window.XMLHttpRequest;

		window.XMLHttpRequest = jest.fn(() => {
			return MockXHR(response);
		});

		$.ajax = jest.fn().mockImplementation(() => {
			return Promise.resolve(response);
		});

		document.body.innerHTML = `<div>
			<input class="select2" data-ams-select2-helper-type="html"
				   data-ams-select2-helper-target="#target"
				   data-ams-select2-helper-url="get-page.html"
				   value="select-value" />
			<div id="target"></div>
		</div>`;

		const
			body = $(document.body),
			source = $('.select2', body),
			target = $('#target');
		const event = $.Event('change', {
			currentTarget: source
		});

		return MyAMS.helpers.select2ChangeHelper(event).then(() => {
			expect(target.html()).toBe(response);
		}).finally(() => {
			$.ajax = oldAjax;
			window.XMLHttpRequest = oldXHR;
		});

	});


	// Test MyAMS.helpers refreshElement
	test("Test MyAMS.helpers refreshElement", () => {

		const response = {
			object_id: 'target',
			content: '<p id="newTarget">This is the response</p>'
		};

		document.body.innerHTML = `<div>
			<form id="testForm" novalidate>
				<div id="target"></div>
			</form>
		</div>`;

		const form = $('#testForm');

		return MyAMS.helpers.refreshElement(form, response).then(() => {
			const target = $('[id="newTarget"]');
			expect(target.html()).toBe("This is the response");
		});

	});


	// Test MyAMS.helpers moveElementToParentEnd
	test("Test MyAMS.helpers moveElementToParentEnd", () => {

		document.body.innerHTML = `<div>
			<ul>
				<li class="first"></li>
				<li class="second"></li>
				<li class="last"></li>
			</ul>
		</div>`;

		const
			list = $('ul'),
			item = $('.first', list);

		MyAMS.helpers.moveElementToParentEnd(item);
		const classes = $('li', list).listattr('class');
		expect(classes.length).toBe(3);
		expect(classes[0]).toBe('second');
		expect(classes[1]).toBe('last');
		expect(classes[2]).toBe('first');

	});


	// Test MyAMS.helpers hideDropdown
	test("Test MyAMS.helpers hideDropdown", () => {

		document.body.innerHTML = `<div>
			<a class="dropdown-toggle" data-toggle="dropdown" aria-expanded="false">Open menu</a>
			<div class="dropdown-menu">
				<button class="submit">Submit</button>
			</div>
		</div>`;

		$.fn.dropdown = bs.Dropdown._jQueryInterface;
		$.fn.dropdown.Constructor = bs.Dropdown;

		const
			link = $('a.dropdown-toggle'),
			menu = $('.dropdown-menu'),
			button = $('button');

		expect(link.attr('aria-expanded')).toBe('false');
		link.dropdown('show');
		expect(link.attr('aria-expanded')).toBe('true');
		expect(menu.hasClass('show')).toBe(true);

		button.on('click', MyAMS.helpers.hideDropdown);
		button.trigger('click');
		// expect(link.attr('aria-expanded')).toBe('false');
		// expect(menu.hasClass('show')).toBe(false);

	});

});
