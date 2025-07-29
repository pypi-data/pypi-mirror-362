/**
 * MyAMS callbacks module tests
 */

import $ from "jquery";

import MyAMS, { init } from "../ext-base";
import { callbacks } from "../mod-callbacks";
import { i18n } from "../mod-i18n";

import myams_require from "../ext-require";


init($);

if (!MyAMS.i18n) {
	MyAMS.i18n = i18n;
	MyAMS.config.modules.push('i18n');
}
MyAMS.require = myams_require;


// Test MyAMS.callbacks exists
test("Test MyAMS.callbacks may exist", () => {

	callbacks.init();
	expect(callbacks).toBeInstanceOf(Object);

});


// Test MyAMS.callbacks.initElement
test("Test MyAMS.callbacks.initElement from string", () => {

	MyAMS.testCallback = (element) => {
		$(element).addClass('modified');
	};

	document.body.innerHTML = `<div>
		<div class="inner"
			 data-ams-callback="MyAMS.testCallback"></div>
	</div>`;
	const body = $(document.body);
	return callbacks.initElement(body).then(() => {
		expect($('.inner', body).hasClass('modified')).toBe(true);
		delete MyAMS.testCallback;
	});

});

test("Test MyAMS.callbacks.initElement from object with options", () => {

	MyAMS.testCallback = (element, klass) => {
		$(element).addClass(klass);
	};

	document.body.innerHTML = `<div>
		<div class="inner"
			 data-ams-callback='{
			 	"callback": "MyAMS.testCallback",
			 	"options": "modified"
			 }'></div>
	</div>`;
	const body = $(document.body);
	return callbacks.initElement(body).then(() => {
		expect($('.inner', body).hasClass('modified')).toBe(true);
		delete MyAMS.testCallback;
	});

});

test("Test MyAMS.callbacks.initElement from object with source", () => {

	const
		oldAjax = $.ajax;
	$.ajax = jest.fn().mockImplementation(() => {
		MyAMS.testCallback = (element, klass) => {
			$(element).addClass(klass);
		};
		return Promise.resolve();
	});

	document.body.innerHTML = `<div>
		<div class="inner"
			 data-ams-callback='{
			 	"source": "resources/js/app.js",
			 	"callback": "MyAMS.testCallback",
			 	"options": "modified"
			 }'></div>
	</div>`;
	const body = $(document.body);
	return callbacks.initElement(body).then(() => {
		expect($('.inner', body).hasClass('modified')).toBe(true);
		delete MyAMS.testCallback;
		$.ajax = oldAjax;
	});

});

test("Test MyAMS.callbacks.initElement with missing callback", () => {

	const
		oldAjax = $.ajax;
	$.ajax = jest.fn().mockImplementation(() => {
		return Promise.resolve();
	});

	delete MyAMS.testCallback;
	document.body.innerHTML = `<div>
		<div class="inner"
			 data-ams-callback='{
			 	"source": "resources/js/missing.js",
			 	"callback": "MyAMS.testCallback",
			 	"options": "modified"
			 }'></div>
	</div>`;
	const body = $(document.body);
	return callbacks.initElement(body).then(() => {
		expect($('.inner', body).hasClass('modified')).toBe(false);
		$.ajax = oldAjax;
	});

});
