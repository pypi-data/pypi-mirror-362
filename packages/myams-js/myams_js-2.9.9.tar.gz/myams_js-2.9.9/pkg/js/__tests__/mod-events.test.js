/* global jest, test, expect */
/**
 * MyAMS events module tests
 */

import $ from "jquery";

import MyAMS, { init } from "../ext-base";
import { events } from "../mod-events";

import myams_require from "../ext-require";


jest.useFakeTimers();

init($);

if (!MyAMS.events) {
	MyAMS.events = events;
	MyAMS.config.modules.push('events');
}
MyAMS.require = myams_require;


MyAMS.events.init();

// Test with multiple initializations!
MyAMS.events.init();


// Test MyAMS.events
test("Test MyAMS.events for simple event", () => {

	MyAMS.testHandler = (evt) => {
		$(evt.target).addClass('modified');
	};

	document.body.innerHTML = `<div>
		<div class="inner"
			 data-ams-events-handlers='{
			 	"test.myams.event": "MyAMS.testHandler"
			 }'></div>
	</div>`;

	const body = $(document.body);

	MyAMS.events.initElement(body);
	$('.inner', body).trigger('test.myams.event');
	expect($('.inner', body).hasClass('modified')).toBe(true);
	delete MyAMS.testHandler;

});

test("Test MyAMS.events for event with options", () => {

	MyAMS.testHandler = (evt, options) => {
		$(evt.target).addClass(options.klass);
	};

	document.body.innerHTML = `<div>
		<div class="inner"
			 data-ams-events-handlers='{
			 	"test.myams.event": "MyAMS.testHandler"
			 }'
			 data-ams-events-options='{"klass": "modified"}'></div>
	</div>`;

	const body = $(document.body);

	MyAMS.events.initElement(body);
	$('.inner', body).trigger('test.myams.event');
	expect($('.inner', body).hasClass('modified')).toBe(true);
	delete MyAMS.testHandler;

});


// Test MyAMS.events getHandlers
test("Test MyAMS.events getHandlers", () => {

	document.body.innerHTML = `<div>
		<div class="inner"
			 data-ams-events-handlers='{
			 	"test.myams.event": "MyAMS.app.testHandler"
			 }'>
			 <div class="other"
			 	  data-ams-events-handlers='{
			 	  	"test.myams.event": "MyAMS.app.anotherHandler"
			 	  }'></div>
		</div>
	</div>`;

	const
		body = $(document.body),
		inner = $('.inner', body),
		handlers = MyAMS.events.getHandlers(inner, 'test.myams.event');
	expect(handlers.length).toBe(2);
	expect(handlers[0].hasClass('inner')).toBe(true);
	expect(handlers[1].hasClass('other')).toBe(true);

});


// Test MyAMS click handlers
test("Test MyAMS.handlers click handler", () => {

	document.body.innerHTML = `<div>
		<a href="#" data-ams-click-handler="MyAMS.test.clickHandler"
					data-ams-click-handler-options='{
						"source": "a",
						"value": "clickHandler"
					}'>
			Test link
		</a>
	</div>`;

	MyAMS.test = {
		clickHandler: (evt, options) => {
			$(evt.currentTarget).data('click-options', options);
		}
	}

	const link = $('a');

	link.trigger('click');
	const options = link.data('click-options');
	expect(options.source).toBe('a');
	expect(options.value).toBe('clickHandler');

	delete MyAMS.test;

});

test("Test MyAMS.handlers disabled click handler", () => {

	document.body.innerHTML = `<div>
		<a href="#" data-ams-disabled-handlers="click"
					data-ams-click-handler="MyAMS.test.clickHandler"
					data-ams-click-handler-options='{
						"source": "a",
						"value": "clickHandler"
					}'>
			Test link
		</a>
	</div>`;

	MyAMS.test = {
		clickHandler: (evt, options) => {
			$(evt.currentTarget).data('click-options', options);
		}
	};

	const link = $('a');
	link.trigger('click');
	const options = link.data('click-options');
	expect(options).toBe(undefined);

	delete MyAMS.test;

});


// Test MyAMS change handlers
test("Test MyAMS.handlers change handler on readonly input", () => {

	document.body.innerHTML = `<div>
		<form>
			<input type="text" 
				   data-ams-change-handler="MyAMS.test.changeHandler"
				   readonly />
		</form>
	</div>`;

	const
		form = $('form'),
		input = $('input', form);

	MyAMS.test = {
		changeHandler: (evt, options) => {
			form.data('changed', true);
		}
	};

	input.trigger('change');
	expect(form.data('changed')).toBe(undefined);

	delete MyAMS.test;

});

test("Test MyAMS.handlers change handler on standard input", () => {

	document.body.innerHTML = `<div>
		<form>
			<input type="text" 
				   data-ams-change-handler="MyAMS.test.changeHandler"
				   data-ams-change-handler-options='{
					   "source": "input",
					   "value": "changeHandler"
				   }'/>
		</form>
	</div>`;

	const
		form = $('form'),
		input = $('input', form);

	MyAMS.test = {
		changeHandler: (evt, options) => {
			form.data('changed', true);
			$(evt.target).data('change-options', options);
		}
	};

	input.trigger('change');
	expect(form.data('changed')).toBe(true);
	const options = input.data('change-options');
	expect(options.source).toBe('input');
	expect(options.value).toBe('changeHandler');

	delete MyAMS.test;

});

test("Test MyAMS.handlers disabled change handler on standard input", () => {

	document.body.innerHTML = `<div>
		<form>
			<input type="text" 
				   data-ams-disabled-handlers="all"
				   data-ams-change-handler="MyAMS.test.changeHandler"
				   data-ams-change-handler-options='{
					   "source": "input",
					   "value": "changeHandler"
				   }'/>
		</form>
	</div>`;

	const
		form = $('form'),
		input = $('input', form);

	MyAMS.test = {
		changeHandler: (evt, options) => {
			form.data('changed', true);
			$(source).data('change-options', options);
		}
	};

	input.trigger('change');
	expect(form.data('changed')).toBe(undefined);
	const options = input.data('change-options');
	expect(options).toBe(undefined);

	delete MyAMS.test;

});


// Test MyAMS.handlers click events
test("Test MyAMS.handlers click events generator", () => {

	document.body.innerHTML = `<div>
		<a href="#" 
		   data-ams-click-event="test.myams.click"
		   data-ams-click-event-options='{
			"source": "a",
			"value": "clickEvent"
		   }'>
		   Link
		</a>
	</div>`;

	MyAMS.test = {
		clickHandler: (evt, options) => {
			$(evt.target).data('click-data', options);
		}
	};

	$(document).on('test.myams.click', MyAMS.test.clickHandler);

	const link = $('a');
	link.trigger('click');

	const options = link.data('click-data');
	expect(options.source).toBe('a');
	expect(options.value).toBe('clickEvent');

	delete MyAMS.test;

});


// Test click on readonly checkbox
test("Test MyAMS.handlers click on checkbox", () => {

	document.body.innerHTML = `<div>
		<input type="checkbox" />
	</div>`;

	$('input').trigger('click');
	expect($('input:checked').length).toBe(1);

});

test("Test MyAMS.handlers click on readony checkbox", () => {

	document.body.innerHTML = `<div>
		<input type="checkbox" readonly />
	</div>`;

	$('input').trigger('click');

});
