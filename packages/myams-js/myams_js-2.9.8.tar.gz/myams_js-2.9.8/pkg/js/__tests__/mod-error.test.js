/**
 * MyAMS error module tests
 */

import $ from "jquery";

import MyAMS, { init } from "../ext-base";
import { ajax } from "../mod-ajax";
import { alert } from "../mod-alert";
import { error } from "../mod-error";
import { form } from "../mod-form";
import { i18n } from "../mod-i18n";

import myams_require from "../ext-require";


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
if (!MyAMS.error) {
	MyAMS.error = error;
	MyAMS.config.modules.push('error');
}
if (!MyAMS.form) {
	MyAMS.form = form;
	MyAMS.config.modules.push('form');
}
MyAMS.require = myams_require;


// Test MyAMS.error.showErrors
test("Test MyAMS.error.showErrors function for error string", () => {

	document.body.innerHTML = `<div>
		<div class="parent"></div>
	</div>`;

	const
		body = $(document.body),
		parent = $('.parent', body);
	expect(parent.exists()).toBe(true);
	return error.showErrors(parent, "Error message").then(() => {
		const alertDiv = $('.alert', parent);
		expect(alertDiv.exists()).toBe(true);
		expect(alertDiv.hasClass('alert-danger')).toBe(true);
		expect($('.alert-heading', alertDiv).text()).toBe(MyAMS.i18n.ERROR_OCCURED);
		expect($('li', alertDiv).text()).toBe('Error message');
	});

});

test("Test MyAMS.error.showErrors function for errors strings array", () => {

	document.body.innerHTML = `<div>
		<div class="parent"></div>
	</div>`;

	const
		body = $(document.body),
		parent = $('.parent', body);
	expect(parent.exists()).toBe(true);
	return error.showErrors(parent, ["Error message 1", "Error message 2"]).then(() => {
		const alertDiv = $('.alert', parent);
		expect(alertDiv.exists()).toBe(true);
		expect(alertDiv.hasClass('alert-danger')).toBe(true);
		expect($('.alert-heading', alertDiv).text()).toBe(MyAMS.i18n.ERRORS_OCCURED);
		expect($('li', alertDiv).length).toBe(2);
	});

});

test("Test MyAMS.error.showErrors function for JSON object", () => {

	document.body.innerHTML = `<div>
		<form class="parent">
			<div class="alert-danger">Old alert</div>
			<div class="row">
				<div class="form-widget">
					<input type="text" name="form.widgets.input" id="form_widgets_input" />
				</div>
			</div>
			<div class="row">
				<div class="form-widget">
					<input type="number" name="form.widgets.number" id="form_widgets_number" />
				</div>
			</div>
		</form>
	</div>`;

	const
		body = $(document.body),
		parent = $('.parent', body);
	expect(parent.exists()).toBe(true);
	return error.showErrors(parent, {
		header: "Error header",
		error: "Error message",
		messages: [
			"First error message",
			{
				header: "Second error header",
				message: "Second error message"
			}
		],
		widgets: [
			{
				id: "form_widgets_input",
				label: "Widget label",
				message: "Text error message"
			},
			{
				name: "form.widgets.number",
				label: "Widget label",
				message: "Number error message"
			}
		]
	}).then(() => {
		const alertDiv = $('.alert', parent);
		expect(alertDiv.exists()).toBe(true);
		expect(alertDiv.length).toBe(1);
		expect(alertDiv.hasClass('alert-danger')).toBe(true);
		expect($('.alert-heading', alertDiv).text()).toBe("Error header");
		expect($('li', alertDiv).length).toBe(4);
		expect($('strong', alertDiv).length).toBe(3);
		const text = $('#form_widgets_input', parent);
		expect(text.exists()).toBe(true);
		expect(text.siblings('.is-invalid').exists()).toBe(true);
		expect(text.siblings('.is-invalid').text()).toBe("Text error message");
		const number = $('[name="form.widgets.number"]', parent);
		expect(number.exists()).toBe(true);
		expect(number.siblings('.is-invalid').exists()).toBe(true);
		expect(number.siblings('.is-invalid').text()).toBe("Number error message");
	});

});
