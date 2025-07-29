/* global jest, test, expect */
/**
 * MyAMS.plugins "checker" test
 */

import $ from "jquery";

import MyAMS, { init } from "../ext-base";
import { checker } from "../mod-plugins";

import myams_require from "../ext-require";


init($);

if (!MyAMS.plugins) {
	MyAMS.config.modules.push('plugins');
}
MyAMS.require = myams_require;


test("Test MyAMS.plugins without checker", () => {

	document.body.innerHTML = `<div>
		<form>
			<fieldset>
				<legend>Legend</legend>
				<div class="panel"></div>
			</fieldset>
		</form>
	</div>`;

	const
		body = $(document.body),
		form = $('form', body),
		fieldset = $('fieldset', form),
		legend = $('legend', fieldset);

	legend.on('after-init.ams.checker', (evt, legend) => {
		legend.data('after-init', true);
	});

	return checker(body).then((result) => {
		expect(result).toBeNull();
		expect(legend.data('after-init')).toBeUndefined();
	});
});


test("Test MyAMS.plugins checker plug-in", () => {

	document.body.innerHTML = `<div>
		<form>
			<fieldset>
				<legend class="checker"></legend>
				<div class="panel"></div>
			</fieldset>
		</form>
	</div>`;

	const
		body = $(document.body),
		form = $('form', body),
		fieldset = $('fieldset', form),
		legend = $('legend', fieldset);

	legend.on('after-init.ams.checker', (evt, legend) => {
		legend.data('after-init', true);
	});

	checker(body);  // test multiple initializations
	return checker(body).then((result) => {

		expect(result.length).toBe(1);

		expect(legend.data('after-init')).toBe(true);
		expect(fieldset.hasClass('switched')).toBe(true);

		const checkbox = $('input[type="checkbox"]', legend);
		expect(checkbox.exists()).toBe(true);
		expect(checkbox.hasClass('checker')).toBe(true);
		expect(checkbox.attr('name').startsWith('checker_')).toBe(true);
		expect(checkbox.val()).toBe('true');

		const prefix = $('input.prefix', legend);
		expect(prefix.exists()).toBe(false);

		const marker = $('input.marker', legend);
		expect(marker.exists()).toBe(false);

		const label = $('label', legend);
		expect(label.exists()).toBe(true);
		expect(label.attr('for')).toBe(checkbox.attr('id'));

		checkbox.prop('checked', true).trigger('change');
		expect(fieldset.hasClass('switched')).toBe(false);

		checkbox.prop('checked', false).trigger('change');
		expect(fieldset.hasClass('switched')).toBe(true);

		checkbox.prop('checked', true).trigger('change');
		expect(fieldset.hasClass('switched')).toBe(false);

		form.trigger('reset');
		expect(fieldset.hasClass('switched')).toBe(true);
	});
});


test("Test MyAMS.plugins checker plug-in in disabled mode", () => {

	document.body.innerHTML = `<div>
		<form>
			<fieldset>
				<legend class="checker"
						data-ams-checker-mode="disable"></legend>
				<div class="panel"></div>
			</fieldset>
		</form>
	</div>`;

	const
		body = $(document.body),
		fieldset = $('fieldset', body),
		legend = $('legend', fieldset);

	return checker(body).then((result) => {

		expect(result.length).toBe(1);
		expect(fieldset.prop('disabled')).toBe(true);

		const checkbox = $('input[type="checkbox"]', legend);

		checkbox.prop('checked', true).trigger('change');
		expect(fieldset.prop('disabled')).toBe(false);

		checkbox.prop('checked', false).trigger('change');
		expect(fieldset.prop('disabled')).toBe(true);
	});
});


test("Test MyAMS.plugins checker plug-in with prefix and field name", () => {

	document.body.innerHTML = `<div>
		<form>
			<fieldset>
				<legend class="checker"
						data-ams-checker-fieldname="form.widgets.myfield"
						data-ams-checker-hidden-prefix="prefix_"></legend>
				<div class="panel"></div>
			</fieldset>
		</form>
	</div>`;

	const
		body = $(document.body),
		fieldset = $('fieldset', body),
		legend = $('legend', fieldset);

	return checker(body).then((result) => {

		expect(result.length).toBe(1);

		expect(fieldset.hasClass('switched')).toBe(true);

		const checkbox = $('input[type="checkbox"]', legend);
		expect(checkbox.exists()).toBe(true);
		expect(checkbox.hasClass('checker')).toBe(true);
		expect(checkbox.attr('name')).toBe('form.widgets.myfield');
		expect(checkbox.val()).toBe('true');

		const prefix = $('input.prefix', legend);
		expect(prefix.exists()).toBe(true);
		expect(prefix.attr('id')).toBe('prefix_form.widgets.myfield_prefix');
		expect(prefix.attr('name')).toBe('prefix_form.widgets.myfield');
		expect(prefix.val()).toBe('false');

		const marker = $('input.marker', legend);
		expect(marker.exists()).toBe(false);

		checkbox.prop('checked', true).trigger('change');
		expect(fieldset.prop('disabled')).toBe(false);
		expect(prefix.val()).toBe('true');

		checkbox.prop('checked', false).trigger('change');
		expect(fieldset.hasClass('switched')).toBe(true);
		expect(prefix.val()).toBe('false');
	});
});


test("Test MyAMS.plugins checker plug-in with marker", () => {

	document.body.innerHTML = `<div>
		<form>
			<fieldset>
				<legend class="checker"
						data-ams-checker-fieldname="form.widgets.myfield"
						data-ams-checker-marker="_marker"></legend>
				<div class="panel"></div>
			</fieldset>
		</form>
	</div>`;

	const
		body = $(document.body),
		fieldset = $('fieldset', body),
		legend = $('legend', fieldset);

	return checker(body).then((result) => {

		expect(result.length).toBe(1);

		expect(fieldset.hasClass('switched')).toBe(true);

		const checkbox = $('input[type="checkbox"]', legend);
		expect(checkbox.exists()).toBe(true);
		expect(checkbox.hasClass('checker')).toBe(true);
		expect(checkbox.attr('name')).toBe('form.widgets.myfield');
		expect(checkbox.val()).toBe('true');

		const prefix = $('input.prefix', legend);
		expect(prefix.exists()).toBe(false);

		const marker = $('input.marker', legend);
		expect(marker.exists()).toBe(true);
		expect(marker.attr('name')).toBe('form.widgets.myfield_marker');

		checkbox.prop('checked', true).trigger('change');
		expect(fieldset.prop('disabled')).toBe(false);

		checkbox.prop('checked', false).trigger('change');
		expect(fieldset.hasClass('switched')).toBe(true);
	});
});


test("Test MyAMS.plugins checker plug-in with global veto", () => {

	document.body.innerHTML = `<div>
		<form>
			<fieldset>
				<legend class="checker"></legend>
				<div class="panel"></div>
			</fieldset>
		</form>
	</div>`;

	const
		body = $(document.body),
		fieldset = $('fieldset', body),
		legend = $('legend', fieldset);

	legend.on('before-init.ams.checker', (evt, legend, props, veto) => {
		veto.veto = true;
	});

	return checker(body).then((result) => {

		expect(result.length).toBe(1);

		const checkbox = $('input[type="checkbox"]', legend);
		expect(checkbox.exists()).toBe(false);
	});
});


test("Test MyAMS.plugins checker plug-in with veto on click", () => {

	document.body.innerHTML = `<div>
		<form>
			<fieldset>
				<legend class="checker"></legend>
				<div class="panel"></div>
			</fieldset>
		</form>
	</div>`;

	const
		body = $(document.body),
		fieldset = $('fieldset', body),
		legend = $('legend', fieldset);

	legend.on('before-switch.ams.checker', (evt, legend, veto) => {
		veto.veto = true;
	});

	return checker(body).then((result) => {

		expect(result.length).toBe(1);

		expect(fieldset.hasClass('switched')).toBe(true);

		const checkbox = $('input[type="checkbox"]', legend);
		checkbox.prop('checked', true).trigger('change');
		expect(fieldset.hasClass('switched')).toBe(true);
	});
});


test("Test MyAMS.plugins checker plug-in with pre-checked state", () => {

	document.body.innerHTML = `<div>
		<form>
			<fieldset>
				<legend class="checker"
						data-ams-checker-state="on"></legend>
				<div class="panel"></div>
			</fieldset>
		</form>
	</div>`;

	const
		body = $(document.body),
		fieldset = $('fieldset', body),
		legend = $('legend', fieldset);

	return checker(body).then((result) => {

		expect(result.length).toBe(1);

		expect(fieldset.hasClass('switched')).toBe(false);
	});
});
