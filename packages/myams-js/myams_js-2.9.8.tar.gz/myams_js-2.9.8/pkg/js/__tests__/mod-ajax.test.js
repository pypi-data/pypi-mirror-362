/* global describe, jest, test, beforeAll, afterAll, expect */
/**
 * MyAMS AJAX module package tests
 */

import $ from 'jquery';

import MyAMS, { init } from '../ext-base';
import { ajax } from '../mod-ajax';
import { alert } from "../mod-alert";
import { error } from "../mod-error";
import { events } from "../mod-events";
import { form } from "../mod-form";
import { i18n } from "../mod-i18n";
import { modal } from "../mod-modal";
import { skin } from "../mod-skin";

import myams_require from "../ext-require";

import { MockXHR } from "../__mocks__/xhr";

const bs = require("bootstrap");
// Bootstrap modals are required
$.fn.modal = bs.Modal._jQueryInterface;
$.fn.modal.Constructor = bs.Modal;
// Bootstrap toasts are required
$.fn.toast = bs.Toast._jQueryInterface;
$.fn.toast.Constructor = bs.Toast;


if (!MyAMS.ajax) {
	MyAMS.ajax = ajax;
	MyAMS.config.modules.push('ajax');
}
if (!MyAMS.alert) {
	MyAMS.alert = alert;
	MyAMS.config.modules.push('alert');
}
if (!MyAMS.error) {
	MyAMS.error = error;
	MyAMS.config.modules.push('error');
}
if (!MyAMS.events) {
	MyAMS.events = events;
	MyAMS.config.modules.push('events');
}
if (!MyAMS.form) {
	MyAMS.form = form;
	MyAMS.config.modules.push('form');
}
if (!MyAMS.i18n) {
	MyAMS.i18n = i18n;
	MyAMS.config.modules.push('i18n');
}
if (!MyAMS.modal) {
	MyAMS.modal = modal;
	MyAMS.config.modules.push('modal');
}
if (!MyAMS.skin) {
	MyAMS.skin = skin;
	MyAMS.config.modules.push('skin');
}
MyAMS.require = myams_require;


init($);


describe("MyAMS.ajax unit tests", () => {

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
			reload: jest.fn()
		}
	});

	afterAll(() => {
		window.open = oldOpen;
		window.alert = oldAlert;
		window.location = oldLocation;
	});

	// Test MyAMS.ajax exists
	test("Test MyAMS.ajax may exist", () => {

		expect(ajax).toBeInstanceOf(Object);

	});


	// Test MyAMS.ajax.check
	test("Test MyAMS.ajax check function", done => {

		function callback(firstLoad, options = {}) {
			expect(firstLoad).toBe(false);
			expect(options).toBeInstanceOf(Object);
			done();
		}

		ajax.check(window.jQuery, '').then(callback);
		ajax.check([window.jQuery], ['']).then(callback);
		ajax.check([window.jQuery], '').then(callback);
		ajax.check(window.missing, '').then(callback);
		ajax.check(window.missing, ['']).then(callback);

	});


	// Test MyAMS.ajax.getAddr
	test("Test MyAMS.ajax getAddr function", () => {

		expect(ajax.getAddr()).toBe('http://localhost/');
		expect(ajax.getAddr('http://example.com/index.html')).toBe('http://example.com/');
		expect(ajax.getAddr('http://example.com/path/index.html')).toBe('http://example.com/path/');

	});


	// Test MyAMS.ajax.start
	test("Test MyAMS.ajax start/stop functions", () => {

		document.body.innerHTML = `<div>
			<div id="ajax-gear"></div>
		</div>`;

		const gear = $('#ajax-gear');
		ajax.start();
		expect(gear.css('display')).toBe('block');
		ajax.stop();
		expect(gear.css('display')).toBe('none');

	});


	// Test MyAMS.ajax.get
	test("Test MyAMS.ajax get function", () => {

		const
			url = 'http://example.com/url',
			oldAjax = $.ajax;
		$.ajax = jest.fn().mockImplementation((settings) => {
			return Promise.resolve({settings: settings, status: 'success'});
		});
		return ajax.get(url).then((result) => {
			expect(result.settings.type).toBe('get');
			expect(result.settings.url).toBe(url);
			expect(result.settings.dataType).toBe('json');
			expect(result.status).toBe('success');
			$.ajax = oldAjax;
		});
	});

	test("Test MyAMS.ajax get function with params", () => {

		const
			url = 'http://example.com/url',
			oldAjax = $.ajax;
		$.ajax = jest.fn().mockImplementation((settings) => {
			return Promise.resolve({settings: settings, status: 'success'});
		});
		return ajax.get(url, {fieldName: 'value'}).then((result) => {
			expect(result.settings.type).toBe('get');
			expect(result.settings.url).toBe(url);
			expect(result.settings.data).toBe('fieldName=value');
			expect(result.status).toBe('success');
			$.ajax = oldAjax;
		});
	});

	test("Test MyAMS.ajax get function with options", () => {

		const
			url = 'http://example.com/url',
			oldAjax = $.ajax;
		$.ajax = jest.fn().mockImplementation((settings) => {
			return Promise.resolve({settings: settings, status: 'success'});
		});
		return ajax.get(url, {}, {dataType: 'text'}).then((result) => {
			expect(result.settings.type).toBe('get');
			expect(result.settings.url).toBe(url);
			expect(result.settings.dataType).toBe('text');
			expect(result.status).toBe('success');
			$.ajax = oldAjax;
		});
	});

	test("Test MyAMS.ajax get function with params and options", () => {

		const
			url = 'http://example.com/url',
			oldAjax = $.ajax;
		$.ajax = jest.fn().mockImplementation((settings) => {
			return Promise.resolve({settings: settings, status: 'success'});
		});
		return ajax.get(url, {fieldName: 'value'}, {dataType: 'text'}).then((result) => {
			expect(result.settings.type).toBe('get');
			expect(result.settings.url).toBe(url);
			expect(result.settings.data).toBe('fieldName=value');
			expect(result.settings.dataType).toBe('text');
			expect(result.status).toBe('success');
			$.ajax = oldAjax;
		});
	});


	// Test MyAMS.ajax.post
	test("Test MyAMS.ajax post function", () => {

		const
			url = 'http://example.com/url',
			oldAjax = $.ajax;
		$.ajax = jest.fn().mockImplementation((settings) => {
			return Promise.resolve({settings: settings, status: 'success'});
		});
		return ajax.post(url).then((result) => {
			expect(result.settings.type).toBe('post');
			expect(result.settings.url).toBe(url);
			expect(result.settings.dataType).toBe('json');
			expect(result.status).toBe('success');
			$.ajax = oldAjax;
		});
	});

	test("Test MyAMS.ajax post function with params", () => {

		const
			url = 'http://example.com/url',
			oldAjax = $.ajax;
		$.ajax = jest.fn().mockImplementation((settings) => {
			return Promise.resolve({settings: settings, status: 'success'});
		});
		return ajax.post(url, {fieldName: 'value'}).then((result) => {
			expect(result.settings.type).toBe('post');
			expect(result.settings.url).toBe(url);
			expect(result.settings.data).toBe('fieldName=value');
			expect(result.status).toBe('success');
			$.ajax = oldAjax;
		});
	});

	test("Test MyAMS.ajax post function with options", () => {

		const
			url = 'http://example.com/url',
			oldAjax = $.ajax;
		$.ajax = jest.fn().mockImplementation((settings) => {
			return Promise.resolve({settings: settings, status: 'success'});
		});
		return ajax.post(url, {}, {dataType: 'text'}).then((result) => {
			expect(result.settings.type).toBe('post');
			expect(result.settings.url).toBe(url);
			expect(result.settings.dataType).toBe('text');
			expect(result.status).toBe('success');
			$.ajax = oldAjax;
		});
	});

	test("Test MyAMS.ajax post function with params and options", () => {

		const
			url = 'http://example.com/url',
			oldAjax = $.ajax;
		$.ajax = jest.fn().mockImplementation((settings) => {
			return Promise.resolve({settings: settings, status: 'success'});
		});
		return ajax.post(url, {fieldName: 'value'}, {dataType: 'text'}).then((result) => {
			expect(result.settings.type).toBe('post');
			expect(result.settings.url).toBe(url);
			expect(result.settings.data).toBe('fieldName=value');
			expect(result.settings.dataType).toBe('text');
			expect(result.status).toBe('success');
			$.ajax = oldAjax;
		});
	});

	test("Test MyAMS.ajax post function with params and options with content-type", () => {

		const
			url = 'http://example.com/url',
			oldAjax = $.ajax;
		$.ajax = jest.fn().mockImplementation((settings) => {
			return Promise.resolve({settings: settings, status: 'success'});
		});
		return ajax.post(url, {fieldName: 'value'}, {dataType: 'text', contentType: 'application/json'}).then((result) => {
			expect(result.settings.type).toBe('post');
			expect(result.settings.url).toBe(url);
			expect(result.settings.data).toBe('{"fieldName":"value"}');
			expect(result.settings.dataType).toBe('text');
			expect(result.status).toBe('success');
			$.ajax = oldAjax;
		});
	});


	// Test MyAMS.ajax getResponse function
	test("Test MyAMS.ajax getResponse function with JSON result", () => {

		const
			url = 'http://localhost/form-submit.json',
			response = {
				contentType: 'application/json',
				status: 'success',
				content: {
					status: 'success',
					value: 1
				}
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

		return ajax.post(url).then(([result, status, xhr]) => {
			expect(status).toBe('success');
			expect(xhr.getResponseHeader('content-type')).toBe('application/json');

			const response = MyAMS.ajax.getResponse(xhr);
			expect(response.contentType).toBe('json');
			expect(response.data.status).toBe('success');
			expect(response.data.value).toBe(1);

			$.ajax = oldAjax;
			window.XMLHttpRequest = oldXHR;
		});

	});

	test("Test MyAMS.ajax getResponse function with missing content-type", () => {

		const
			url = 'http://localhost/form-submit.json',
			response = {
				contentType: null,
				status: 'success'
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

		return ajax.post(url).then(([result, status, xhr]) => {
			expect(status).toBe('success');
			expect(xhr.getResponseHeader('content-type')).toBe(null);

			const response = MyAMS.ajax.getResponse(xhr);
			expect(response.contentType).toBe('json');
			expect(response.data.status).toBe('alert');
			expect(response.data.alert.title).toBe(MyAMS.i18n.ERROR_OCCURED);
			expect(response.data.alert.content).toBe(MyAMS.i18n.NO_SERVER_RESPONSE);

			$.ajax = oldAjax;
			window.XMLHttpRequest = oldXHR;
		});

	});

	test("Test MyAMS.ajax getResponse function with Javascript result", () => {

		const
			url = 'http://localhost/form-submit.json',
			response = {
				contentType: 'application/javascript',
				status: 'success',
				content: '/* This is Javascript */'
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

		return ajax.post(url).then(([result, status, xhr]) => {
			expect(status).toBe('success');
			expect(xhr.getResponseHeader('content-type')).toBe('application/javascript');

			const response = MyAMS.ajax.getResponse(xhr);
			expect(response.contentType).toBe('script');
			expect(response.data).toBe('/* This is Javascript */');

			$.ajax = oldAjax;
			window.XMLHttpRequest = oldXHR;
		});

	});

	test("Test MyAMS.ajax getResponse function with HTML result", () => {

		const
			url = 'http://localhost/form-submit.json',
			response = {
				contentType: 'text/html',
				status: 'success',
				content: '<html><body>This is HTML</body></html>'
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

		return ajax.post(url).then(([result, status, xhr]) => {
			expect(status).toBe('success');
			expect(xhr.getResponseHeader('content-type')).toBe('text/html');

			const response = MyAMS.ajax.getResponse(xhr);
			expect(response.contentType).toBe('html');
			expect(response.data).toBe('<html><body>This is HTML</body></html>');

			$.ajax = oldAjax;
			window.XMLHttpRequest = oldXHR;
		});

	});

	test("Test MyAMS.ajax getResponse function with text result", () => {

		const
			url = 'http://localhost/form-submit.json',
			response = {
				contentType: 'text/plain',
				status: 'success',
				content: 'This is text'
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

		return ajax.post(url).then(([result, status, xhr]) => {
			expect(status).toBe('success');
			expect(xhr.getResponseHeader('content-type')).toBe('text/plain');

			const response = MyAMS.ajax.getResponse(xhr);
			expect(response.contentType).toBe('binary');
			expect(response.data).toBe('This is text');

			$.ajax = oldAjax;
			window.XMLHttpRequest = oldXHR;
		});

	});

	test("Test MyAMS.ajax getResponse function with JSON result as text", () => {

		const
			url = 'http://localhost/form-submit.json',
			response = {
				contentType: 'text/plain',
				status: 'success',
				content: '{ "status": "success", "message": "This is a message" }'
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

		return ajax.post(url).then(([result, status, xhr]) => {
			expect(status).toBe('success');
			expect(xhr.getResponseHeader('content-type')).toBe('text/plain');

			const response = MyAMS.ajax.getResponse(xhr);
			expect(response.contentType).toBe('json');
			expect(response.data.status).toBe('success');
			expect(response.data.message).toBe('This is a message');

			$.ajax = oldAjax;
			window.XMLHttpRequest = oldXHR;
		});

	});


	// Test MyAMS.ajax handleJSON function
	test("Test MyAMS.ajax handleJSON function for alert result", () => {

		const
			url = 'http://localhost/form-submit.json',
			response = {
				contentType: 'application/json',
				status: 'success',
				content: {
					status: 'alert',
					alert: {
						title: "Alert title",
						content: "Alert content"
					}
				}
			},
			oldAjax = $.ajax,
			oldAlert = window.alert,
			oldXHR = window.XMLHttpRequest;
		let alert = null;

		window.alert = (message) => {
			alert = message;
		};
		window.XMLHttpRequest = jest.fn(() => {
			return MockXHR(response);
		});

		$.ajax = jest.fn().mockImplementation(() => {
			const request = XMLHttpRequest();
			return Promise.all([response, 'success', request]);
		});

		return ajax.post(url).then(([result, status, request]) => {
			const response = MyAMS.ajax.getResponse(request);
			MyAMS.ajax.handleJSON(response.data);
			expect(alert).toBe('Alert title\n\nAlert content');

			$.ajax = oldAjax;
			window.alert = oldAlert,
			window.XMLHttpRequest = oldXHR;
		});

	});

	test("Test MyAMS.ajax handleJSON function for simple error result", () => {

		const
			url = 'http://localhost/form-submit.json',
			response = {
				contentType: 'application/json',
				status: 'success',
				content: {
					status: 'error',
					error: "Simple error message"
				}
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

		let ajaxResponse;
		return ajax.post(url).then(([result, status, request]) => {
			ajaxResponse = MyAMS.ajax.getResponse(request);
		}).then(() => {
			return MyAMS.ajax.handleJSON(ajaxResponse.data, $(document.body)).then(() => {
				return $('.alert').length;
			}).then((value) => {
				// expect(value).toBe(1);
				$.ajax = oldAjax;
				window.XMLHttpRequest = oldXHR;
			});
		});

	});

	test("Test MyAMS.ajax handleJSON function with modal result", () => {

		const
			url = 'http://localhost/form-submit.json',
			response = {
				contentType: 'application/json',
				status: 'success',
				content: {
					status: 'modal',
					location: "#modal1"
				}
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
			<div id="modal1" class="modal"></div>
		</div>`;

		let ajaxResponse;
		return ajax.post(url).then(([result, status, request]) => {
			ajaxResponse = MyAMS.ajax.getResponse(request);
		}).then(() => {
			return MyAMS.ajax.handleJSON(ajaxResponse.data, $(document.body)).then(() => {
				// expect($('.modal').hasClass('show')).toBe(true);
				$.ajax = oldAjax;
				window.XMLHttpRequest = oldXHR;
			});
		});

	});

	test("Test MyAMS.ajax handleJSON function with reload result", () => {

		const
			url = 'http://localhost/form-submit.json',
			response = {
				contentType: 'application/json',
				status: 'success',
				content: {
					status: 'reload',
					location: "#modal1"
				}
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
			<div id="content" class="container"></div>
		</div>`;

		let ajaxResponse;
		return ajax.post(url).then(([result, status, request]) => {
			ajaxResponse = MyAMS.ajax.getResponse(request);
		}).then(() => {
			return MyAMS.ajax.handleJSON(ajaxResponse.data, $(document.body)).then(() => {
				// expect($('#content').hasClass('show')).toBe(true);
				$.ajax = oldAjax;
				window.XMLHttpRequest = oldXHR;
			});
		});

	});

	test("Test MyAMS.ajax handleJSON function with redirect result", () => {

		const
			url = 'http://localhost/form-submit.json',
			response = {
				contentType: 'application/json',
				status: 'success',
				content: {
					status: 'redirect'
				}
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
			<div id="content" class="container"></div>
		</div>`;

		let ajaxResponse;
		return ajax.post(url).then(([result, status, request]) => {
			ajaxResponse = MyAMS.ajax.getResponse(request);
		}).then(() => {
			return MyAMS.ajax.handleJSON(ajaxResponse.data, $(document.body)).then(() => {
				expect(window.location.reload).toHaveBeenCalled();
				$.ajax = oldAjax;
				window.XMLHttpRequest = oldXHR;
			});
		});

	});

	test("Test MyAMS.ajax handleJSON function with simple content result", () => {

		const
			url = 'http://localhost/form-submit.json',
			response = {
				contentType: 'application/json',
				status: 'success',
				content: {
					status: 'success',
					content: '<p class="result">This is my result!</p>'
				}
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
			<div id="content" class="container"></div>
		</div>`;

		let ajaxResponse;
		return ajax.post(url).then(([result, status, request]) => {
			ajaxResponse = MyAMS.ajax.getResponse(request);
		}).then(() => {
			MyAMS.ajax.handleJSON(ajaxResponse.data, $(document.body)); //.then(() => {
			// 	expect($('.result').exists()).toBe(true);
			// 	expect($('.result').text()).toBe('This is my result!');
			$.ajax = oldAjax;
			window.XMLHttpRequest = oldXHR;
			// });
		});

	});

	test("Test MyAMS.ajax handleJSON function with rich content result", () => {

		const
			url = 'http://localhost/form-submit.json',
			response = {
				contentType: 'application/json',
				status: 'success',
				content: {
					status: 'success',
					content: {
						html: '<p class="result">This is my result!</p>',
						target: '#target'
					}
				}
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
			<div id="target" class="container"></div>
		</div>`;

		let ajaxResponse;
		return ajax.post(url).then(([result, status, request]) => {
			ajaxResponse = MyAMS.ajax.getResponse(request);
		}).then(() => {
			MyAMS.ajax.handleJSON(ajaxResponse.data, $(document.body));  //.then(() => {
			// 	expect($('.result', '#target').exists()).toBe(true);
			// 	expect($('.result', '#target').text()).toBe('This is my result!');
			$.ajax = oldAjax;
			window.XMLHttpRequest = oldXHR;
			// });
		});

	});

	test("Test MyAMS.ajax handleJSON function with simple message result", () => {

		const
			url = 'http://localhost/form-submit.json',
			response = {
				contentType: 'application/json',
				status: 'success',
				content: {
					status: 'success',
					message: 'This is my result!'
				}
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
			<div id="content" class="container"></div>
		</div>`;

		let ajaxResponse;
		return ajax.post(url).then(([result, status, request]) => {
			ajaxResponse = MyAMS.ajax.getResponse(request);
		}).then(() => {
			MyAMS.ajax.handleJSON(ajaxResponse.data, $(document.body));  //.then(() => {
			// 	expect($('.toast').exists()).toBe(true);
			$.ajax = oldAjax;
			window.XMLHttpRequest = oldXHR;
			// });
		});

	});

	test("Test MyAMS.ajax handleJSON function with event result", () => {

		const
			url = 'http://localhost/form-submit.json',
			response = {
				contentType: 'application/json',
				status: 'success',
				content: {
					status: 'success',
					event: 'test.ams'
				}
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
			<div id="content" class="container"></div>
		</div>`;

		let event = false;
		$(document).on('test.ams', () => {
			event = true;
		});

		let ajaxResponse;
		return ajax.post(url).then(([result, status, request]) => {
			ajaxResponse = MyAMS.ajax.getResponse(request);
		}).then(() => {
			MyAMS.ajax.handleJSON(ajaxResponse.data, $(document.body));  //.then(() => {
			// 	expect(event).toBe(true);
			$.ajax = oldAjax;
			window.XMLHttpRequest = oldXHR;
			// });
		});

	});

	test("Test MyAMS.ajax handleJSON function with multiple events result", () => {

		const
			url = 'http://localhost/form-submit.json',
			response = {
				contentType: 'application/json',
				status: 'success',
				content: {
					status: 'success',
					events: [
						'test1.ams',
						{
							event: 'test2.ams',
							options: 'Value 1'
						}
					]
				}
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
			<div id="content" class="container"></div>
		</div>`;

		let events = [];
		$(document).on('test1.ams', () => {
			events.push('test1');
		});
		$(document).on('test2.ams', () => {
			events.push('test2');
		});

		let ajaxResponse;
		return ajax.post(url).then(([result, status, request]) => {
			ajaxResponse = MyAMS.ajax.getResponse(request);
		}).then(() => {
			MyAMS.ajax.handleJSON(ajaxResponse.data, $(document.body));  //.then(() => {
			// 	expect(events.length).toBe(2);
			// 	expect(events.indexOf('test1')).toBeGreaterThan(-1);
			// 	expect(events.indexOf('test2')).toBeGreaterThan(-1);
			$.ajax = oldAjax;
			window.XMLHttpRequest = oldXHR;
			// });
		});

	});

	test("Test MyAMS.ajax handleJSON function with callback result", () => {

		const
			url = 'http://localhost/form-submit.json',
			response = {
				contentType: 'application/json',
				status: 'success',
				content: {
					status: 'success',
					callback: 'MyAMS.test.callback',
					options: 'Value 1'
				}
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
			<div id="content" class="container"></div>
		</div>`;

		let called;
		MyAMS.test = {
			callback: (parent, value) => {
				called = value
			}
		};

		let ajaxResponse;
		return ajax.post(url).then(([result, status, request]) => {
			ajaxResponse = MyAMS.ajax.getResponse(request);
		}).then(() => {
			MyAMS.ajax.handleJSON(ajaxResponse.data, $(document.body));  //.then(() => {
			// 	expect(called).toBe('Value 1');
			delete MyAMS.test;
			$.ajax = oldAjax;
			window.XMLHttpRequest = oldXHR;
			// });
		});

	});

	test("Test MyAMS.ajax handleJSON function with multiple callbacks result", () => {

		const
			url = 'http://localhost/form-submit.json',
			response = {
				contentType: 'application/json',
				status: 'success',
				content: {
					status: 'success',
					callbacks: [
						'MyAMS.test.callback',
						{
							callback: 'MyAMS.test.callback2',
							options: 'Value 2'
						}
					],
					options: 'Value 1'
				}
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
			<div id="content" class="container"></div>
		</div>`;

		let called1,
			called2;
		MyAMS.test = {
			callback: (parent, value) => {
				called1 = value;
			},
			callback2: (parent, value) => {
				called2 = value;
			}
		};

		let ajaxResponse;
		return ajax.post(url).then(([result, status, request]) => {
			ajaxResponse = MyAMS.ajax.getResponse(request);
		}).then(() => {
			MyAMS.ajax.handleJSON(ajaxResponse.data, $(document.body));  //.then(() => {
			// 	expect(called1).toBe('Value 1');
			// 	expect(called2).toBe('Value 2');
			delete MyAMS.test;
			$.ajax = oldAjax;
			window.XMLHttpRequest = oldXHR;
			// });
		});

	});


	// Test MyAMS.ajax error
	test("Test MyAMS.ajax error function without error", () => {

		const
			url = 'http://localhost/form-submit.json',
			response = {
				contentType: 'application/json',
				status: 'success',
				statusText: 'OK',
				content: {
					status: 'success'
				}
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

		return ajax.post(url).then(([result, status, request]) => {
			ajax.error($.Event(), request, request, 'OK');
			$.ajax = oldAjax;
			window.XMLHttpRequest = oldXHR;
		});

	});

	test("Test MyAMS.ajax error function with abort", () => {

		const
			url = 'http://localhost/form-submit.json',
			response = {
				contentType: 'text/plain',
				status: 'success',
				statusText: 'Bad request',
				content: "Error message"
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

		return ajax.post(url).then(([result, status, request]) => {
			ajax.error($.Event(), request, request, 'abort');
			$.ajax = oldAjax;
			window.XMLHttpRequest = oldXHR;
		});

	});

	test("Test MyAMS.ajax error function with HTML error", () => {

		const
			url = 'http://localhost/form-submit.json',
			response = {
				contentType: 'text/plain',
				status: 'success',
				statusText: 'Bad request',
				content: "Error message"
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

		return ajax.post(url).then(([result, status, request]) => {
			ajax.error($.Event(), request, request, 'error');
			$.ajax = oldAjax;
			window.XMLHttpRequest = oldXHR;
		});

	});

	test("Test MyAMS.ajax error function with HTML error", () => {

		const
			url = 'http://localhost/form-submit.json',
			response = {
				contentType: 'text/plain',
				status: 'success',
				statusText: 'Bad request',
				content: "Error message"
			},
			oldAjax = $.ajax,
			oldXHR = window.XMLHttpRequest;

		window.XMLHttpRequest = jest.fn(() => {
			return MockXHR(response);
		});

		$.ajax = jest.fn().mockImplementation(() => {
			const request = XMLHttpRequest();
			return Promise.all([response, 'error', request]);
		});

		return ajax.post(url).then(([result, status, request]) => {
			ajax.error($.Event(), request, request, 'error');
			$.ajax = oldAjax;
			window.XMLHttpRequest = oldXHR;
		});

	});

	test("Test MyAMS.ajax error function with unknown error", () => {

		const
			url = 'http://localhost/form-submit.json',
			response = {
				contentType: 'image/unknown',
				status: 'success',
				statusText: 'Bad request'
			},
			oldAjax = $.ajax,
			oldXHR = window.XMLHttpRequest;

		window.XMLHttpRequest = jest.fn(() => {
			return MockXHR(response);
		});

		$.ajax = jest.fn().mockImplementation(() => {
			const request = XMLHttpRequest();
			return Promise.all([response, 'error', request]);
		});

		return ajax.post(url).then(([result, status, request]) => {
			ajax.error($.Event(), request, request, 'error');
			$.ajax = oldAjax;
			window.XMLHttpRequest = oldXHR;
		});

	});
});
