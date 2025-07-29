/* global describe, jest, test, beforeAll, afterAll, expect */
/*
 * Test MyAMS notifications module
 */

import $ from "jquery";

import MyAMS, { init } from "../ext-base";
import { alert } from "../mod-alert";
import { ajax } from "../mod-ajax";
import { i18n } from "../mod-i18n";
import { modal } from "../mod-modal";
import { notifications } from "../mod-notifications";
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
if (!MyAMS.modal) {
	MyAMS.modal = modal;
	MyAMS.config.modules.push('modal');
}
if (!MyAMS.nav) {
	MyAMS.nav = nav;
	MyAMS.config.modules.push('nav');
}
if (!MyAMS.notifications) {
	MyAMS.notifications = notifications;
	MyAMS.config.modules.push('notifications');
}
if (!MyAMS.skin) {
	MyAMS.skin = skin;
	MyAMS.config.modules.push('skin');
}
MyAMS.require = myams_require;


describe("Test MyAMS.notifications module", () => {

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


	// Test MyAMS.notifications getNotifications function
	test("Test MyAMS.notifications getNotifications", () => {

		const
			response = {
				timestamp: 1587644933164,
				notifications: [
					{
						timestamp: 1587644933164,
						source: {
							title: "MyAMS.js",
							id: "user.id",
							avatar: "resources/img/profile.png"
						},
						host: "localhost",
						title: "Notification title",
						message: "Notification message",
						status: "success",
						url: "#test.html"
					},
					{
						timestamp: 1587644933164,
						source: {
							title: "MyAMS.js",
							id: "unknown"
						},
						host: "localhost",
						title: "Notification title",
						message: "Notification message",
						status: "success",
						url: "test.html",
						modal: true
					}
				]
			},
			oldAjax = $.ajax,
			oldXHR = window.XMLHttpRequest;

		window.XMLHttpRequest = jest.fn(() => {
			return MockXHR(response);
		});

		$.ajax = jest.fn().mockImplementation(() => {
			return Promise.resolve(response);
		});
		document.body.innerHTML = `<div>
			<a class="link" 
			   data-ams-notifications-source="data/notifications.json"
			   data-ams-notifications-target="#target">Link</a>
			<div id="target"></div>
		</div>`;

		const
			body = $(document.body),
			link = $('.link', body);
		const event = $.Event('click', {
			target: link,
			currentTarget: link
		});

		return MyAMS.notifications.getNotifications(event, {}).then(() => {
			expect($('li.alert-success', body).length).toBe(2);
			expect($('.timestamp', body).length).toBe(3);
			expect($('img.avatar', body).length).toBe(1);
			expect($('img.avatar', body).attr('src')).toBe('resources/img/profile.png');
			expect($('i.avatar', body).length).toBe(1);
			expect($('a[data-toggle="modal"]', body).length).toBe(1);
			$.ajax = oldAjax;
			window.XMLHttpRequest = oldXHR;
		});
	});

	test("Test MyAMS.notifications getNotifications with event data", () => {

		const
			response = {
				timestamp: 1587644933164,
				notifications: [
					{
						timestamp: 1587644933164,
						source: {
							title: "MyAMS.js",
							id: "user.id",
							avatar: "resources/img/profile.png"
						},
						host: "localhost",
						title: "Notification title",
						message: "Notification message",
						status: "success",
						url: "#test.html"
					},
					{
						timestamp: 1587644933164,
						source: {
							title: "MyAMS.js",
							id: "unknown"
						},
						host: "localhost",
						title: "Notification title",
						message: "Notification message",
						status: "success",
						url: "test.html",
						modal: true
					}
				]
			},
			oldAjax = $.ajax,
			oldXHR = window.XMLHttpRequest;

		window.XMLHttpRequest = jest.fn(() => {
			return MockXHR(response);
		});

		$.ajax = jest.fn().mockImplementation(() => {
			return Promise.resolve(response);
		});
		document.body.innerHTML = `
		<div data-ams-notifications-source="data/notifications.json"
			 data-ams-notifications-target="#target">
			<a class="link">Link</a>
			<div id="target"></div>
		</div>`;

		const
			body = $(document.body),
			link = $('.link', body);
		const event = $.Event('click', {
			data: {
				localTimestamp: true,
				hideTimestamp: true
			},
			target: link,
			currentTarget: link
		});

		return MyAMS.notifications.getNotifications(event).then(() => {
			expect($('.timestamp', body).length).toBe(2);
			expect($('a[data-toggle="modal"]', body).length).toBe(1);
			$.ajax = oldAjax;
			window.XMLHttpRequest = oldXHR;
		});
	});


	// Test MyAMS.notifications getNotificationsBadge function
	test("Test MyAMS.notifications getNotificationsBadge", () => {

		const
			response = {
				timestamp: 1587644933164,
				notifications: [
					{
						timestamp: 1587644933164,
						source: {
							title: "MyAMS.js",
							id: "user.id",
							avatar: "resources/img/profile.png"
						},
						host: "localhost",
						title: "Notification title",
						message: "Notification message",
						status: "success",
						url: "#test.html"
					},
					{
						timestamp: 1587644933164,
						source: {
							title: "MyAMS.js",
							id: "unknown"
						},
						host: "localhost",
						title: "Notification title",
						message: "Notification message",
						status: "success",
						url: "test.html",
						modal: true
					}
				]
			},
			oldAjax = $.ajax,
			oldXHR = window.XMLHttpRequest;

		window.XMLHttpRequest = jest.fn(() => {
			return MockXHR(response);
		});

		$.ajax = jest.fn().mockImplementation(() => {
			return Promise.resolve(response);
		});
		document.body.innerHTML = `
		<div id="user-notifications"
			 data-ams-notifications-source="data/notifications.json">
			<span id="notifications-count"></span>
		</div>`;

		localStorage.setItem('notifications-timestamp', '2020-01-01T12:00');
		return MyAMS.notifications.getNotificationsBadge().then(() => {
			expect($('#notifications-count').text()).toBe('2');
			$.ajax = oldAjax;
			window.XMLHTTPRequest = oldXHR;
		});
	});


	// Test MyAMS.notifications addNotification function
	test("Test MyAMS.notifications addNotification", () => {

		const
			message = {
				timestamp: 1587644933164,
				source: {
					title: "MyAMS.js",
					id: "user.id",
					avatar: "resources/img/profile.png"
				},
				host: "localhost",
				title: "Notification title",
				message: "Notification message",
				status: "success",
				url: "#test.html"
			};

		document.body.innerHTML = `<div id="notifications-pane">
			<span id="notifications-count"></span>
			<ul></ul>
		</div>`;

		const body = $(document.body);
		MyAMS.notifications.addNotification(message, false);
		expect($('#notifications-count').text()).toBe('1');
		expect($('li', body).length).toBe(1);
	});
});
