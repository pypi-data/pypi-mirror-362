/* global test, expect */
/*
 * MyAMS modal module tests
 */

import $ from "jquery";

import MyAMS, { init } from "../ext-base";
import { events } from "../mod-events";
import { form } from "../mod-form";
import { i18n } from "../mod-i18n";

import {
	modal,
	modalToggleEventHandler,
	modalDismissEventHandler,
	dynamicModalShownEventHandler
} from "../mod-modal";

import myams_require from "../ext-require";

const bs = require("bootstrap");
// Bootstrap modals are required
$.fn.modal = bs.Modal._jQueryInterface;
$.fn.modal.Constructor = bs.Modal;


init($);

if (!MyAMS.modal) {
	MyAMS.modal = modal;
	MyAMS.config.modules.push('modal');
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
MyAMS.require = myams_require;


// Test MyAMS.modal initialization
test("Test MyAMS.modal module initialization", () => {

	document.body.innerHTML = `<div>
		<div id="modaltest" class="modal">
			<div class="modal-dialog">
				<button id="hide-modal" type="button" data-dismiss="modal">
					<i class="fa fa-times"></i>
				</button>
				<p>Modal content</p>
			</div>
		</div>
		<a id="open-modal" href="#modaltest" data-toggle="modal" 
		   data-ams-stop-propagation="true"></a>
	</div>`;

	const
		body = $(document.body),
		modal = $('.modal', body),
		link = $('#open-modal', body);

	MyAMS.modal.init();

	return MyAMS.modal.open(link).then(() => {
		expect(modal.exists()).toBe(true);
		expect(modal.hasClass('show')).toBe(true);
		expect(modal.css('z-index')).toBe('1100');
	});

});

test("Test MyAMS.modal with click handler", () => {

	document.body.innerHTML = `<div>
		<div id="modaltest" class="modal">
			<div class="modal-dialog">
				<button id="hide-modal" type="button" data-dismiss="modal">
					<i class="fa fa-times"></i>
				</button>
				<p>Modal content</p>
			</div>
		</div>
		<a id="open-modal" href="#modaltest" data-toggle="modal"></a>
	</div>`;

	const body = $(document.body);
	MyAMS.modal.init();

	$('#open-modal', body).click();

});

test("Test MyAMS.modal on disabled click handler", () => {

	document.body.innerHTML = `<div>
		<div id="modaltest" class="modal">
			<div class="modal-dialog">
				<button id="hide-modal" type="button" data-dismiss="modal">
					<i class="fa fa-times"></i>
				</button>
				<p>Modal content</p>
			</div>
		</div>
		<a id="open-modal" href="#modaltest" data-toggle="modal" 
		   data-ams-disabled-handlers="click"></a>
	</div>`;

	const body = $(document.body);
	MyAMS.modal.init();

	$('#open-modal', body).click();

});


// Test MyAMS.modal toggle handler
test("Test MyAMS.modal toggle handler", () => {

	document.body.innerHTML = `<div>
		<div id="modaltest" class="modal">
			<div class="modal-dialog">
				<button id="hide-modal" type="button" data-dismiss="modal">
					<i class="fa fa-times"></i>
				</button>
				<p>Modal content</p>
			</div>
		</div>
		<a id="open-modal" href="#modaltest" 
		   data-toggle="modal" data-ams-stop-propagation="true"></a>
	</div>`;

	const
		body = $(document.body),
		modal = $('.modal', body),
		link = $('#open-modal', body);
	MyAMS.modal.init();
	return modalToggleEventHandler({
		currentTarget: link,
		preventDefault: () => {
			link.data('prevented', true);
		},
		stopPropagation: () => {
			link.data('stopped', true);
		}
	}).then(() => {
		expect(modal.hasClass('show')).toBe(true);
		expect(link.data('prevented')).toBe(true);
		expect(link.data('stopped')).toBe(true);
	});

});

test("Test MyAMS.modal disabled button", () => {

	document.body.innerHTML = `<div>
		<div id="modaltest" class="modal">
			<div class="modal-dialog">
				<button id="hide-modal" type="button" data-dismiss="modal">
					<i class="fa fa-times"></i>
				</button>
				<p>Modal content</p>
			</div>
		</div>
		<a id="open-modal" href="#modaltest"
		   data-toggle="modal" disabled></a>
	</div>`;

	const
		body = $(document.body),
		modal = $('.modal', body),
		link = $('#open-modal', body);
	MyAMS.modal.init();
	return modalToggleEventHandler({
		currentTarget: link,
		preventDefault: () => {
			link.data('prevented', true);
		},
		stopPropagation: () => {
			link.data('stopped', true);
		}
	}).then(() => {
		expect(modal.hasClass('show')).toBe(false);
		expect(link.data('prevented')).toBe(undefined);
		expect(link.data('stopped')).toBe(undefined);
	});

});

test("Test MyAMS.modal disabled toggle handler", () => {

	document.body.innerHTML = `<div>
		<div id="modaltest" class="modal">
			<div class="modal-dialog">
				<button id="hide-modal" type="button" data-dismiss="modal">
					<i class="fa fa-times"></i>
				</button>
				<p>Modal content</p>
			</div>
		</div>
		<a id="open-modal" href="#modaltest" 
		   data-toggle="modal" data-ams-stop-propagation="true"
		   data-ams-disabled-handlers="click"></a>
	</div>`;

	const
		body = $(document.body),
		modal = $('.modal', body),
		link = $('#open-modal', body);
	MyAMS.modal.init();
	return modalToggleEventHandler({
		currentTarget: link,
		preventDefault: () => {
			link.data('prevented', true);
		},
		stopPropagation: () => {
			link.data('stopped', true);
		}
	}).then(() => {
		expect(modal.hasClass('show')).toBe(false);
		expect(link.data('prevented')).toBe(undefined);
		expect(link.data('stopped')).toBe(undefined);
	});

});

test("Test MyAMS.modal toggle handler from context menu", () => {

	document.body.innerHTML = `<div>
		<div id="modaltest" class="modal">
			<div class="modal-dialog">
				<button id="hide-modal" type="button" data-dismiss="modal">
					<i class="fa fa-times"></i>
				</button>
				<p>Modal content</p>
			</div>
		</div>
		<a id="open-modal" href="#modaltest" 
		   data-toggle="modal" data-ams-context-menu="true"></a>
	</div>`;

	const
		body = $(document.body),
		modal = $('.modal', body),
		link = $('#open-modal', body);
	MyAMS.modal.init();
	return modalToggleEventHandler({
		currentTarget: link,
		preventDefault: () => {
			link.data('prevented', true);
		},
		stopPropagation: () => {
			link.data('stopped', true);
		}
	}).then(() => {
		expect(modal.hasClass('show')).toBe(false);
		expect(link.data('prevented')).toBe(undefined);
		expect(link.data('stopped')).toBe(undefined);
	});

});


// Test MyAMS.modal open function
test("Test MyAMS.modal open function with function target", () => {

	document.body.innerHTML = `<div>
		<div id="modaltest" class="modal">
			<div class="modal-dialog">
				<button id="hide-modal" type="button" data-dismiss="modal">
					<i class="fa fa-times"></i>
				</button>
				<p>Modal content</p>
			</div>
		</div>
		<a id="open-modal" data-ams-url="MyAMS.test.getURL" 
		   data-toggle="modal" data-ams-context-menu="true"></a>
	</div>`;

	MyAMS.test = {
		getURL: () => {
			return "#modaltest";
		}
	};

	const
		body = $(document.body),
		modal = $('#modaltest', body),
		link = $('#open-modal', body);
	MyAMS.modal.init();
	return MyAMS.modal.open(link).then(() => {
		expect(modal.hasClass('show')).toBe(true);
		delete MyAMS.test;
	});

});


// Test MyAMS.modal show function
test("Test MyAMS.modal show function", () => {

	document.body.innerHTML = `<div>
		<div id="modaltest" class="modal" data-ams-shown-handler="MyAMS.test.initContent">
			<div class="modal-dialog">
				<button id="hide-modal" type="button" data-dismiss="modal">
					<i class="fa fa-times"></i>
				</button>
				<p>Modal content</p>
			</div>
		</div>
		<a id="open-modal" data-toggle="modal" href="#modaltest"></a>
	</div>`;

	MyAMS.test = {
		initContent: (evt) => {
			return new Promise((resolve, reject) => {
				const modal = $(evt.target);
				modal.data('init-done', true);
				resolve();
			});
		}
	}
	const
		body = $(document.body),
		modal = $('#modaltest', body),
		button = $('#open-modal', body);
	MyAMS.modal.init();
	button.click();
	return dynamicModalShownEventHandler($.Event('click', {
		target: modal
	})).then(() => {
		expect(modal.data('init-done')).toBe(true);
	});

});


// Test MyAMS.modal dismiss handler
test("Test MyAMS.modal dismiss handler", () => {

	document.body.innerHTML = `<div>
		<div id="modaltest" class="modal">
			<div class="modal-dialog">
				<button id="hide-modal" type="button" data-dismiss="modal">
					<i class="fa fa-times"></i>
				</button>
				<p>Modal content</p>
			</div>
		</div>
		<a id="open-modal" href="#modaltest" 
		   data-toggle="modal" data-ams-context-menu="true"></a>
	</div>`;

	const
		body = $(document.body),
		modal = $('.modal', body),
		link = $('#hide-modal', body);
	MyAMS.modal.init();

	return modalDismissEventHandler({
		currentTarget: link
	}).then(() => {
		expect(modal.hasClass('show')).toBe(false);
	});

});


// Test MyAMS.modal events handlers
test("Test MyAMS.modal events handlers", () => {

	document.body.innerHTML = `<div>
		<div id="modaltest" class="modal"
			 data-ams-events-handlers='{"shown.bs.modal": "MyAMS.test.shownCallback"}'>
			<div class="modal-dialog">
				<button id="hide-modal" type="button" data-dismiss="modal">
					<i class="fa fa-times"></i>
				</button>
				<p>Modal content</p>
			</div>
		</div>
		<a id="open-modal" href="#modaltest" data-toggle="modal"></a>
	</div>`;

	const body = $(document.body);
	MyAMS.modal.init();
	MyAMS.events.initElement(body);
	MyAMS.test = {
		shownCallback: (evt) => {
			$(evt.currentTarget).data('ams.shown', true);
		}
	}
	const link = $('#open-modal', body);
	return MyAMS.modal.open(link).then(() => {
		expect($('.modal').data('ams.shown')).toBe(true);
		delete MyAMS.test;
	});

});


// Test MyAMS.modal close function
test("Test MyAMS.modal close function", () => {

	document.body.innerHTML = `<div>
		<div id="modaltest" class="modal">
			<div class="modal-dialog">
				<button id="hide-modal" type="button" data-dismiss="modal">
					<i class="fa fa-times"></i>
				</button>
				<p>Modal content</p>
			</div>
		</div>
		<a id="open-modal" href="#modaltest" data-toggle="modal"></a>
	</div>`;

	const body = $(document.body);
	MyAMS.modal.init();
	const link = $('#open-modal', body);
	return MyAMS.modal.open(link).then(() => {
		expect($('.modal').hasClass('show')).toBe(true);
		MyAMS.modal.close();
		expect($('.modal').hasClass('show')).toBe(false);
	});

});

test("Test MyAMS.modal close function with element", () => {

	document.body.innerHTML = `<div>
		<div id="modaltest" class="modal">
			<div class="modal-dialog">
				<button id="hide-modal" type="button" data-dismiss="modal">
					<i class="fa fa-times"></i>
				</button>
				<p>Modal content</p>
			</div>
		</div>
		<a id="open-modal" href="#modaltest" data-toggle="modal"></a>
	</div>`;

	const body = $(document.body);
	MyAMS.modal.init();
	const link = $('#open-modal', body);
	return MyAMS.modal.open(link).then(() => {
		expect($('.modal').hasClass('show')).toBe(true);
		MyAMS.modal.close('#modaltest');
		expect($('.modal').hasClass('show')).toBe(false);
	});

});


// Test MyAMS.modal stacked modals
test("Test MyAMS.modal stacked modals (first step!)", () => {

	document.body.innerHTML = `<div>
		<div id="modal1" class="modal">
			<div class="modal-dialog">
				<button id="hide-modal1" type="button" data-dismiss="modal">
					<i class="fa fa-times"></i>
				</button>
				<p>Modal content</p>
				<a id="open-modal2" href="#modal2" data-toggle="modal"></a>
			</div>
		</div>
		<a id="open-modal1" href="#modal1" data-toggle="modal"></a>
		<div id="modal2" class="modal">
			<div class="modal-dialog">
				<button id="hide-modal2" type="button" data-dismiss="modal">
					<i class="fa fa-times"></i>
				</button>
				<p>Modal content</p>
			</div>
		</div>
	</div>`;

	const body = $(document.body);
	MyAMS.modal.init();
	const link = $('#open-modal1', body);
	return MyAMS.modal.open(link).then(() => {
		expect($('#modal1').hasClass('show')).toBe(true);
		expect($('#modal2').hasClass('show')).toBe(false);
		MyAMS.modal.close('#modal1');
		expect($('.modal1').hasClass('show')).toBe(false);
	});

});

test("Test MyAMS.modal stacked modals (second step!)", () => {

	document.body.innerHTML = `<div>
		<div id="modal1" class="modal show" style="display: block; z-index: 1100;">
			<div class="modal-dialog">
				<button id="hide-modal1" type="button" data-dismiss="modal">
					<i class="fa fa-times"></i>
				</button>
				<p>Modal content</p>
				<a id="open-modal2" href="#modal2" data-toggle="modal"></a>
			</div>
		</div>
		<a id="open-modal1" href="#modal1" data-toggle="modal"></a>
		<div id="modal2" class="modal">
			<div class="modal-dialog">
				<button id="hide-modal2" type="button" data-dismiss="modal">
					<i class="fa fa-times"></i>
				</button>
				<p>Modal content</p>
			</div>
		</div>
	</div>`;

	const body = $(document.body);
	MyAMS.modal.init();
	const link = $('#open-modal2', body);
	return MyAMS.modal.open(link).then(() => {
		expect($('#modal1').hasClass('show')).toBe(true);
		expect($('#modal2').hasClass('show')).toBe(true);
		expect($('#modal2').css('z-index')).toBe('1100');  // testing only!!!
		MyAMS.modal.close('#modal2');
		expect($('#modal2').hasClass('show')).toBe(false);
		expect($('#modal1').hasClass('show')).toBe(true);
	});

});
