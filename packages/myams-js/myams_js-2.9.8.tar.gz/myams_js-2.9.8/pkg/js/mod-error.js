/* global MyAMS */
/**
 * MyAMS errors management
 */

import 'jsrender';

const $ = MyAMS.$;


const ERRORS_TEMPLATE_STRING = `
	<div class="alert alert-{{:status}}" role="alert">
		<button type="button" class="close" data-dismiss="alert" 
				aria-label="{{*: MyAMS.i18n.BTN_CLOSE }}">
			<i class="fa fa-times" aria-hidden="true"></i>	
		</button>
		{{if header}}
		<h5 class="alert-heading">{{:header}}</h5>
		{{/if}}
		{{if message}}
		<p>{{:message}}</p>
		{{/if}}
		{{if messages}}
		<ul>
		{{for messages}}
			<li>
				{{if header}}<strong>{{:header}} :</strong>{{/if}}
				{{:message}}
			</li>
		{{/for}}
		</ul>
		{{/if}}
		{{if widgets}}
		<ul>
		{{for widgets}}
			<li>
				{{if header}}<strong>{{:header}} :</strong>{{/if}}
				{{:message}}
			</li>
		{{/for}}
		</ul>
		{{/if}}
	</div>`;

const ERROR_TEMPLATE = $.templates({
	markup: ERRORS_TEMPLATE_STRING,
	allowCode: true
});


export const error = {

	/**
	 * Show errors as alert in given parent
	 *
	 * @param parent: alert parent element
	 * @param errors: errors properties
	 */
	showErrors: (parent, errors) => {
		return new Promise((resolve, reject) => {
			if (!parent) {
				parent = $('#content >section:first-child >div:first-child');
			}
			if (typeof errors === 'string') {  // simple error message
				MyAMS.require('i18n', 'alert').then(() => {
					MyAMS.alert.alert({
						parent: parent,
						status: 'danger',
						header: MyAMS.i18n.ERROR_OCCURED,
						message: errors
					});
				}).then(resolve, reject);
			} else if ($.isArray(errors)) {  // array of messages
				MyAMS.require('i18n', 'alert').then(() => {
					MyAMS.alert.alert({
						parent: parent,
						status: 'danger',
						header: MyAMS.i18n.ERRORS_OCCURED,
						message: errors
					});
				}).then(resolve, reject);
			} else {  // full errors with widgets
				MyAMS.require('i18n', 'ajax', 'alert', 'form').then(() => {
					// clear previous alerts
					MyAMS.form.clearAlerts(parent);
					// create new alert
					const messages = [];
					for (const message of errors.messages || []) {
						if (typeof message === 'string') {
							messages.push({
								header: null,
								message: message
							});
						} else {
							messages.push(message);
						}
					}
					for (const widget of errors.widgets || []) {
						messages.push({
							header: widget.label,
							message: widget.message
						});
					}
					const
						header = errors.header ||
							(messages.length > 1 ? MyAMS.i18n.ERRORS_OCCURED : MyAMS.i18n.ERROR_OCCURED),
						props = {
							status: 'danger',
							header: header,
							message: errors.error || null,
							messages: messages
						};
					$(ERROR_TEMPLATE.render(props)).prependTo(parent);
					// update status of invalid widgets
					for (const widget of errors.widgets || []) {
						let input;
						if (widget.id) {
							input = $(`#${widget.id}`, parent);
						} else {
							input = $(`[name="${widget.name}"]`, parent);
						}
						if (input.exists()) {
							MyAMS.form.setInvalid(parent, input, widget.message);
						}
						// open parent fieldsets switchers
						const fieldsets = input.parents('fieldset.switched');
						fieldsets.each((idx, elt) => {
							$('legend.switcher', elt).click();
						});
						// open parent tab panels
						const panels = input.parents('.tab-pane');
						panels.each((idx, elt) => {
							const
								panel = $(elt),
								tabs = panel.parents('.tab-content')
									.siblings('.nav-tabs');
							$(`li:nth-child(${panel.index() + 1})`, tabs)
								.addClass('is-invalid');
							$('li.is-invalid:first a', tabs)
								.click();
						});
					}
					MyAMS.require('helpers').then(() => {
						let scrollBox = parent.parents('.modal-body');
						if (!scrollBox.exists()) {
							scrollBox = $('#main');
						}
						MyAMS.helpers.scrollTo(scrollBox, parent, { offset: -15 });
					});
				}).then(resolve, reject);
			}
		});
	},

	/**
	 * Display message for standard HTTP error
	 *
	 * @param error: error object
	 */
	showHTTPError: (error) => {
		return new Promise((resolve, reject) => {
			MyAMS.require('alert').then(() => {
				MyAMS.alert.messageBox({
					status: 'error',
					title: error.title,
					message: error.message,
					hideTimestamp: false,
					timeout: 0
				});
			}).then(resolve, reject);
		});
	}
};


/**
 * Global module initialization
 */
if (window.MyAMS) {
	if (MyAMS.env.bundle) {
		MyAMS.config.modules.push('error');
	} else {
		MyAMS.error = error;
		console.debug("MyAMS: error module loaded...");
	}
}
