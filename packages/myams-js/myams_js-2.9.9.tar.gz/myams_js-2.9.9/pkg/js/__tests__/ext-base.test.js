/* global jest, test, expect */

/**
 * MyAMS base package tests
 */

import $ from "jquery";

import MyAMS, {
	executeFunctionByName,
	generateId,
	generateUUID,
	getFunctionByName,
	getObject,
	getQueryVar,
	getSource,
	getModules,
	getScript,
	switchIcon,
	init,
	initData,
	clearContent,
	initContent
} from '../ext-base';
import { events } from "../mod-events";
import myams_require from "../ext-require";
import { registry } from "../ext-registry";


// Initialize MyAMS
init($);

if (!MyAMS.events) {
	MyAMS.events = events;
	MyAMS.config.modules.push('events');
}


// Test String protoype functions
test("Test String.camelCase function", () => {

	expect(''.camelCase()).toBe('');
	expect('a'.camelCase()).toBe('a');
	expect('this-is-a-name'.camelCase()).toBe('thisIsAName');
	expect('This-Is-A-Name'.camelCase()).toBe('ThisIsAName');

});

test("Test String.deCase function", () => {

	expect(''.deCase()).toBe('');
	expect('a'.deCase()).toBe('a');
	expect('thisIsCamelCase'.deCase()).toBe('this-is-camel-case');
	expect('ThisIsCamelCase'.deCase()).toBe('-this-is-camel-case');

});

test("Test String.initLowerCase function", () => {

	expect(''.initLowerCase()).toBe('');
	expect('a'.initLowerCase()).toBe('a');
	expect('A'.initLowerCase()).toBe('a');
	expect('UpCase'.initLowerCase()).toBe('upCase');
	expect('lowcase'.initLowerCase()).toBe('lowcase');
});

test("Test String.unserialize function", () => {

	expect(''.unserialize()).toBe('');

	const obj1 = 'a=1'.unserialize();
	expect(obj1.a).toBe('1');

	const obj2 = 'a=1&b=two'.unserialize();
	expect(obj2.a).toBe('1');
	expect(obj2.b).toBe('two');

	const obj3 = 'a=1&b=two&b=three'.unserialize();
	expect(obj3.a).toBe('1');
	expect(obj3.b).toBe('three');

});


// Text JQuery $ extensions
test("Test JQuery extendPrefix function", () => {

	let source = { amsFormData: true, amsFormOtherData: false, amsOtherData: false };
	let target = {};
	$.extendPrefix(target, 'amsForm', null, source);
	expect(Object.keys(target).length).toBe(2);
	expect(target.data).toBe(true);
	expect(target.otherData).toBe(false);

});

test("Test JQuery extendOnly function", () => {

	let source = { amsFormData: false };
	let target = { amsFormData: true, amsOtherData: false };
	$.extendOnly(source, null, target);
	expect(Object.keys(source).length).toBe(1);
	expect(source.amsFormData).toBe(true);

});


// Test JQuery $.fn.exists
test("Test JQuery exists function", () => {

	const tag = $('<div><a href="."></a></div>');

	expect($('a', tag).exists()).toBe(true);
	expect($('p', tag).exists()).toBe(false);

});


// Test JQuery $.fn.objectOrParentWithClass
test("Test JQuery objectOrParentWithClass function", () => {

	const tag = $('<body><div class="parent"><p class="child"><span class="span"></span></p></div>');

	const missing = $('.span', tag).objectOrParentWithClass('missing');
	expect(missing.length).toBe(0);

	const span = $('.span', tag).objectOrParentWithClass('span');
	expect(span.length).toBe(1);
	expect(span[0].tagName).toBe('SPAN');

	const p = $('.span', tag).objectOrParentWithClass('child');
	expect(p.length).toBe(1);
	expect(p[0].tagName).toBe('P');

	const div = $('.span', tag).objectOrParentWithClass('parent');
	expect(div.length).toBe(1);
	expect(div[0].tagName).toBe('DIV');

});


// Test JQuery $.fn.listattr
test("Test JQuery listattr function", () => {

	const tag = $('<body>' +
		'<select class="select" multiple>' +
		'<option value="1" selected>' +
		'<option value="2">' +
		'<option value="3" selected>' +
		'</select>' +
		'</body>');

	const selected = $('option:selected', tag).listattr('value');
	expect(selected).toBeInstanceOf(Array);
	expect(selected.length).toBe(2);
	expect(selected[0]).toBe('1');
	expect(selected[1]).toBe('3');

});


// Test JQuery $.fn.style
test("Test JQuery style function", () => {

	const tag = $('<body>' +
		'<div class="div">' +
		'<span></span>' +
		'</div>' +
		'</body>');

	const span = $('span', tag).style("border", "1px solid red", 1);
	expect(span.length).toBe(1);
	expect(span.get(0).style.getPropertyValue('border')).toBe('1px solid red');
	expect(span.style('border')).toBe('1px solid red');

	const style = span.style();
	expect(style._importants.border).toBe(1);

	const p = $('p', tag);
	expect(p.length).toBe(0);
	expect(p.style().length).toBe(0);

});


// Test JQuery $.fn.removeClassPrefix
test("Test JQuery removeClassPrefix function", () => {

	const tag = $('<body>' +
		'<div><div class="class-1 class-2 other-1"></div></div>' +
		'</body>');

	const div = $('.class-1', tag).removeClassPrefix('class-');
	expect(div.length).toBe(1);
	expect(div.get(0).className).toBe('other-1');

});


// Test MyAMS getModules
test("Test MyAMS getModules base function", () => {

	document.body.innerHTML = `<html>
		<body>
			<div class="inner" data-ams-modules="app">
				<div class="other"
					 data-ams-modules='{"other": "resources/js/script.js"}'>
					 <p>This is just a paragraph.</p>
				</div>
			</div>
		</body>
	</html>`;
	const body = $('body');
	const modules = getModules(body);
	expect($.isArray(modules)).toBe(true);
	expect(modules.length).toBe(2);
	expect(modules[0]).toBe('app');
	expect(modules[1]).toBeInstanceOf(Object);
	expect(modules[1].other).toBe('resources/js/script.js');

});

test("Test MyAMS getModules with multiple names", () => {

	document.body.innerHTML = `<div>
		<div class="inner" data-ams-modules="app i18n">
			<div class="other">
				 <p>This is just a paragraph.</p>
			</div>
		</div>
	</div>`;
	const body = $('body');
	const modules = getModules(body);
	expect($.isArray(modules)).toBe(true);
	expect(modules.length).toBe(2);
	expect(modules[0]).toBe('app');
	expect(modules[1]).toBe('i18n');

});

test("Test MyAMS getModules from body with object definition", () => {

	document.body.innerHTML = `<div data-ams-modules='{
		"app": "resources/js/app.js"
	}'>
		<div class="inner">
			<div class="other">
				 <p>This is just a paragraph.</p>
			</div>
		</div>
	</div>`;
	const div = $('body > div');
	const modules = getModules(div);
	expect($.isArray(modules)).toBe(true);
	expect(modules.length).toBe(1);
	expect(modules[0]).toBeInstanceOf(Object);
	expect(modules[0].app).toBe('resources/js/app.js');

});

test("Test MyAMS getModules from body with multiple names", () => {

	document.body.innerHTML = `<div data-ams-modules="app i18n">
		<div class="inner">
			<div class="other">
				 <p>This is just a paragraph.</p>
			</div>
		</div>
	</div>`;
	const div = $('body > div');
	const modules = getModules(div);
	expect($.isArray(modules)).toBe(true);
	expect(modules.length).toBe(2);
	expect(modules[0]).toBe('app');
	expect(modules[1]).toBe('i18n');

});


// Test MyAMS getObject
test("Test MyAMS getObject function", () => {

	const
		name1 = 'window.location.href',
		name2 = 'window.undefined',
		name3 = 'missing.undefined';

	expect(typeof getObject).toBe('function');
	expect(getObject(undefined)).toBe(undefined);
	expect(getObject('')).toBe(undefined);
	expect(getObject(123)).toBe(123);
	expect(getObject(name1)).toBe('http://localhost/');
	expect(getObject(name2)).toBe(undefined);
	expect(getObject(name3)).toBe(undefined);

});


// Test MyAMS getFunctionByName
test("Test MyAMS getFunctionByName function", () => {

	const
		name = 'MyAMS.$.fn.removeClassPrefix',
		func = getFunctionByName(name);

	expect(typeof(func)).toBe('function');
	expect(getFunctionByName(func)).toBe(func);
	expect(getFunctionByName()).toBe(undefined);
	expect(getFunctionByName(1)).toBe(undefined);
	expect(getFunctionByName(false)).toBe(undefined);
	expect(getFunctionByName([])).toBe(undefined);
	expect(getFunctionByName({})).toBe(undefined);
	expect(getFunctionByName('MyAMS.env.missing')).toBe(undefined);
	expect(getFunctionByName('MyAMS.missing.missing')).toBe(undefined);
	expect(getFunctionByName('missing.missing.missing')).toBe(undefined);

});


// Test MyAMS executeFunctionByName
test("Test MyAMS executeFunctionByName function", () => {

	MyAMS.test = {
		testFunction: function(arg1, arg2) {
			return [arg1, arg2];
		}
	};

	const
		name = 'MyAMS.test.testFunction',
		result = executeFunctionByName(name, MyAMS, 'value 1', 'value 2');

	expect(result).toBeInstanceOf(Array);
	expect(result[0]).toBe('value 1');
	expect(result[1]).toBe('value 2');

	delete MyAMS.test;

});


// Test MyAMS getSource
test("Test MyAMS getSource function", () => {

	const url = getSource("http://example.com/{MyAMS.env.baseURL}myams_js/test{MyAMS.env.devext}.js");

	expect(url).toBe('http://example.com//myams_js/test-dev.js');

});


// Test MyAMS getScript
test("Test MyAMS getScript function", () => {

	const url = 'resources/test.js';
	$.ajax = jest.fn().mockImplementation(() => {
		return Promise.resolve(url);
	});
	return getScript(url).then(result => {
		expect(result).toBe(url);
	})
});


// Test MyAMS getQueryVar
test("Test MyAMS getQueryVar function", () => {

	const
		url1 = null,
		url2 = '',
		url3 = {},
		url4 = 'http://localhost/',
		url5 = 'http://localhost/api?',
		url6 = 'http://localhost/api?param1',
		url7 = 'http://localhost/api?param1=value1',
		url8 = 'http://localhost/api?param1=value1&',
		url9 = 'http://localhost/api?param1=value1&param2=value2',
		url10 = 'http://localhost/api?param1=value1&param1=value2';

	expect(getQueryVar(url1, 'param1')).toBe(undefined);
	expect(getQueryVar(url2, 'param1')).toBe(undefined);
	expect(getQueryVar(url3, 'param1')).toBe(undefined);
	expect(getQueryVar(url4, 'param1')).toBe(undefined);
	expect(getQueryVar(url5, 'param1')).toBe(null);
	expect(getQueryVar(url6, 'param1')).toBe(null);
	expect(getQueryVar(url7, 'param1')).toBe('value1');
	expect(getQueryVar(url8, 'param1')).toBe('value1');
	expect(getQueryVar(url9, 'param1')).toBe('value1');
	expect(getQueryVar(url10, 'param1')).toBe('value1');

});


// Test MyAMS generateId
test("Test MyAMS generateId function", () => {

	const id = generateId();

	expect(typeof id).toBe('string');
	expect(id.length).toBe(16);

});

// Test MyAMS generateUUID
test("Test MyAMS generateUUID function", () => {

	const id = generateUUID();

	expect(typeof id).toBe('string');
	expect(id.length).toBe(36);
	expect(/[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[a-f0-9]{4}-[a-f0-9]{12}/.test(id)).toBe(true);

});


// Test MyAMS switchIcon
test("Test MyAMS switchIcon function", () => {

	const element = $('<i class="fa fa-open"></i>');
	switchIcon(element, 'open', 'close');
	expect(element.hasClass('fa-close')).toBe(true);

	document.body.innerHTML = `<div>
		<i id="testIcon" class="fa fa-cog"></i>
	</div>`;

	const
		body = $(document.body),
		icon = $('#testIcon', body);
	switchIcon('#testIcon', 'cog', 'spin');
	expect(icon.exists()).toBe(true);
	expect(icon.hasClass('fa-spin')).toBe(true);

});


// Test MyAMS initData
test("Test MyAMS initData function", () => {

	const tag = $(`<div class="parent"><p data-ams-data='{"ams-field1": "value1"}'>Data block</p></div>`);

	const element = $(tag);
	initData(element);

	const p = $('p', element);
	expect(p.attr('data-ams-field1')).toBe('value1');

});


	// Test MyAMS initContent
test("Test MyAMS initContent function", () => {

	document.body.innerHTML = `<div>
		<div class="inner"></div>
	</div>`;
	MyAMS.require = myams_require;
	MyAMS.config.useRegistry = false;
	let beforeInitEvent = false;
	$(document).on('before-init.ams.content', () => {
		beforeInitEvent = true;
	});
	let afterInitEvent = false;
	$(document).on('after-init.ams.content', () => {
		afterInitEvent = true;
	});
	const body = $(document.body);
	return initContent(body).then(() => {
		expect(beforeInitEvent).toBe(true);
		expect(afterInitEvent).toBe(false);
		$(document).off('.ams');
	});
});


// Test MyAMS clearContent
test("Test MyAMS clearContent function with events", () => {

	document.body.innerHTML = `<div class="body">
		<div class="inner"></div>
	</div>`;
	let clearEvent = false;
	$(document).on('clear.ams.content', () => {
		clearEvent = true;
	});
	let clearedEvent = false;
	$(document).on('cleared.ams.content', () => {
		clearedEvent = true;
	});
	return clearContent('.body').then((status) => {
		expect(status).toBe(true);
		expect(clearEvent).toBe(true);
		expect(clearedEvent).toBe(true);
		$(document).off('.ams');
	});

});

test("Test MyAMS clearContent function veto", () => {

	document.body.innerHTML = `<div>
		<div class="inner"></div>
	</div>`;
	let clearEvent = false;
	$(document).on('clear.ams.content', (evt, veto) => {
		veto.veto = true;
		clearEvent = true;
	});
	let clearedEvent = false;
	$(document).on('cleared.ams.content', () => {
		clearedEvent = true;
	})
	const body = $(document.body);
	clearContent(body).then((status) => {
		expect(status).toBe(false);
		expect(clearEvent).toBe(true);
		expect(clearedEvent).toBe(false);
		$(document).off('.ams');
	});

});

test("Test MyAMS clearContent function with inner events handlers", () => {

	document.body.innerHTML = `<div>
		<div class="inner"
			 data-ams-events-handlers='{
			 	"clear.ams.content": "MyAMS.app.clearHandler",
			 	"cleared.ams.content": "MyAMS.app.clearedHandler"
			 }'></div>
	</div>`;

	let clearEvent = false,
		clearedEvent = false;
	MyAMS.app = {
		clearHandler: (evt) => {
			$(evt.target).data('clearing', true);
			clearEvent = true;
		},
		clearedHandler: (evt) => {
			$(evt.target).data('cleared', true);
			clearedEvent = true;
		}
	}
	const
		body = $(document.body),
		inner = $('.inner', body);

	MyAMS.events.initElement(body);
	return clearContent(body).then((status) => {
		expect(status).toBe(true);
		expect(clearEvent).toBe(true);
		expect(inner.data('clearing')).toBe(true);
		expect(clearedEvent).toBe(true);
		expect(inner.data('cleared')).toBe(true);

		delete MyAMS.app;
	});

});

test("Test MyAMS clearContent function with inner events handlers and veto", () => {

	document.body.innerHTML = `<div>
		<div class="inner"
			 data-ams-events-handlers='{
			 	"clear.ams.content": "MyAMS.app.clearHandler",
			 	"cleared.ams.content": "MyAMS.app.clearedHandler"
			 }'></div>
	</div>`;

	let clearEvent = false,
		clearedEvent = false;
	MyAMS.app = {
		clearHandler: (evt, veto) => {
			$(evt.target).data('clearing', true);
			clearEvent = true;
			veto.veto = true;
		},
		clearedHandler: (evt) => {
			$(evt.target).data('cleared', true);
			clearedEvent = true;
		}
	}
	const
		body = $(document.body),
		inner = $('.inner', body);

	MyAMS.events.initElement(body);
	return clearContent(body).then((status) => {
		expect(status).toBe(false);
		expect(clearEvent).toBe(true);
		expect(inner.data('clearing')).toBe(true);
		expect(clearedEvent).toBe(false);
		expect(inner.data('cleared')).toBeUndefined();

		delete MyAMS.app;
	});

});


// Test base MyAMS structure
test("Test MyAMS base structure", () => {

	expect(window.MyAMS).toBeInstanceOf(Object);
	expect(MyAMS.$).toBeInstanceOf(Object);
	expect(MyAMS.env).toBeInstanceOf(Object);
	expect(MyAMS.env.bundle).toBe(true);
	expect(MyAMS.env.devmode).toBe(true);
	expect(MyAMS.env.devext).toBe('-dev');
	expect(MyAMS.env.baseURL).toBe('/');
	expect(MyAMS.config).toBeInstanceOf(Object);
	expect(MyAMS.core).toBeInstanceOf(Object);
	expect(MyAMS.core.getObject).toBeInstanceOf(Function);
	expect(MyAMS.theme).toBe("unknown");

});
