/* global describe, jest, test, expect */
/**
 * MyAMS plugins tests
 */

import $ from "jquery";
import MyAMS, { init } from "../ext-base";

import { registry } from "../ext-registry";
import { i18n } from "../mod-i18n";
import myams_require from "../ext-require";


init($);

if (!MyAMS.i18n) {
	MyAMS.i18n = i18n;
	MyAMS.config.modules.push('i18n');
}
MyAMS.require = myams_require;


describe("MyAMS.ext-registry tests", () => {

	beforeEach(() => {
		registry.plugins.plugins.clear();
	});

	// Test MyAMS.registry.register
	test("Test MyAMS.registry.register function from props", () => {

		const callback = (element, context) => {
			$('.inner', element).addClass('modified');
		};
		const props = {
			name: 'MyAMS_test',
			callback: callback
		};
		const plugin = registry.register(props);
		expect(plugin).toBeInstanceOf(Object);
		expect(plugin.name).toBe('MyAMS_test');
		expect(plugin.src).toBe(undefined);
		expect(plugin.css).toBe(undefined);
		expect($.isArray(plugin.callbacks)).toBe(true);
		expect(plugin.async).toBe(true);
		expect(plugin.loaded).toBe(true);

		document.body.innerHTML = `<div>
			<div class="inner"></div>
		</div>`;
		const body = $(document.body);
		registry.run(body);
		expect($('.inner', body).hasClass('modified')).toBe(true);

		// cleanup
		registry.plugins.plugins.delete(plugin.name);
	});

	test("Test MyAMS.registry.register function from callable", () => {

		const callback = (element, context) => {
			$('.inner', element).addClass('modified');
		};
		const plugin = registry.register(callback, 'MyAMS_test');
		expect(plugin).toBeInstanceOf(Object);
		expect(plugin.name).toBe('MyAMS_test');

		document.body.innerHTML = `<div>
			<div class="inner"></div>
		</div>`;
		const body = $(document.body);
		registry.run(body);
		expect($('.inner', body).hasClass('modified')).toBe(true);

		// cleanup
		registry.plugins.plugins.delete(plugin.name);

	});

	test("Test MyAMS.registry.register function from callable name", () => {

		MyAMS.pluginCall = (element, context) => {
			$('.inner', element).addClass('modified');
		};
		const plugin = registry.register('MyAMS.pluginCall', 'MyAMS_test');
		expect(plugin).toBeInstanceOf(Object);
		expect(plugin.name).toBe('MyAMS_test');

		document.body.innerHTML = `<div>
			<div class="inner"></div>
		</div>`;
		const body = $(document.body);
		registry.run(body);
		expect($('.inner', body).hasClass('modified')).toBe(true);

		// cleanup
		registry.plugins.plugins.delete(plugin.name);
		delete MyAMS.pluginCall;

	});

	// Test MyAMS.registry.load
	test("Test MyAMS.registry.load from string definition", () => {

		MyAMS.pluginCall = (element, context) => {
			$('.inner', element).addClass('modified');
		};

		document.body.innerHTML = `<div>
			<div data-ams-plugins="MyAMS_test"
				 data-ams-plugin-MyAMS_test-callback="MyAMS.pluginCall">
				<div class="inner"></div>
			</div>
		</div>`;
		const body = $(document.body);

		// Load registry
		registry.initElement(body);
		const plugin = registry.plugins.plugins.get('MyAMS_test');
		expect(plugin).toBeInstanceOf(Object);
		expect(plugin.name).toBe('MyAMS_test');

		// Run registry
		registry.run(body);
		expect($('.inner', body).hasClass('modified')).toBe(true);

		// cleanup
		registry.plugins.plugins.delete(plugin.name);
		delete MyAMS.pluginCall;
	});

	test("Test MyAMS.registry.load from object definition", () => {

		MyAMS.pluginCall = (element, context) => {
			$('.inner', element).addClass('modified');
		};

		document.body.innerHTML = `<div>
			<div data-ams-plugins='{"name": "MyAMS_test", "callback": "MyAMS.pluginCall"}'>
				<div class="inner"></div>
			</div>
		</div>`;
		const body = $(document.body);

		// Load registry
		registry.initElement(body);
		const plugin = registry.plugins.plugins.get('MyAMS_test');
		expect(plugin).toBeInstanceOf(Object);
		expect(plugin.name).toBe('MyAMS_test');

		// Run registry
		registry.run(body);
		expect($('.inner', body).hasClass('modified')).toBe(true);

		// cleanup
		registry.plugins.plugins.delete(plugin.name);
		delete MyAMS.pluginCall;
	});

	test("Test MyAMS.registry.load from object definition with source", () => {

		const oldAjax = $.ajax;
		$.ajax = jest.fn().mockImplementation((settings) => {
			MyAMS.pluginCall = (element, context) => {
				$('.inner', element).addClass('modified');
			};
			return Promise.resolve();
		});

		document.body.innerHTML = `<div>
			<div data-ams-plugins='{
				"name": "MyAMS_test",
				"src": "resources/js/callback.js", 
				"callback": "MyAMS.pluginCall"
			}'>
				<div class="inner"></div>
			</div>
		</div>`;
		const body = $(document.body);

		// Load registry
		return registry.initElement(body).then(() => {
			const plugin = registry.plugins.plugins.get('MyAMS_test');
			expect(plugin).toBeInstanceOf(Object);
			expect(plugin.name).toBe('MyAMS_test');

			// Run registry
			registry.run(body);
			expect($('.inner', body).hasClass('modified')).toBe(true);

			// cleanup
			registry.plugins.plugins.delete(plugin.name);
			delete MyAMS.pluginCall;
		});
	});

	test("Test MyAMS.registry.load multiple objects definitions", () => {

		MyAMS.pluginCall = (element, context) => {
			$('.inner', element).addClass('modified');
		};

		document.body.innerHTML = `<div>
			<div data-ams-plugins='{"name": "MyAMS_test", "callback": "MyAMS.pluginCall"}'>
				<div class="inner"></div>
			</div>
			<div data-ams-plugins='{"name": "MyAMS_test", "callback": "MyAMS.pluginCall"}'>
				<div class="inner"></div>
			</div>
		</div>`;
		const body = $(document.body);

		// Load registry
		return registry.initElement(body).then(() => {
			const plugin = registry.plugins.plugins.get('MyAMS_test');
			expect(plugin).toBeInstanceOf(Object);
			expect(plugin.name).toBe('MyAMS_test');
			expect(plugin.callbacks.length).toBe(2);

			// Run registry
			registry.run(body);
			expect($('.inner', body).first().hasClass('modified')).toBe(true);
			expect($('.inner', body).last().hasClass('modified')).toBe(true);

			// cleanup
			registry.plugins.plugins.delete(plugin.name);
			delete MyAMS.pluginCall;
		});
	});

	test("Test MyAMS.registry.load from array definition", () => {

		MyAMS.pluginCall = (element) => {
			$('.inner', element).addClass('modified');
		};

		document.body.innerHTML = `<div>
			<div data-ams-plugins='[{"name": "MyAMS_test", "callback": "MyAMS.pluginCall"}]'>
				<div class="inner"></div>
			</div>
		</div>`;
		const body = $(document.body);

		// Load registry
		return registry.initElement(body).then(() => {
			const plugin = registry.plugins.plugins.get('MyAMS_test');
			expect(plugin).toBeInstanceOf(Object);
			expect(plugin.name).toBe('MyAMS_test');

			// Run registry
			registry.run(body);
			expect($('.inner', body).hasClass('modified')).toBe(true);

			// cleanup
			registry.plugins.plugins.delete(plugin.name);
			delete MyAMS.pluginCall;
		});
	});

	test("Test MyAMS.registry.load from array definition with same context", () => {

		MyAMS.pluginCall = (element) => {
			$('.inner', element).addClass('modified');
		};

		document.body.innerHTML = `<div>
			<div data-ams-plugins='[
				{"name": "MyAMS_test", "callback": "MyAMS.pluginCall"},
				{"name": "MyAMS_test", "callback": "MyAMS.pluginCall"}
			]'>
				<div class="inner"></div>
			</div>
		</div>`;
		const body = $(document.body);

		// Load registry
		return registry.initElement(body).then(() => {
			const plugin = registry.plugins.plugins.get('MyAMS_test');
			expect(plugin).toBeInstanceOf(Object);
			expect(plugin.name).toBe('MyAMS_test');

			// Run registry
			registry.run(body);
			expect($('.inner', body).hasClass('modified')).toBe(true);

			// cleanup
			registry.plugins.plugins.delete(plugin.name);
			delete MyAMS.pluginCall;
		});
	});

	test("Test MyAMS.registry async plug-ins", () => {

		const output = [];

		MyAMS.asyncCall = (element) => {
			output.push("Async callback");
		};
		MyAMS.syncCall = (element) => {
			output.push("Sync callback");
		};

		document.body.innerHTML = `<body>
			<div data-ams-plugins='[
				{"name": "MyAMS_sync", "callback": "MyAMS.syncCall", "async": "false"},
				{"name": "MyAMS_async", "callback": "MyAMS.asyncCall"}
			]'></div>
		</body>`;
		const body = $(document.body);

		// Load registry
		return registry.initElement(body).then(() => {
			const syncPlugin = registry.plugins.plugins.get('MyAMS_sync');
			expect(syncPlugin).toBeInstanceOf(Object);
			expect(syncPlugin.name).toBe('MyAMS_sync');
			const asyncPlugin = registry.plugins.plugins.get('MyAMS_async');
			expect(asyncPlugin).toBeInstanceOf(Object);
			expect(asyncPlugin.name).toBe('MyAMS_async');

			// Run registry
			registry.run(body);
			expect(output.length).toBe(2);

			// cleanup
			registry.plugins.plugins.delete(syncPlugin.name);
			registry.plugins.plugins.delete(asyncPlugin.name);
			delete MyAMS.syncCall;
			delete MyAMS.asyncCall;
		});
	});

	test("Test MyAMS.registry.load with disabled plug-ins", () => {

		MyAMS.pluginCall = (element, context) => {
			$('.inner', element).addClass('modified');
		};

		document.body.innerHTML = `<div>
			<div data-ams-plugins='{"name": "MyAMS_test", "callback": "MyAMS.pluginCall"}'
				 data-ams-plugins-disabled="MyAMS_test">
				<div class="inner"></div>
			</div>
		</div>`;
		const body = $(document.body);

		// Load registry
		return registry.initElement(body).then(() => {
			const plugin = registry.plugins.plugins.get('MyAMS_test');
			expect(plugin).toBeInstanceOf(Object);
			expect(plugin.name).toBe('MyAMS_test');

			// Run registry
			registry.run(body);
			expect($('.inner', body).hasClass('modified')).toBe(false);

			// cleanup
			registry.plugins.plugins.delete(plugin.name);
			delete MyAMS.pluginCall;
		});
	});

	test("Test MyAMS.registry.run with selected plug-ins", () => {

		MyAMS.pluginCall = (element, context) => {
			$('.inner', element).addClass('modified');
		};
		MyAMS.disabledCall = (element, context) => {
			$('.inner', element).addClass('notcalled');
		};

		document.body.innerHTML = `<div>
			<div data-ams-plugins='[
				{"name": "MyAMS_test", "callback": "MyAMS.pluginCall"},
				{"name": "MyAMS_disabled", "callback": "MyAMS.disabledCall"}
			]'>
				<div class="inner"></div>
			</div>
		</div>`;
		const body = $(document.body);

		// Load registry
		registry.initElement(body);
		const plugin = registry.plugins.plugins.get('MyAMS_test');
		expect(plugin).toBeInstanceOf(Object);
		expect(plugin.name).toBe('MyAMS_test');
		const disabled = registry.plugins.plugins.get('MyAMS_disabled');
		expect(disabled).toBeInstanceOf(Object);
		expect(disabled.name).toBe('MyAMS_disabled');

		// Run registry
		registry.run(body, ['MyAMS_test']);
		expect($('.inner', body).hasClass('modified')).toBe(true);
		expect($('.inner', body).hasClass('notcalled')).toBe(false);

		// cleanup
		registry.plugins.plugins.delete(plugin.name);
		registry.plugins.plugins.delete(disabled.name);
		delete MyAMS.pluginCall;
		delete MyAMS.disabledCall;

	});
});
