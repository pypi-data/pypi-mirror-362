/* global describe, beforeAll, afterAll, jest, test, expect */
/**
 * MyAMS form module tests
 */

import $ from "jquery";

import MyAMS, { init } from "../ext-base";
import { ajax } from "../mod-ajax";
import { alert } from "../mod-alert";
import { i18n } from "../mod-i18n";
import { modal } from "../mod-modal";

import {
	form,
	showFormSubmitWarning,
	getFormValidators,
	checkFormValidators,
	initFormSubmitButton,
	resetFormSubmitButton,
	getFormData,
	initFormData,
	submitForm,
	formSubmitCallback,
	getFormTarget,
	initFormTarget,
	getFormAction,
	getFormAjaxSettings,
	getFormProgressSettings,
	getFormProgressState,
	resetFormAfterSubmit,
	resetFormAfterError,
	getFormDownloadTarget,
	initFormDownloadTarget,
	resetFormDownloadTarget
} from "../mod-form";

import myams_require from "../ext-require";

import { MockXHR } from "../__mocks__/xhr";

const bs = require("bootstrap");
// Bootstrap toasts are required...
$.fn.toast = bs.Toast._jQueryInterface;
$.fn.toast.Constructor = bs.Toast;

const jqForm = require("jquery-form");
$.fn.ajaxSubmit = jqForm;


init($);

if (!MyAMS.ajax) {
	MyAMS.ajax = ajax;
	MyAMS.config.modules.push('ajax');
}
if (!MyAMS.alert) {
	MyAMS.alert = alert;
	MyAMS.config.modules.push('alert');
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
MyAMS.require = myams_require;


describe("Test MyAMS.skin module", () => {

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

	// Test MyAMS.form initialization
	test("Test MyAMS.form init function", () => {

		document.body.innerHTML = `<div>
			<form>
				<a class="submit">Submit</a>
			</form>
		</div>`;

		MyAMS.form.init();
		const body = $(document.body);
		$('.submit', body).click();
		expect($('form', body).data('ams-submit-button').exists()).toBe(true);

	});


	// Test MyAMS.form initElement
	test("Test MyAMS.form initElement function", () => {

		document.body.innerHTML = `<div>
			<form>
				<div class="alert alert-danger"></div>
				<input type="text" name="form.widgets.text"
					   data-ams-changed-callback="MyAMS.testCallback" />
			</form>
		</div>`;

		MyAMS.testCallback = (form, input) => {
			form.addClass('modified');
			input.addClass('modified');
		}

		jest.useFakeTimers();
		try {
			MyAMS.form.init();

			const
				body = $(document.body),
				testForm = $('form', body),
				testInput = $('input', testForm);
			form.initElement('body');

			// test change event
			expect(MyAMS.config.warnOnFormChange).toBe(true);
			testInput.trigger('change')
			expect(testForm.attr('data-ams-form-changed')).toBe('true');
			expect(testForm.hasClass('modified')).toBe(true);
			expect(testInput.hasClass('modified')).toBe(true);
			delete MyAMS.testCallback;

			// test form unload
			const unload = form.checkBeforeUnload();
			expect(unload).toBe(i18n.FORM_CHANGED_WARNING);

			// test reset event
			testForm.trigger('reset');
			jest.runAllTimers();
			expect($('.alert', testForm).exists()).toBe(false);
			expect(testForm.attr('data-ams-form-changed')).toBe(undefined);
		} finally {
			jest.useRealTimers();
			delete MyAMS.testCallback;
		}
	});


	// Test MyAMS.form confirmChangedForm
	test("Test MyAMS.form confirmChangedForm function", () => {

		document.body.innerHTML = `<div>
			<form>
				<input type="text" name="form.widgets.text" />
			</form>
		</div>`;

		MyAMS.dom = {
			root: $(document.body)
		};

		// patch MyAMS.alert.bigBox for user input
		const oldBox = alert.bigBox;
		alert.bigBox = jest.fn().mockImplementation(() => {
			return Promise.resolve('success');
		});

		const
			body = $(document.body),
			testForm = $('form', body),
			testInput = $('input', testForm);

		form.initElement(body);
		testInput.trigger('change')

		return form.confirmChangedForm(body).then((status) => {
			expect(status).toBe('success');
			expect(testForm.attr('data-ams-form-changed')).toBe(undefined);
			alert.bigBox = oldBox;
		});

	});

	test("Test MyAMS.form confirmChangedForm function with cancelled result", () => {

		document.body.innerHTML = `<div>
			<form>
				<input type="text" name="form.widgets.text" />
			</form>
		</div>`;

		MyAMS.dom = {
			root: $(document.body)
		};

		// patch MyAMS.alert.bigBox for user input
		const oldBox = alert.bigBox;
		alert.bigBox = jest.fn().mockImplementation(() => {
			return Promise.resolve('abort');
		});

		const
			body = $(document.body),
			testForm = $('form', body),
			testInput = $('input', testForm);

		form.initElement(body);
		testInput.trigger('change');

		return form.confirmChangedForm(body).then((status) => {
			expect(status).toBe('abort');
			expect(testForm.attr('data-ams-form-changed')).toBe('true');
			alert.bigBox = oldBox;
		});

	});

	test("Test MyAMS.form confirmChangedForm function with no modified form", () => {

		document.body.innerHTML = `<div>
			<form>
				<input type="text" name="form.widgets.text" />
			</form>
		</div>`;

		MyAMS.dom = {
			root: $(document.body)
		};

		const
			body = $(document.body),
			testForm = $('form', body);

		form.initElement(body);

		return form.confirmChangedForm(body).then((status) => {
			expect(status).toBe('success');
			expect(testForm.attr('data-ams-form-changed')).toBe(undefined);
		});

	});

	test("Test MyAMS.form confirmChangedForm function with disabled warn changes", () => {

		document.body.innerHTML = `<div>
			<form data-ams-warn-on-change="true">
				<input type="text" name="form.widgets.text" />
			</form>
		</div>`;

		MyAMS.dom = {
			root: $(document.body)
		};

		const
			body = $(document.body),
			testForm = $('form', body);

		MyAMS.config.warnOnFormChange = false;
		form.initElement(body);

		return form.confirmChangedForm(body).then((status) => {
			expect(status).toBe('success');
			expect(testForm.attr('data-ams-form-changed')).toBe(undefined);
		});

	});


	// Test MyAMS.form setFocus
	test("Test MyAMS.form setFocus", () => {

		document.body.innerHTML = `<div>
			<form>
				<input type="text" name="form.widgets.text" />
			</form>
		</div>`;

		MyAMS.dom = {
			root: $(document.body)
		};

		const
			body = $(document.body),
			testForm = $('form', body),
			input = $('input', testForm);

		let focused = false;
		$(input).on('focusin', () => {
			focused = true;
		});

		MyAMS.config.warnOnFormChange = false;
		form.initElement(body);
		return MyAMS.form.setFocus(testForm).then((target) => {
			expect(focused).toBe(true);
			expect(target.exists()).toBe(true);
			expect(target.get(0)).toBe(input.get(0));
		});

	});

	test("Test MyAMS.form setFocus with focus target", () => {

		document.body.innerHTML = `<div>
			<form>
				<input id="text1" type="text" name="form.widgets.text1" />
				<input id="text2" type="text" name="form.widgets.text2"
					   data-ams-focus-target />
			</form>
		</div>`;

		MyAMS.dom = {
			root: $(document.body)
		};

		const
			body = $(document.body),
			testForm = $('form', body),
			input = $('#text2', testForm);

		let focused = false;
		$(input).on('focusin', () => {
			focused = true;
		});

		MyAMS.config.warnOnFormChange = false;
		form.initElement(body);
		return MyAMS.form.setFocus(testForm).then((target) => {
			expect(focused).toBe(true);
			expect(target.exists()).toBe(true);
			expect(target.get(0)).toBe(input.get(0));
		});

	});


	// Test MyAMS.form reset handler
	test("Test MyAMS.form reset handlers", () => {

		document.body.innerHTML = `<div>
			<form>
				<div class="alert-danger persistent">Persistent alert</div>
				<div class="alert-danger">Temporary alert</div>
				<input type="text" name="input1" value="Value 1" />
				<label class="state-error">State error</label>
				<input type="text" name="input2" value="Value 2"
					   data-ams-reset-callback="MyAMS.test.resetHandler"
					   data-ams-reset-callback-options='{
						"source": "input2",
						"value": "Value 3"
					   }' />
			</form>
		</div>`;

		const form = $('form');
		MyAMS.test = {
			resetHandler: (form, source, options) => {
				form.data('reset', true);
				$(source).val(options.value);
			}
		};

		jest.useFakeTimers();
		try {
			MyAMS.form.init();
			form.trigger('reset');
			jest.runAllTimers();
			expect(form.data('reset')).toBe(true);
			expect($('.alert-danger', form).length).toBe(1);
			expect($('input[name="input2"]', form).val()).toBe('Value 3');
		} finally {
			jest.useRealTimers();
			delete MyAMS.test;
		}

	});


	// Test MyAMS.handlers custom reset handlers
	test("Test MyAMS.handlers custom reset handler", () => {

		document.body.innerHTML = `<div>
			<form data-ams-reset-handler="MyAMS.test.resetHandler"
				  data-ams-reset-handler-options='{
					"source": "form",
					"value": "resetHandler"
				  }'
				  data-ams-reset-keep-default="false">
				<input type="test" name="input1" />
			</form>
		</div>`;

		const form = $('form');

		MyAMS.test = {
			resetHandler: (evt, form, options) => {
				form.data('reset', true);
				form.data('values', options);
			}
		};

		jest.useFakeTimers();
		try {
			MyAMS.form.init();
			form.trigger('reset');
			jest.runAllTimers();

			expect(form.data('reset')).toBe(true);
			const values = form.data('values');
			expect(values.source).toBe('form');
			expect(values.value).toBe('resetHandler');
		} finally {
			jest.useRealTimers();
			delete MyAMS.test;
		}

	});


	// Test MyAMS.form setInvalid
	test("Test MyAMS.form setInvalid function", () => {

		document.body.innerHTML = `<div>
			<form>
				<div class="form-widget">
					<input type="text" name="form.widgets.text" class="valid" />
				</div>
				<div class="form-widget">
					<input type="number" name="form.widgets.number" class="valid" />
				</div>
			</form>
		</div>`;

		const
			body = $(document.body),
			testForm = $('form', body),
			testInput = $('input[type="text"]', testForm),
			testNumber = $('input[type="number"]', testForm);

		form.initElement(body);

		// set input state by JQuery reference
		form.setInvalid(testForm, testInput, "Error message");
		expect(testInput.siblings('.invalid-feedback').text()).toBe("Error message");
		expect(testInput.hasClass('valid')).toBe(false);
		expect(testInput.hasClass('is-invalid')).toBe(true);

		// set input state by name
		form.setInvalid(testForm, testNumber.attr('name'), "Error message");
		expect(testNumber.siblings('.invalid-feedback').text()).toBe("Error message");
		expect(testNumber.hasClass('valid')).toBe(false);
		expect(testNumber.hasClass('is-invalid')).toBe(true);

	});


	// Test MyAMS.form getSettings
	test("Test MyAMS.form getSettings with default settings", () => {

		document.body.innerHTML = `<div>
			<form action="data/test.json">
				<input type="text" />
				<button type="submit"><i class="fa fa-save>"></i></button>
			</form>
		</div>`;

		const
			body = $(document.body),
			testForm = $('form', body),
			testFormData = testForm.data(),
			testButton = $('button', testForm),
			testButtonData = testButton.data();

		const settings = form.getSettings(testForm, testFormData, testButton, testButtonData, {});
		expect(settings.submitHandler).toBe('data/test.json');
		expect(settings.submitTarget).toBe(null);
		expect(settings.submit).toBe(submitForm);
		expect(settings.submitCallback).toBe(formSubmitCallback);

	});

	test("Test MyAMS.form getSettings with form data, button data and submit options", () => {

		document.body.innerHTML = `<div>
			<form action="data/test.json"
				  data-ams-form-submit-handler="resources/data/submit-handler.json"
				  data-ams-form-submit-callback="MyAMS.settings.customSubmitCallback">
				<input type="text" />
				<button type="submit" name="submit-1">Submit 1</button>
				<button type="submit" name="submit-2"
						data-ams-form-submit-handler="resources/data/submit-handler-2.json"
						data-ams-form-submit-callback="MyAMS.settings.customSubmitCallbackTwo"
						data-ams-form-keep-modal-open="true">
					Submit 2
				</button>
			</form>
		</div>`;

		MyAMS.settings = {
			customSubmitCallback: () => {
			},
			customSubmitCallbackTwo: () => {
			},
			customSubmitCallbackThree: () => {
			},
			customResetAfterSubmit: () => {
			}
		}

		const
			body = $(document.body),
			testForm = $('form', body),
			testFormData = testForm.data(),
			testButton1 = $('button[name="submit-1"]', testForm),
			testButton1Data = testButton1.data(),
			testButton2 = $('button[name="submit-2"]', testForm),
			testButton2Data = testButton2.data();

		// basic form with data options
		let settings = form.getSettings(testForm, testFormData, testButton1, testButton1Data, {});
		expect(settings.submitHandler).toBe('resources/data/submit-handler.json');
		expect(settings.submitCallback).toBe(MyAMS.settings.customSubmitCallback);
		expect(settings.submitTarget).toBe(null);
		expect(settings.submit).toBe(submitForm);
		expect(settings.keepModalOpen).toBe(false);

		// form submit with button data options
		settings = form.getSettings(testForm, testFormData, testButton2, testButton2Data, {});
		expect(settings.submitHandler).toBe('resources/data/submit-handler-2.json');
		expect(settings.submitCallback).toBe(MyAMS.settings.customSubmitCallbackTwo);
		expect(settings.submitTarget).toBe(null);
		expect(settings.submit).toBe(submitForm);
		expect(settings.keepModalOpen).toBe(true);

		// form submit with button data and argument options given by reference or by name
		settings = form.getSettings(testForm, testFormData, testButton1, testButton1Data, {
			submitCallback: MyAMS.settings.customSubmitCallbackThree,
			resetAfterSubmit: "MyAMS.settings.customResetAfterSubmit",
			keepModalOpen: true,
			submitTarget: '#form_target',
			missingOption: true
		});
		expect(settings.submitHandler).toBe('resources/data/submit-handler.json');
		expect(settings.submitCallback).toBe(MyAMS.settings.customSubmitCallbackThree);
		expect(settings.submitTarget).toBe('#form_target');
		expect(settings.submit).toBe(submitForm);
		expect(settings.resetAfterSubmit).toBe(MyAMS.settings.customResetAfterSubmit);
		expect(settings.keepModalOpen).toBe(true);
		expect(settings.missingOption).toBe(undefined);

		// form submit with form data, button data and argument options
		settings = form.getSettings(testForm, testFormData, testButton2, testButton2Data, {
			submitHandler: 'resources/data/submit-options.json',
			submitCallback: MyAMS.settings.customSubmitCallbackThree,
			keepModalOpen: false,
			submitTarget: '#form_target'
		});
		expect(settings.submitHandler).toBe('resources/data/submit-options.json');
		expect(settings.submitCallback).toBe(MyAMS.settings.customSubmitCallbackThree);
		expect(settings.submitTarget).toBe('#form_target');
		expect(settings.submit).toBe(submitForm);
		expect(settings.keepModalOpen).toBe(false);

		delete MyAMS.settings;

	});


	// Test MyAMS.form showFormSubmitWarning
	test("Test MyAMS.form showFormSubmitWarning", () => {

		document.body.innerHTML = `<div>
			<form data-ams-form-alert-timeout="0">
				<div class="form-widget">
					<input type="text" name="form.widgets.text" class="valid" />
				</div>
			</form>
		</div>`;

		const
			body = $(document.body),
			testForm = $('form', body);

		form.initElement(body);

		// Simulate form submit
		testForm.data('submitted', true);
		return showFormSubmitWarning(testForm, {}).then(() => {
			const container = $(`.${MyAMS.config.alertsContainerClass}`);
			expect(container.exists());
			let toast = $('.toast', container);
			expect(toast.exists()).toBe(true);
			expect(toast.length).toBe(1);
			expect(toast.hasClass('toast-warning')).toBe(true);
			expect(toast.data('autohide')).toBe(true);
		});
	});


	// Test MyAMS.form getFormValidators
	test("Test MyAMS.form getFormValidators", () => {

		document.body.innerHTML = `<div>
			<form data-ams-form-validator="MyAMS.validators.test1">
				<input type="text"
					   data-ams-form-validator="MyAMS.validators.test2;;MyAMS.validators.test3" />
			</form>
		</div>`;

		const
			body = $(document.body),
			testForm = $('form', body),
			testInput = $('input', testForm);

		form.initElement(body);

		const validators = getFormValidators(testForm);
		expect(validators).toBeInstanceOf(Map);
		expect(validators.size).toBe(2);
		expect(validators.has(testForm)).toBe(true);
		for (const [key, values] of validators.entries()) {
			if (key.get(0) === testForm.get(0)) {
				expect($.isArray(values)).toBe(true);
				expect(values.length).toBe(1);
				expect(values[0]).toBe('MyAMS.validators.test1');
			} else if (key.get(0) === testInput.get(0)) {
				expect($.isArray(values)).toBe(true);
				expect(values.length).toBe(2);
				expect(values[0]).toBe('MyAMS.validators.test2');
				expect(values[1]).toBe('MyAMS.validators.test3');
			} else {
				throw new Error("Invalid map key!")
			}
		}

	});


	// Test MyAMS.form checkFormValidators
	test("Test MyAMS.form checkFormvalidators with no validator", () => {

		document.body.innerHTML = `<div>
			<form></form>
		</div>`;

		const
			body = $(document.body),
			testForm = $('form', body);

		return checkFormValidators(testForm, {
			getValidators: getFormValidators
		}).then((status) => {
			expect(status).toBe('success');
		});
	});

	test("Test MyAMS.form checkFormvalidators with successfull validator", () => {

		document.body.innerHTML = `<div>
			<form data-ams-form-validator="MyAMS.validators.checkOK"></form>
		</div>`;

		MyAMS.validators = {
			checkOK: () => {
				return Promise.resolve(true);
			}
		};

		const
			body = $(document.body),
			testForm = $('form', body);

		return checkFormValidators(testForm, {
			getValidators: getFormValidators
		}).then((status) => {
			expect(status).toBe('success');
			delete MyAMS.validators;
		});
	});

	test("Test MyAMS.form checkFormvalidators with multiple successfull validators", () => {

		document.body.innerHTML = `<div>
			<form data-ams-form-validator="MyAMS.validators.checkOK">
				<input type="text"
					   data-ams-form-validator="MyAMS.validators.checkOK" />
			</form>
		</div>`;

		MyAMS.validators = {
			checkOK: () => {
				return Promise.resolve(true);
			}
		};

		const
			body = $(document.body),
			testForm = $('form', body);

		return checkFormValidators(testForm, {
			getValidators: getFormValidators
		}).then((status) => {
			expect(status).toBe('success');
			delete MyAMS.validators;
		});
	});

	test("Test MyAMS.form checkFormvalidators with mixed validators", () => {

		document.body.innerHTML = `<div>
			<form data-ams-form-validator="MyAMS.validators.checkOK">
				<input type="text"
					   data-ams-form-validator="MyAMS.validators.checkKO" />
			</form>
		</div>`;

		MyAMS.validators = {
			checkOK: () => {
				return Promise.resolve(true);
			},
			checkKO: () => {
				return Promise.resolve(false);
			}
		};

		const
			body = $(document.body),
			testForm = $('form', body);

		return checkFormValidators(testForm, {
			getValidators: getFormValidators
		}).then((status) => {
			expect(status).toBe('error');
			delete MyAMS.validators;
		});
	});

	test("Test MyAMS.form checkFormvalidators with undefined validator", () => {

		document.body.innerHTML = `<div>
			<form data-ams-form-validator="MyAMS.validators.undefined">
				<input type="text"
					   data-ams-form-validator="MyAMS.validators.checkOK" />
			</form>
		</div>`;

		MyAMS.validators = {
			checkOK: () => {
				return Promise.resolve(true);
			}
		};

		const
			body = $(document.body),
			testForm = $('form', body);

		return checkFormValidators(testForm, {
			getValidators: getFormValidators
		}).then((status) => {
			expect(status).toBe('error');
			delete MyAMS.validators;
		});
	});

	test("Test MyAMS.form checkFormvalidators with validators with message", () => {

		document.body.innerHTML = `<div>
			<form data-ams-form-validator="MyAMS.validators.checkOK">
				<input type="text"
					   data-ams-form-validator="MyAMS.validators.checkKO" />
			</form>
		</div>`;

		MyAMS.validators = {
			checkOK: () => {
				return Promise.resolve(true);
			},
			checkKO: () => {
				return Promise.resolve("Error message");
			}
		};

		const
			body = $(document.body),
			testForm = $('form', body);

		return checkFormValidators(testForm, {
			getValidators: getFormValidators
		}).then((status) => {
			expect(status).toBe('error');
			expect($('.alert', testForm).exists()).toBe(true);
			expect($('.alert li', testForm).length).toBe(1);
			expect($('.alert li', testForm).text().trim()).toBe("Error message");
			delete MyAMS.validators;
		});
	});

	test("Test MyAMS.form checkFormvalidators with validators with multiple messages", () => {

		document.body.innerHTML = `<div>
			<form data-ams-form-validator="MyAMS.validators.checkKO_1">
				<input type="text"
					   data-ams-form-validator="MyAMS.validators.checkKO_2" />
			</form>
		</div>`;

		MyAMS.validators = {
			checkKO_1: () => {
				return Promise.resolve("Error message 1");
			},
			checkKO_2: () => {
				return Promise.resolve("Error message 2");
			}
		};

		const
			body = $(document.body),
			testForm = $('form', body);

		return checkFormValidators(testForm, {
			getValidators: getFormValidators
		}).then((status) => {
			expect(status).toBe('error');
			expect($('.alert', testForm).exists()).toBe(true);
			expect($('.alert li', testForm).length).toBe(2);
			expect($('.alert li', testForm).first().text().trim()).toBe("Error message 1");
			expect($('.alert li', testForm).last().text().trim()).toBe("Error message 2");
			delete MyAMS.validators;
		});
	});


	// Test MyAMS.form initFormSubmitButton/resetFormSubmitButton
	test("Test MyAMS.form initFormSubmitButton/resetFormSubmitbutton with default settings", () => {

		document.body.innerHTML = `<div>
			<form>
				<input type="text" />
				<button type="submit">Submit</button>
			</form>
		</div>`;

		const
			body = $(document.body),
			testForm = $('form', body),
			testButton = $('button', testForm);

		// init submit button
		initFormSubmitButton(testForm, {}, testButton);
		expect(testButton.prop('disabled')).toBe(true);
		expect(testButton.data('original-text')).toBe("Submit");
		expect(testButton.text()).toBe("Submit...");
		expect($('.progress', testButton).exists()).toBe(true);

		// reset submit button
		resetFormSubmitButton(testForm, {}, testButton);
		expect($('.progress', testButton).exists()).toBe(false);
		expect(testButton.text()).toBe("Submit");
		expect(testButton.prop('disabled')).toBe(false);

	});

	test("Test MyAMS.form initFormSubmitButton/resetFormSubmitbutton with custom message", () => {

		document.body.innerHTML = `<div>
			<form>
				<input type="text" />
				<button type="submit" data-ams-loading-text="Loading">Submit</button>
			</form>
		</div>`;

		const
			body = $(document.body),
			testForm = $('form', body),
			testButton = $('button', testForm);

		// init submit button
		initFormSubmitButton(testForm, {}, testButton);
		expect(testButton.prop('disabled')).toBe(true);
		expect(testButton.data('original-text')).toBe("Submit");
		expect(testButton.text()).toBe("Loading...");
		expect($('.progress', testButton).exists()).toBe(true);

		// reset submit button
		resetFormSubmitButton(testForm, {}, testButton);
		expect($('.progress', testButton).exists()).toBe(false);
		expect(testButton.text()).toBe("Submit");
		expect(testButton.prop('disabled')).toBe(false);

	});

	test("Test MyAMS.form initFormSubmitButton/resetFormSubmitbutton with HTML button", () => {

		document.body.innerHTML = `<div>
			<form>
				<input type="text" />
				<button type="submit"><i class="fa fa-save>"></i></button>
			</form>
		</div>`;

		const
			body = $(document.body),
			testForm = $('form', body),
			testButton = $('button', testForm);

		// init submit button
		initFormSubmitButton(testForm, {}, testButton);
		expect(testButton.prop('disabled')).toBe(true);
		expect(testButton.data('original-html')).toBeDefined();
		expect(testButton.html()).toBe('<i class="fa fa-cog fa-spin"></i>');
		expect($('.progress', testButton).exists()).toBe(false);

		// reset submit button
		resetFormSubmitButton(testForm, {}, testButton);
		expect($('.progress', testButton).exists()).toBe(false);
		expect(testButton.html()).toBe('<i class="fa fa-save>"></i>');
		expect(testButton.prop('disabled')).toBe(false);

	});


	// Test MyAMS.form getFormData / initFormData
	test("Test MyAMS.form getFormData/initFormData", () => {

		document.body.innerHTML = `<div>
			<form data-ams-form-data='{
				"field1": "value1",
				"field2": "value2",
				"field3": "value3"
			}'>
				<input type="text" />
				<button type="submit"
						data-ams-form-data='{
							"field1": "value4",
							"field2": "value5",
							"field4": "value6"
						}'>
					Submit
				</button>
			</form>
		</div>`;

		const
			body = $(document.body),
			testForm = $('form', body),
			testFormData = testForm.data(),
			testButton = $('button', testForm),
			testButtonData = testButton.data();

		const
			settings = form.getSettings(testForm, testFormData, testButton, testButtonData, {}),
			result = getFormData(testForm, settings, testFormData, testButton, testButtonData, {
				data: {
					field1: "value7",
					field4: "value8",
					field5: "value9"
				}
			});

		expect(result.field1).toBe("value7");
		expect(result.field2).toBe("value5");
		expect(result.field3).toBe("value3");
		expect(result.field4).toBe("value8");
		expect(result.field5).toBe("value9");

		testForm.on('init-data.ams.form', (evt) => {
			$(evt.target).data('init', true);
		});

		const
			postData = {},
			veto = {veto: false};
		settings.initDataCallback = (theForm, settings, button, data, options, veto) => {
			theForm.data('init-callback', true);
		};
		initFormData(testForm, settings, testButton, postData, {}, veto);
		expect(testForm.data('init')).toBe(true);
		expect(testForm.data('init-callback')).toBe(true);

	});


	// Test MyAMS.form getFormTarget
	test("Test MyAMS.form getFormTarget without any target", () => {

		document.body.innerHTML = `<div>
			<form></form>
		</div>`;

		const
			body = $(document.body),
			testForm = $('form', body),
			testFormData = testForm.data(),
			testButton = $('button', testForm),
			testButtonData = testButton.data() || {};

		const
			settings = form.getSettings(testForm, testFormData, testButton, testButtonData, {}),
			target = getFormTarget(testForm, settings, testFormData, testButtonData);

		expect(target.exists()).toBe(false);

	});

	test("Test MyAMS.form getFormTarget with simple target", () => {

		document.body.innerHTML = `<div>
			<form target="#target"></form>
			<div id="target"></div>
		</div>`;

		const
			body = $(document.body),
			testForm = $('form', body),
			testFormData = testForm.data(),
			testButton = $('button', testForm),
			testButtonData = testButton.data() || {},
			testTarget = $('#target', body);

		const
			settings = form.getSettings(testForm, testFormData, testButton, testButtonData, {}),
			target = getFormTarget(testForm, settings, testFormData, testButtonData);

		expect(target.exists()).toBe(true);
		expect(target.get(0)).toBe(testTarget.get(0));

	});

	test("Test MyAMS.form getFormTarget with form target data attribute", () => {

		document.body.innerHTML = `<div>
			<form data-ams-form-submit-target="#target"></form>
			<div id="target"></div>
		</div>`;

		const
			body = $(document.body),
			testForm = $('form', body),
			testFormData = testForm.data(),
			testButton = $('button', testForm),
			testButtonData = testButton.data() || {},
			testTarget = $('#target', body);

		const
			settings = form.getSettings(testForm, testFormData, testButton, testButtonData, {}),
			target = getFormTarget(testForm, settings, testFormData, testButtonData);

		expect(target.exists()).toBe(true);
		expect(target.get(0)).toBe(testTarget.get(0));

	});

	test("Test MyAMS.form getFormTarget with button target data attribute", () => {

		document.body.innerHTML = `<div>
			<form>
				<button type="submit"
						data-ams-form-submit-target="#target">Submit</button>
			</form>
			<div id="target"></div>
		</div>`;

		const
			body = $(document.body),
			testForm = $('form', body),
			testFormData = testForm.data(),
			testButton = $('button', testForm),
			testButtonData = testButton.data() || {},
			testTarget = $('#target', body);

		const
			settings = form.getSettings(testForm, testFormData, testButton, testButtonData, {}),
			target = getFormTarget(testForm, settings, testFormData, testButtonData);

		expect(target.exists()).toBe(true);
		expect(target.get(0)).toBe(testTarget.get(0));

	});

	test("Test MyAMS.form getFormTarget with submit options", () => {

		document.body.innerHTML = `<div>
			<form target="#missing">
				<button type="submit"
						data-ams-form-submit-target="#other">Submit</button>
			</form>
			<div id="target"></div>
		</div>`;

		const
			body = $(document.body),
			testForm = $('form', body),
			testFormData = testForm.data(),
			testButton = $('button', testForm),
			testButtonData = testButton.data() || {},
			testTarget = $('#target', body);

		const
			settings = form.getSettings(testForm, testFormData, testButton, testButtonData, {
				submitTarget: '#target'
			}),
			target = getFormTarget(testForm, settings, testFormData, testButtonData);

		expect(target.exists()).toBe(true);
		expect(target.get(0)).toBe(testTarget.get(0));

	});


	// Test MyAMS.form initFormTarget
	test("Test MyAMS.form initFormTarget", () => {

		document.body.innerHTML = `<div>
			<form target="#target"></form>
			<div class="hidden">
				<div id="target"></div>
			</div>
		</div>`;

		const
			body = $(document.body),
			testForm = $('form', body),
			testFormData = testForm.data(),
			testButton = $('button', testForm),
			testButtonData = testButton.data() || {},
			testTarget = $('#target', body);

		const
			settings = form.getSettings(testForm, testFormData, testButton, testButtonData, {}),
			target = getFormTarget(testForm, settings, testFormData, testButtonData);

		initFormTarget(testForm, settings, target);
		expect($('.fa-cog', testTarget).exists()).toBe(true);
		expect(testTarget.parents('.hidden').exists()).toBe(false);

	});


	// Test MyAMS.form getFormAction
	test("Test MyAMS.form getFormAction for relative URL", () => {

		document.body.innerHTML = `<div>
			<form action="data/submit.json"></form>
		</div>`;

		MyAMS.ajax = {
			getAddr: (addr) => {
				const href = addr || window.location.href;
				return href.substr(0, href.lastIndexOf('/') + 1);
			}
		}

		const
			body = $(document.body),
			testForm = $('form', body),
			testFormData = testForm.data(),
			testButton = $('button', testForm),
			testButtonData = testButton.data() || {};

		const
			settings = form.getSettings(testForm, testFormData, testButton, testButtonData, {}),
			url = getFormAction(testForm, settings);

		expect(url).toBe('http://localhost/data/submit.json');

		delete MyAMS.ajax;

	});

	test("Test MyAMS.form getFormAction for absolute URL", () => {

		document.body.innerHTML = `<div>
			<form action="http://example.com/data/submit.json"></form>
		</div>`;

		const
			body = $(document.body),
			testForm = $('form', body),
			testFormData = testForm.data(),
			testButton = $('button', testForm),
			testButtonData = testButton.data() || {};

		const
			settings = form.getSettings(testForm, testFormData, testButton, testButtonData, {}),
			url = getFormAction(testForm, settings);

		expect(url).toBe('http://example.com/data/submit.json');

	});

	test("Test MyAMS.form getFormAction with custom handler", () => {

		document.body.innerHTML = `<div>
			<form></form>
		</div>`;

		MyAMS.ajax = {
			getAddr: (addr) => {
				const href = addr || window.location.href;
				return href.substr(0, href.lastIndexOf('/') + 1);
			}
		}

		const
			body = $(document.body),
			testForm = $('form', body),
			testFormData = testForm.data(),
			testButton = $('button', testForm),
			testButtonData = testButton.data() || {};

		const
			settings = form.getSettings(testForm, testFormData, testButton, testButtonData, {}),
			url = getFormAction(testForm, settings, 'data/submit.json');

		expect(url).toBe('http://localhost/data/submit.json');

		delete MyAMS.ajax;

	});


	// Test MyAMS.form getAjaxSettings
	test("Test MyAMS.form getAjaxSettings", () => {

		document.body.innerHTML = `<div>
			<form action="data/submit.json"></form>
		</div>`;

		MyAMS.ajax = {
			getAddr: (addr) => {
				const href = addr || window.location.href;
				return href.substr(0, href.lastIndexOf('/') + 1);
			},
			getResponse: (request) => {
				return {
					contentType: 'json',
					data: {
						status: 'success'
					}
				}
			}
		}

		const
			body = $(document.body),
			testForm = $('form', body),
			testFormData = testForm.data(),
			testButton = $('button', testForm),
			testButtonData = testButton.data() || {};

		$(testForm).on('before-serialize.ams.form', (evt, veto) => {
			$(evt.target).data('event-before-serialize', true);
		});
		$(testForm).on('before-submit.ams.form', (evt, data, veto) => {
			$(evt.target).data('event-before-submit', true);
		});
		$(testForm).on('complete.ams.form', (evt) => {
			$(evt.target).data('event-complete', true);
		});

		const
			settings = form.getSettings(testForm, testFormData, testButton, testButtonData, {}),
			postData = getFormData(testForm, settings, testFormData, testButton, testButtonData, {}),
			action = getFormAction(testForm, settings),
			target = getFormTarget(testForm, settings, testFormData, testButtonData),
			ajaxSettings = getFormAjaxSettings(testForm, settings, testButton, postData, action, target);

		expect(ajaxSettings.url).toBe("http://localhost/data/submit.json");
		expect(ajaxSettings.type).toBe('post');
		expect(ajaxSettings.iframe).toBe(false);

		ajaxSettings.beforeSerialize(testForm, ajaxSettings);
		expect(testForm.data('event-before-serialize')).toBe(true);

		ajaxSettings.beforeSubmit(postData, testForm, ajaxSettings);
		expect(testForm.data('event-before-submit')).toBe(true);
		expect(testForm.data('submitted')).toBe(true);

		ajaxSettings.uploadProgress(null, 50, 100, 50);

		ajaxSettings.complete();

		delete MyAMS.ajax;

	});


	// Test MyAMS.form getProgressSettings
	test("Test MyAMS.form getProgressSettings without settings", () => {

		document.body.innerHTML = `<div>
			<form action="data/submit.json"></form>
		</div>`;

		const
			body = $(document.body),
			testForm = $('form', body),
			testFormData = testForm.data(),
			testButton = $('button', testForm),
			testButtonData = testButton.data() || {};

		const
			settings = form.getSettings(testForm, testFormData, testButton, testButtonData, {}),
			postData = getFormData(testForm, settings, testFormData, testButton, testButtonData, {}),
			progress = getFormProgressSettings(testForm, settings, testButton, postData);

		expect(progress).toBeUndefined();

	});

	test("Test MyAMS.form getProgressSettings with default settings", () => {

		document.body.innerHTML = `<div>
			<form action="data/submit.json"
				  data-ams-form-progress-handler="data/progress.json">
				<button type="submit">Submit</button>
			</form>
		</div>`;

		const
			body = $(document.body),
			testForm = $('form', body),
			testFormData = testForm.data(),
			testButton = $('button', testForm),
			testButtonData = testButton.data() || {};

		const
			settings = form.getSettings(testForm, testFormData, testButton, testButtonData, {}),
			postData = getFormData(testForm, settings, testFormData, testButton, testButtonData, {}),
			progress = getFormProgressSettings(testForm, settings, testButton, postData);

		expect(progress).toBeDefined();
		expect(progress.handler).toBe('data/progress.json');
		expect(progress.fieldname).toBe('progressId');
		expect(postData.progressId).toBeDefined();
		expect(progress.target.text()).toBe('Submit');

	});


	// Test MyAMS.form getProgressState
	test("Test MyAMS.form getProgressState", () => {

		document.body.innerHTML = `<div>
			<form action="data/submit.json"
				  data-ams-form-progress-handler="data/progress.json"></form>
		</div>`;

		const
			oldTimeout = window.setTimeout,
			cldClearTimeout = window.clearTimeout;
		window.setTimeout = (callback, timeout) => {
			callback();
			return null;
		};
		window.clearTimeout = (timeout) => {
		};

		MyAMS.ajax = {
			post: () => {
				return Promise.resolve([{
					status: 'running',
					progress: 'Processing',
					current: 50,
					length: 100
				}, 'success']);
			}
		};

		const
			body = $(document.body),
			testForm = $('form', body),
			testFormData = testForm.data(),
			testButton = $('button', testForm),
			testButtonData = testButton.data() || {};

		const
			settings = form.getSettings(testForm, testFormData, testButton, testButtonData, {}),
			postData = getFormData(testForm, settings, testFormData, testButton, testButtonData, {}),
			progress = getFormProgressSettings(testForm, settings, testButton, postData);

		getFormProgressState(testForm, settings, postData, progress, testButton);

		delete MyAMS.ajax;
		window.setTimeout = oldTimeout;
		window.clearTimeout = cldClearTimeout;

	});

	test("Test MyAMS.form getProgressState for unknown length result", () => {

		document.body.innerHTML = `<div>
			<form action="data/submit.json"
				  data-ams-form-progress-handler="data/progress.json"></form>
		</div>`;

		const
			oldTimeout = window.setTimeout,
			cldClearTimeout = window.clearTimeout;
		window.setTimeout = (callback, timeout) => {
			callback();
			return null;
		};
		window.clearTimeout = (timeout) => {
		};

		MyAMS.ajax = {
			post: () => {
				return Promise.resolve([{
					status: 'running'
				}, 'success']);
			}
		};

		const
			body = $(document.body),
			testForm = $('form', body),
			testFormData = testForm.data(),
			testButton = $('button', testForm),
			testButtonData = testButton.data() || {};

		const
			settings = form.getSettings(testForm, testFormData, testButton, testButtonData, {}),
			postData = getFormData(testForm, settings, testFormData, testButton, testButtonData, {}),
			progress = getFormProgressSettings(testForm, settings, testButton, postData);

		getFormProgressState(testForm, settings, postData, progress, testButton);

		delete MyAMS.ajax;
		window.setTimeout = oldTimeout;
		window.clearTimeout = cldClearTimeout;

	});

	test("Test MyAMS.form getProgressState for finished action", () => {

		document.body.innerHTML = `<div>
			<form action="data/submit.json"
				  data-ams-form-progress-handler="data/progress.json"></form>
		</div>`;

		const
			oldTimeout = window.setTimeout,
			cldClearTimeout = window.clearTimeout;
		window.setTimeout = (callback, timeout) => {
			callback();
			return null;
		};
		window.clearTimeout = (timeout) => {
		};

		MyAMS.ajax = {
			post: () => {
				return Promise.resolve([{
					status: 'finished',
					current: 100,
					length: 100
				}, 'success']);
			}
		};

		const
			body = $(document.body),
			testForm = $('form', body),
			testFormData = testForm.data(),
			testButton = $('button', testForm),
			testButtonData = testButton.data() || {};

		const
			settings = form.getSettings(testForm, testFormData, testButton, testButtonData, {}),
			postData = getFormData(testForm, settings, testFormData, testButton, testButtonData, {}),
			progress = getFormProgressSettings(testForm, settings, testButton, postData);

		getFormProgressState(testForm, settings, postData, progress, testButton);

		delete MyAMS.ajax;
		window.setTimeout = oldTimeout;
		window.clearTimeout = cldClearTimeout;

	});


	// Test MyAMS.form resetAfterSubmit
	test("Test MyAMS.form resetAfterSubmit", () => {

		document.body.innerHTML = `<div>
			<form action="data/submit.json">
				<button type="submit">Submit</button>
			</form>
		</div>`;

		const
			body = $(document.body),
			testForm = $('form', body),
			testFormData = testForm.data(),
			testButton = $('button', testForm),
			testButtonData = testButton.data() || {};

		testForm.on('after-reset.ams.form', (evt) => {
			$(evt.target).data('event-after-reset', true);
		});

		const
			settings = form.getSettings(testForm, testFormData, testButton, testButtonData, {});

		testForm.data('submitted', true);
		initFormSubmitButton(testForm, settings, testButton);
		resetFormAfterSubmit(testForm, settings, testButton);
		expect(testForm.data('submitted')).toBe(false);
		expect(testForm.data('ams-submit-button')).toBe(undefined);
		expect(testForm.data('event-after-reset')).toBe(true);

	});


	// Test MyAMS.form resetAfterError
	test("Test MyAMS.form resetAfterError", () => {

		document.body.innerHTML = `<div>
			<form target="#target"></form>
			<div class="hidden">
				<div id="target"></div>
			</div>
		</div>`;

		const
			body = $(document.body),
			testForm = $('form', body),
			testFormData = testForm.data(),
			testButton = $('button', testForm),
			testButtonData = testButton.data() || {},
			testTarget = $('#target', body);

		const
			settings = form.getSettings(testForm, testFormData, testButton, testButtonData, {}),
			target = getFormTarget(testForm, settings, testFormData, testButtonData);

		initFormTarget(testForm, settings, target);
		expect($('.fa-cog', testTarget).exists()).toBe(true);
		expect(testTarget.parents('.hidden').exists()).toBe(false);
		resetFormAfterError(testForm, settings, target);
		expect($('.fa-cog', testTarget).exists()).toBe(false);
		expect($('.fa-ambulance', testTarget).exists()).toBe(true);

	});


	// Test MyAMS.form getDownloadTarget/initDownloadTarget/resetDownloadTarget
	test("Test MyAMS.form getDownloadTarget/initDownloadTarget/resetDownloadTarget", () => {

		document.body.innerHTML = `<div>
			<form target="#target"
				  data-ams-form-download-target="download_frame"></form>
			<div class="hidden">
				<div id="target"></div>
			</div>
		</div>`;

		const
			body = $(document.body),
			testForm = $('form', body),
			testFormData = testForm.data(),
			testButton = $('button', testForm),
			testButtonData = testButton.data() || {};

		MyAMS.dom = {
			root: body
		};
		MyAMS.ajax = {
			getAddr: (addr) => {
				const href = addr || window.location.href;
				return href.substr(0, href.lastIndexOf('/') + 1);
			}
		};

		const
			settings = form.getSettings(testForm, testFormData, testButton, testButtonData, {}),
			postData = getFormData(testForm, settings, testFormData, testButton, testButtonData, {}),
			action = getFormAction(testForm, settings),
			target = getFormDownloadTarget(testForm, settings),
			ajaxSettings = getFormAjaxSettings(testForm, settings, testButton, postData, action, target);

		expect(target).toBe('download_frame');

		initFormDownloadTarget(testForm, settings, target, ajaxSettings);
		expect($('iframe[name="download_frame"]').exists()).toBe(true);
		expect(ajaxSettings.iframe).toBe(true);
		expect(ajaxSettings.iframeTarget.exists()).toBe(true);

		resetFormDownloadTarget(testForm, settings, testButton, target, ajaxSettings);

		delete MyAMS.ajax;

	});


	// Test MyAMS.form submit
	test("Test MyAMS.form basic submit", () => {

		document.body.innerHTML = `<div>
			<form action="submit.json" method="post"></form>
		</div>`;

		const
			body = $(document.body),
			testForm = $('form', body);

		const
			oldXHR = window.XMLHttpRequest,
			oldAjax = $.ajax;

		const response = {
			contentType: 'application/json',
			status: 'success',
			content: {
				status: 'success'
			}
		}
		window.XMLHttpRequest = jest.fn(() => {
			return MockXHR(response);
		})
		$.ajax = jest.fn().mockImplementation((settings) => {
			const request = XMLHttpRequest();
			return Promise.all([response, 'success', request]);
		});
		expect(MyAMS.form.submit(testForm)).toBe(false);
		$.ajax = oldAjax;
		window.XMLHttpRequest = oldXHR;

	});
});
