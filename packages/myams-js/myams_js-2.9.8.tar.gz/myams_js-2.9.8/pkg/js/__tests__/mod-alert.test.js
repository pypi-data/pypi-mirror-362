/* global test, expect */
/**
 * MyAMS alert module tests
 */

import $ from "jquery";

import MyAMS, { init } from "../ext-base";
import { alert } from "../mod-alert";
import { i18n } from "../mod-i18n";
import { modal } from "../mod-modal";

import myams_require from "../ext-require";

const bs = require("bootstrap");


init($);

if (!MyAMS.i18n) {
	MyAMS.i18n = i18n;
	MyAMS.config.modules.push('i18n');
}
if (!MyAMS.alert) {
	MyAMS.alert = alert;
	MyAMS.config.modules.push('alert');
}
if (!MyAMS.modal) {
	MyAMS.modal = modal;
	MyAMS.config.modules.push('modal');
}
MyAMS.require = myams_require;


// Test MyAMS.alert.alert
test("Test MyAMS.alert.alert function", () => {

	document.body.innerHTML = `<div>
		<div class="parent"></div>
	</div>`;
	const
		body = $(document.body),
		parent = $('.parent', body);
	alert.alert({
		status: 'info',
		parent: parent,
		header: 'header',
		message: 'This is a message'
	});
	const alertDiv = $('.alert', parent);
	expect(alertDiv.exists()).toBe(true);
	expect($('.alert-heading', alertDiv).text()).toBe('header');
	expect($('li', alertDiv).text()).toBe('This is a message');

});

test("Test MyAMS.alert.alert function from messages array", () => {

	document.body.innerHTML = `<div>
		<div class="parent"></div>
	</div>`;
	const
		body = $(document.body),
		parent = $('.parent', body);
	alert.alert({
		status: 'error',
		parent: parent,
		header: 'header',
		message: ['This is first message', 'This is second message']
	});
	const alertDiv = $('.alert', parent);
	expect(alertDiv.exists()).toBe(true);
	expect(alertDiv.hasClass('alert-danger')).toBe(true);
	expect($('.alert-heading', alertDiv).text()).toBe('header');
	expect($('li', alertDiv).length).toBe(2);

});


// Test MyAMS.alert.messageBox
test("Test MyAMS.alert.messageBox function", () => {

	document.body.innerHTML = `<div></div>`;
	// Init DOM
	const body = $(document.body);
	MyAMS.dom = {
		root: body
	};
	// Bootstrap toasts are required...
	$.fn.toast = bs.Toast._jQueryInterface;
	$.fn.toast.Constructor = bs.Toast;

	alert.messageBox({
		status: 'error',
		icon: 'fa-info-circle',
		title: 'Message title',
		message: 'Message content',
		timeout: 0
	});
	const container = $(`.${MyAMS.config.alertsContainerClass}`);
	expect(container.exists());
	let toast = $('.toast', container);
	expect(toast.exists()).toBe(true);
	expect(toast.length).toBe(1);
	expect(toast.hasClass('toast-danger')).toBe(true);
	expect(toast.data('autohide')).toBe(false);
	expect($('i.fa', toast).hasClass('fa-info-circle')).toBe(true);
	expect($('strong', toast).text()).toBe('Message title');
	expect($('.toast-body', toast).text().trim()).toBe('Message content');

});


// Test MyAMS.alert.smallBox
test("Test MyAMS.alert.smallBox function", () => {

	document.body.innerHTML = `<div></div>`;
	// Init DOM
	const body = $(document.body);
	MyAMS.dom = {
		root: body
	};
	// Bootstrap toasts are required...
	$.fn.toast = bs.Toast._jQueryInterface;
	$.fn.toast.Constructor = bs.Toast;

	alert.smallBox({
		status: 'error',
		icon: 'fa-info-circle',
		message: 'Message content'
	});
	const container = $(`.${MyAMS.config.alertsContainerClass}`);
	expect(container.exists());
	let toast = $('.toast', container);
	expect(toast.exists()).toBe(true);
	expect(toast.length).toBe(1);
	expect(toast.hasClass('toast-danger')).toBe(true);
	expect(toast.data('autohide')).toBe(true);
	expect($('i.fa', toast).hasClass('fa-info-circle')).toBe(true);
	expect($('.toast-body', toast).text().trim()).toBe('Message content');

});


// Test MyAMS.alert.bigBox
test("Test MyAMS.alert.bigBox function", () => {

	document.body.innerHTML = `<body></body>`;
	// Init DOM
	const body = $(document.body);
	MyAMS.dom = {
		root: body
	};
	// Bootstrap toasts are required...
	$.fn.toast = bs.Toast._jQueryInterface;
	$.fn.toast.Constructor = bs.Toast;

	alert.bigBox({
		status: 'error',
		icon: 'fa-info-circle',
		title: 'Message title',
		message: 'Message content'
	});
	let modalBox = $('.modal');
	expect(modalBox.exists()).toBe(false);

});
