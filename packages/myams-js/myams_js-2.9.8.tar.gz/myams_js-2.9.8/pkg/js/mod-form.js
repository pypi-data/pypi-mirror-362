/* global MyAMS, tinyMCE */
/**
 * MyAMS forms support
 */

const $ = MyAMS.$;

if (!$.templates) {
	const jsrender = require('jsrender');
	$.templates = jsrender.templates;
}


let _initialized = false;


/**
 * MyAMS "form" module
 */
export const form = {

	init: () => {

		if (_initialized) {
			return;
		}
		_initialized = true;

		// Add click listener on submit buttons
		$(document).on('click', '[type="submit"], .submit', (evt) => {
			const button = $(evt.currentTarget);
			if (button.exists()) {
				$(button).closest('form').data('ams-submit-button', button);
			}
		});

		// Cancel clicks on readonly checkbox
		$(document).on('click', 'input[type="checkbox"][readonly]', () => {
			return false;
		});

		// Initialize generic and custom reset handlers
		$(document).on('reset', MyAMS.form.resetHandler);
		$(document).on('reset', '[data-ams-reset-handler]', MyAMS.form.customResetHandler);

		// Submit form when CTRL+Enter key is pressed in textarea
		$(document).on('keydown', 'textarea', (evt) => {
			if ((evt.keyCode === 10 || evt.keyCode === 13) && (evt.ctrlKey || evt.metaKey)) {
				const form = $(evt.currentTarget).closest('form');
				$('button[type="submit"]', form).first().click();
			}
		});

		// Always blur readonly inputs
		$(document).on('focus', 'input[readonly]', (evt) => {
			$(evt.currentTarget).blur();
		});

		// Prevent bootstrap dialog from blocking TinyMCE focus
		$(document).on('focusin', (evt) => {
			if ($(evt.target).closest('.mce-window').length >= 0) {
				evt.stopImmediatePropagation();
			}
		});

		// Add unload event listener to check for modified forms
		$(window).on('beforeunload', MyAMS.form.checkBeforeUnload);
	},

	initElement: (element) => {

		if (typeof element === 'string') {
			element = $(element);
		}

		let forms;
		if (MyAMS.config.warnOnFormChange) {
			forms = $('form[data-ams-warn-on-change!="false"]', element);
		} else {
			forms = $('form[data-ams-warn-on-change="true"]', element);
		}
		forms.each((idx, elt) => {
			const
				form = $(elt),
				formData = form.data(),
				callback = formData.amsChangedCallback || MyAMS.config.formChangeCallback;
			$('input, select, textarea, [data-ams-changed-event]', form).each((idx, elt) => {
				const
					input = $(elt),
					inputData = input.data();
				if (inputData.amsIgnoreChange !== true) {
					const event = inputData.amsChangedEvent || 'change';
					input.on(event, () => {
						MyAMS.form.setChanged(form);
						MyAMS.core.executeFunctionByName(inputData.amsChangedCallback ||
							callback, document, form, input);
					});
				}
			});
		});

		MyAMS.form.setFocus(element);
	},

	setFocus: (element) => {
		return new Promise((resolve, reject) => {
			setTimeout(() => {
				let focused = $('[data-ams-focus-target]', element).first();
				if (!focused.exists()) {
					if (window?.process?.env?.NODE_ENV === 'test') {
						focused = $('input, select, textarea', element).first();
					} else {
						focused = $('input:enabled:visible, ' +
							'select:enabled:visible, ' +
							'textarea:enabled:visible', element).first();
					}
				}
				if (focused.exists()) {
					focused.get(0).focus();
				}
				resolve(focused);
			}, 100);
		});
	},

	checkBeforeUnload: () => {
		if (MyAMS.i18n) {
			const forms = $('form[data-ams-form-changed="true"]');
			if (forms.exists()) {
				return MyAMS.i18n.FORM_CHANGED_WARNING;
			}
		}
	},

	confirmChangedForm: (element) => {
		return new Promise((resolve, reject) => {
			const forms = $('form[data-ams-form-changed="true"]', element);
			if (forms.exists()) {
				MyAMS.require('alert').then(() => {
					MyAMS.alert.bigBox({
						status: 'danger',
						title: MyAMS.i18n.WARNING,
						icon: 'text-danger fa-bell',
						message: MyAMS.i18n.FORM_CHANGED_WARNING
					}).then((button) => {
						if (button === 'success') {
							MyAMS.form.resetChanged(forms);
						}
						resolve(button);
					});
				}, () => {
					reject("Missing 'alert' module!");
				});
			} else {
				form.resetChanged(forms);
				resolve('success');
			}
		});
	},

	/**
	 * Update form "chenged" status flag
	 */
	setChanged: (form) => {
		form.attr('data-ams-form-changed', true);
	},

	/**
	 * Default form reset handler
	 *
	 * @param event: the original reset event
	 */
	resetHandler: (event) => {
		const form = $(event.target);
		MyAMS.form.clearAlerts(form);
		MyAMS.form.handleDefaultReset(form);
	},

	/**
	 * Clear remaining form alerts before submitting form
	 */
	clearAlerts: (form) => {
		$('.alert-danger, SPAN.state-error', form).not('.persistent').remove();
		$('.state-error', form).removeClassPrefix('state-');
		$('.invalid-feedback', form).remove();
		$('.is-invalid', form).removeClass('is-invalid');
	},

	/**
	 * Call reset callbacks defined on a form
	 */
	handleDefaultReset: (form) => {
		setTimeout(() => {
			form.find('.select2').trigger('change');
			$('[data-ams-reset-callback]', form).each((idx, elt) => {
				const
					element = $(elt),
					data = element.data(),
					callback = MyAMS.core.getFunctionByName(data.amsResetCallback);
				if (callback !== undefined) {
					callback.call(document, form, element, data.amsResetCallbackOptions);
				}
			});
			MyAMS.form.resetChanged(form);
		}, 10);
	},

	/**
	 * Reset form changed flag
	 */
	resetChanged: (form) => {
		if (form !== undefined) {
			$(form).removeAttr('data-ams-form-changed');
		}
	},

	/**
	 * Custom reset handler
	 */
	customResetHandler: (event) => {
		const
			form = $(event.target),
			data = form.data();
		if (data.amsResetHandler) {
			if ((data.amsKeepDefault !== true) && (data.amsResetKeepDefault !== true)) {
				event.preventDefault();
			}
			const callback = MyAMS.core.getFunctionByName(data.amsResetHandler);
			if (callback !== undefined) {
				callback.call(document, event, form, data.amsResetHandlerOptions);
			}
		}
	},

	/**
	 * Set widget's invalid status
	 *
	 * @param form: parent form
	 * @param input: input name
	 * @param message: associated message
	 */
	setInvalid: (form, input, message) => {
		if (typeof input === 'string') {
			input = $(`[name="${input}"]`, form);
		}
		if (input.exists()) {
			const widget = input.closest('.form-widget');
			$('.invalid-feedback', widget).remove();
			$('<span>')
				.text(message)
				.addClass('is-invalid invalid-feedback')
				.appendTo(widget);
			input.removeClass('valid')
				.addClass('is-invalid');
		}
	},

	/**
	 * Get all settings for given form
	 *
	 * @param form: submitted form
	 * @param formData: form data
	 * @param button: submit button
	 * @param buttonData: submit button data
	 * @param options: submit options
	 */
	getSettings: (form, formData, button, buttonData, options) => {
		const
			defaults = {
				submitWarning: showFormSubmitWarning,
				getValidators: getFormValidators,
				checkValidators: checkFormValidators,
				clearAlerts: MyAMS.form.clearAlerts,
				initSubmitButton: initFormSubmitButton,
				resetSubmitButton: resetFormSubmitButton,
				getData: getFormData,
				initData: initFormData,
				initDataCallback: null,
				getTarget: getFormTarget,
				initTarget: initFormTarget,
				getAction: getFormAction,
				getAjaxSettings: getFormAjaxSettings,
				getProgressSettings: getFormProgressSettings,
				getProgressState: getFormProgressState,
				submit: submitForm,
				datatype: null,
				submitOptions: null,
				submitHandler: (form.attr('action') || '').replace(/#/, ''),
				submitTarget: form.attr('target') || null,
				submitMessage: null,
				submitCallback: formSubmitCallback,
				progressHandler: null,
				progressFieldName: 'progressId',
				progressInterval: 1000,
				progressTarget: null,
				progressCallback: null,
				progressEndCallback: null,
				resetBeforeSubmit: false,
				keepModalOpen: false,
				resetAfterSubmit: resetFormAfterSubmit,
				resetTimeout: 1000,
				resetAfterError: resetFormAfterError,
				downloadTarget: null,
				getDownloadTarget: getFormDownloadTarget,
				initDownloadTarget: initFormDownloadTarget,
				resetDownloadTarget: resetFormDownloadTarget
			},
			settings = $.extend({}, defaults);

		// extend default values with form, button and options properties
		$.extendPrefix(settings, 'amsForm', (value) => {
			return MyAMS.core.getFunctionByName(value) || value;
		}, formData, buttonData);
		$.extendOnly(settings, (value) => {
			return MyAMS.core.getFunctionByName(value) || value;
		}, options);

		return settings;
	},

	/**
	 * Submit given form
	 *
	 * @param form: input form
	 * @param handler: AJAX submit target
	 * @param options: submit options
	 */
	submit: (form, handler, options={}) => {

		// check arguments
		form = $(form);
		if (!form.exists()) {
			return false;
		}
		if (typeof handler === 'object') {
			options = handler;
			handler = undefined;
		}

		// initialize default settings
		const
			formData = form.data(),
			button = $(formData.amsSubmitButton),
			buttonData = button.data() || {},
			settings = MyAMS.form.getSettings(form, formData, button, buttonData, options);

		// prevent multiple submits
		if (formData.submitted) {
			settings.submitWarning(form, settings);
			return false;
		}

		// check custom submit validators
		settings.checkValidators(form, settings).then((status) => {

			// check validation status
			if (status !== 'success') {
				return;
			}

			// submit form
			MyAMS.require('ajax', 'i18n').then(() => {
				MyAMS.ajax.check($.fn.ajaxSubmit,
					`${MyAMS.env.baseURL}../ext/jquery-form${MyAMS.env.extext}.js`).then(() => {

					// clear alerts and initialize submit button
					settings.clearAlerts(form, settings);
					settings.initSubmitButton(form, settings, button);

					// extract and initialize custom submit data
					const
						postData = settings.getData(form, settings, formData, button, buttonData, options),
						veto = { veto: false };
					settings.initData(form, settings, button, postData, options, veto);
					if (veto.veto) {
						settings.resetSubmitButton(form, settings, button);
						return;
					}

					// get and initialize post target
					const target = settings.getTarget(form, settings, formData, buttonData);
					if (target && target.exists()) {
						settings.initTarget(form, settings, target);
					}

					// get form action and POST settings
					const
						action = settings.getAction(form, settings, handler),
						ajaxSettings = settings.getAjaxSettings(form, settings,
							button, postData, action, target);

					// get and initialize download target
					const downloadTarget = settings.getDownloadTarget(form, settings);
					if (downloadTarget) {
						settings.initDownloadTarget(form, settings, downloadTarget, ajaxSettings);
					}

					// get progress settings
					ajaxSettings.progress = settings.getProgressSettings(form, settings,
						button, postData);

					// YESSSS!!!!
					// submit form!!
					settings.submit(form, settings, button, postData, ajaxSettings, target);
					if (downloadTarget) {
						settings.resetDownloadTarget(form, settings, button, downloadTarget, ajaxSettings);
					}
				});
			});
		});

		// disable standard submit
		return false;
	},

	/**
	 * Submit a form from a button click handler
	 */
	submitForm: (evt) => {
		const
			button = $(evt.currentTarget),
			form = button.parents('form');
		form.data('ams-submit-button', button);
		form.submit();
	}
};


/**
 * Show warning message if form was already submitted
 *
 * @param form: submitted form
 * @param settings: computed form settings
 */
export function showFormSubmitWarning(form /*, settings */) {
	return new Promise((resolve, reject) => {
		if (!form.data('ams-form-hide-submitted')) {
			MyAMS.require('i18n', 'alert').then(() => {
				MyAMS.alert.messageBox({
					status: 'warning',
					title: MyAMS.i18n.WAIT,
					message: MyAMS.i18n.FORM_SUBMITTED,
					icon: 'fa-save',
					timeout: form.data('ams-form-alert-timeout') || 5000
				});
			}).then(resolve, reject);
		} else {
			resolve();
		}
	});
}


/**
 * Extract custom validators from given form
 *
 * @param form: checked form
 * @param settings: computed form settings
 * @returns {Map<any, any>}
 */
export function getFormValidators(form /*, settings */) {
	const
		result = new Map(),
		formValidators = (form.data('ams-form-validator') || '').trim().split(/[\s,;]+/);
	let validators = [];
	$(formValidators).each((idx, elt) => {
		if (!elt) {
			return;
		}
		validators.push(elt);
	});
	if (validators.length > 0) {
		result.set(form, validators);
	}
	$('[data-ams-form-validator]', form).each((idx, elt) => {
		const
			element = $(elt),
			elementValidators = (element.data('ams-form-validator') || '').trim().split(/[\s,;]+/);
		validators = [];
		$(elementValidators).each((innerIdx, innerElt) => {
			if (!innerElt) {
				return;
			}
			validators.push(innerElt);
		})
		if (validators.length > 0) {
			result.set(element, validators);
		}
	});
	return result;
}


/**
 * Check custom form validators.
 * A form can handle several form validators which will be called before the form is submitted.
 *
 *
 * @param form: checked form
 * @param settings: computed form settings
 */
export function checkFormValidators(form, settings) {

	return new Promise((resolve, reject) => {
		const validators = settings.getValidators(form, settings);
		if (!validators.size) {
			resolve('success');
			return;
		}
		const checks = [];
		for (const [context, contextValidators] of validators.entries()) {
			for (const validator of contextValidators) {
				checks.push(MyAMS.core.executeFunctionByName(validator, document, form, context));
			}
		}
		$.when.apply($, checks).then((...results) => {
			let status = 'success',
				output = [];
			for (const result of results) {
				if (result !== true) {
					status = 'error';
					if (typeof result === 'string') {
						output.push(result);
					} else if ($.isArray(result) && (result.length > 0)) {
						output = output.concat(result);
					}
				}
			}
			if (output.length > 0) {
				MyAMS.require('i18n', 'alert').then(() => {
					const header = output.length === 1 ? MyAMS.i18n.ERROR_OCCURED :
						MyAMS.i18n.ERRORS_OCCURED;
					MyAMS.alert.alert({
						parent: form,
						status: 'danger',
						header: header,
						message: output
					});
					resolve(status);
				});
			} else {
				resolve(status);
			}
		}, () => {
			reject('error');
		});
	});
}


/**
 * Initialize form submit button
 * Button is disabled and text is updated
 */
export function initFormSubmitButton(form, settings, button) {
	const text = button.data('ams-loading-text') || button.text().trim();
	if (text) {
		button.data('original-text', button.text())
			.prop('disabled', true)
			.text(`${text}...`);
		$('<div>').addClass('progress')
			.appendTo(button);
	} else {  // button without text
		button.data('original-html', button.html())
			.prop('disabled', true)
			.html('<i class="fa fa-cog fa-spin"></i>');
	}
}


// reset form submit button
export function resetFormSubmitButton(form, settings, button) {
	$('.progress', button).remove();
	const text = button.data('original-text');
	if (text) {
		button.text(text);
	} else {
		const html = button.data('original-html');
		if (html) {
			button.html(html);
		}
	}
	button.prop('disabled', false);
}


// get form data
export function getFormData(form, settings, formData, button, buttonData, options) {
	const
		data = $.extend({}, formData.amsFormData, buttonData.amsFormData, options.data),
		name = button.attr('name');
	if (name) {
		data[name] = button.val();
	}
	return data;
}


// initialize form data
export function initFormData(form, settings, button, postData, options, veto) {
	const callback = settings.initDataCallback;
	if (callback) {
		$.extend(postData, callback(form, settings, button, postData, options, veto));
	}
	form.trigger('init-data.ams.form', [postData, veto]);
}


// get form target
export function getFormTarget(form, settings /*, formData, buttonData */) {
	return $(settings.submitTarget);
}


// initialize form target
const TARGET_INIT_TEMPLATE_STRING = `
	<div class="row m-3">
		<div class="text-center w-100">
			<i class="fa fa-3x fa-cog fa-spin"></i>
			{{if message}}
			<strong>{{:message}}</strong>
			{{/if}}
		</div>
	</div>`;

const TARGET_INIT_TEMPLATE = $.templates({
	markup: TARGET_INIT_TEMPLATE_STRING
});

export function initFormTarget(form, settings, target) {
	target.html(TARGET_INIT_TEMPLATE.render({ message: settings.submitMessage }));
	target.parents('.hidden').removeClass('hidden');
}


// get form action
export function getFormAction(form, settings, handler) {
	let url;
	const formHandler = handler || settings.submitHandler;
	if (formHandler.startsWith(window.location.protocol)) {
		url = formHandler;
	} else {
		url = MyAMS.ajax.getAddr() + formHandler;
	}
	return url;
}


// get AJAX POST submit settings
export function getFormAjaxSettings(form, settings, button, postData, action, target) {
	const base = {
		url: action,
		type: 'post',
		cache: false,
		data: postData,
		dataType: settings.datatype,
		beforeSerialize: (form /*, options */) => {
			const veto = { veto: false };
			form.trigger('before-serialize.ams.form', [veto]);
			if (veto.veto) {
				return false;
			}
			if (typeof window.tinyMCE !== 'undefined') {
				tinyMCE.triggerSave();
			}
		},
		beforeSubmit: (data, form /*, options */) => {
			const veto = { veto: false };
			form.trigger('before-submit.ams.form', [data, veto]);
			if (veto.veto) {
				return false;
			}
			form.data('submitted', true);
			if (settings.resetBeforeSubmit) {
				setTimeout(() => {
					settings.resetSubmitButton(form, settings, button);
				}, 250);
			}
		},
		uploadProgress: (evt, position, total, completed) => {
			$('.progress', button).css('background-image',
				`linear-gradient(to right, white -45%, green ${completed}%, red ${completed}%, red)`);
		},
		complete: (xhr) => {
			form.trigger('complete.ams.form', [xhr]);
		},
		success: (result, status, request, form) => {
			const veto = { veto: false };
			form.trigger('submit-success.ams.form', [result, status, request, veto]);
			if (veto.veto) {
				return;
			}
			if (result && result.status !== 'error' && result.closeForm !== false) {
				const modal = form.closest('.modal-dialog');
				if (modal.exists() && !settings.keepModalOpen) {
					MyAMS.modal && MyAMS.modal.close(modal);
				}
			}
			try {
				settings.submitCallback(form, settings, target, result, status, request);
			} finally {
				settings.resetAfterSubmit(form, settings, button);
				MyAMS.form.resetChanged(form);
			}
		},
		error: (request, status, error, form) => {
			form.trigger('submit-error.ams.form', [request, status, error, target]);
			if (target) {
				settings.resetAfterError(form, settings, button, target);
			}
			settings.resetAfterSubmit(form, settings, button);
		},
		iframe: false
	}
	return $.extend({}, base, settings.submitOptions);
}


// get form submit processing progress settings
export function getFormProgressSettings(form, settings, button, postData) {
	const handler = settings.progressHandler;
	if (handler) {
		// check fieldname
		const fieldname = settings.progressFieldName;
		postData[fieldname] = MyAMS.core.generateUUID();
		// check progress target
		let progressTarget = button;
		if (settings.progressTarget) {
			progressTarget = $(settings.progressTarget);
		}
		return {
			handler: handler,
			interval: settings.progressInterval,
			fieldname: fieldname,
			target: progressTarget,
			callback: settings.progressCallback,
			endCallback: settings.progressEndCallback
		}
	}
}


// get form submit progress state
export function getFormProgressState(form, settings, postData, progress, target) {

	let timeout = setTimeout(_getProgressState, progress.interval);

	function _getProgressState() {
		const data = {};
		data[progress.fieldname] = postData[progress.fieldname];
		MyAMS.ajax.post(progress.handler, data)
			.then(MyAMS.core.getFunctionByName(progress.callback || function (result) {
				if ($.isArray(result)) {
					result = result[0];
				}
				if (result.status === 'running') {
					const progressTarget = $(progress.target);
					if (result.message) {
						progressTarget.text(result.message);
					} else {
						let text = result.progress || progressTarget.data('ams-progress-text') || MyAMS.i18n.PROGRESS;
						if (result.current) {
							text += `: ${result.current} / ${result.length || 100}`;
						} else {
							text += '...';
						}
						progressTarget.text(text);
					}
					timeout = setTimeout(_getProgressState, progress.interval);
				} else if (result.status === 'finished') {
					_clearProgressState();
				}
			}), _clearProgressState);
	}

	function _clearProgressState() {
		clearTimeout(timeout);
		settings.resetSubmitButton(form, settings, target);
		MyAMS.core.executeFunctionByName(progress.endCallback, document, form, settings, target);
		MyAMS.form.resetChanged(form);
	}
}


// submit form
export function submitForm(form, settings, button, postData, ajaxSettings, target) {
	if (ajaxSettings.progress) {
		settings.getProgressState(form, settings, postData, ajaxSettings.progress, target);
	}
	form.ajaxSubmit(ajaxSettings);
}


/**
 * Default form submit callback
 * 
 * @param form
 * @param settings: computed form settings
 * @param target
 * @param result
 * @param status
 * @param request
 */
export function formSubmitCallback(form, settings, target, result, status, request) {
	let dataType = settings.datatype;
	if (!dataType) {
		const response = MyAMS.ajax.getResponse(request);
		if (response) {
			dataType = response.contentType;
			result = response.data;
		}
	}

	switch (dataType) {
		case 'binary':
		case 'script':
		case 'xml':
			break;
		case 'json':
			MyAMS.ajax.handleJSON(result, form, target);
			break;
		default:  // text or html
			MyAMS.form.resetChanged(form);
			target.css({ opacity: '0.0' });
			target.removeClass('hidden')
				.parents('.hidden')
				.removeClass('.hidden');
			target.html(result)
				.delay(50)
				.animate({ opacity: '1.0' }, 250);
			MyAMS.core.executeFunctionByName(MyAMS.config.initContent, document, target).then(() => {
				MyAMS.require('helpers').then(() => {
					MyAMS.helpers.scrollTo('#main', target, { offset: -15 });
				});
			});
	}

	const callback = request.getResponseHeader('X-AMS-Callback');
	if (callback) {
		const options = request.getResponseHeader('X-AMS-Callback-Options') || "{}";
		MyAMS.core.executeFunctionByName(callback, document, form, settings, options,
			result, status, request);
	}
	form.trigger('after-submit.ams.form', [result]);
}


/**
 * Reset AJAX form after submit
 * 
 * @param form: current form
 * @param settings: computed form settings
 * @param button: button used to submit the form, if any
 */
export function resetFormAfterSubmit(form, settings, button) {
	if (form.data('submitted')) {
		settings.resetSubmitButton(form, settings, button);
		form.data('submitted', false);
		form.removeData('ams-submit-button');
		form.trigger('after-reset.ams.form');
		if (form.data('ams-reset-after-submit')) {
			form.get(0).reset();
		}
	}
}


/**
 * Reset form after submit error
 *
 * @param form: current form
 * @param settings: computed form settings
 * @param target: previous form target
 */
export function resetFormAfterError(form, settings, target) {
	$('i', target)
		.removeClass('fa-spin')
		.removeClass('fa-cog')
		.addClass('fa-ambulance');
}


// get form download target
export function getFormDownloadTarget(form, settings) {
	return settings.downloadTarget;
}


// initialize download target
export function initFormDownloadTarget(form, settings, target, ajaxSettings) {
	let iframe = $(`iframe[name="${target}"]`);
	if (!iframe.exists()) {
		iframe = $('<iframe>').attr('name', target)
			.hide()
			.appendTo(MyAMS.dom.root);
	}
	$.extend(ajaxSettings, {
		iframe: true,
		iframeTarget: iframe
	});
}


// reset if download target
export function resetFormDownloadTarget(form, settings, button, target, ajaxSettings) {
	const
		modal = form.closest('.modal-dialog'),
		keepModal = settings.keepModalOpen;
	if (modal.exists() && (keepModal !== true)) {
		MyAMS.require('modal').then(() => {
			MyAMS.modal.close(modal);
		});
	}
	if (!ajaxSettings.progress) {
		setTimeout(() => {
			settings.resetAfterSubmit(form, settings, button);
			MyAMS.ajax && MyAMS.ajax.stop();
			MyAMS.form.resetChanged(form);
		}, settings.resetTimeout);
	}
}


/**
 * Global module initialization
 */
if (window.MyAMS) {
	if (MyAMS.env.bundle) {
		MyAMS.config.modules.push('form');
	} else {
		MyAMS.form = form;
		console.debug("MyAMS: form module loaded...");
	}
}
