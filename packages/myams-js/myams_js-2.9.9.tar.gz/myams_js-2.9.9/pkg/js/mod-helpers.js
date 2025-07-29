/* global MyAMS */
/**
 * MyAMS generic helpers
 */

const $ = MyAMS.$;


export const helpers = {

	/**
	 * Click handler used to clear input
	 */
	clearValue: (evt) => {
		const target = $(evt.currentTarget).data('target');
		if (target) {
			$(target).val(null);
		}
	},

	/**
	 * Click handler used to clear datetime input
	 */
	clearDatetimeValue: (evt) => {
		const
			target = $(evt.currentTarget).data('target'),
			picker = $(target).data('datetimepicker');
		if (picker) {
			picker.date(null);
		}
	},

	/**
	 * Scroll anchor parent element to given anchor
	 *
	 * @param anchor: scroll target
	 * @param parent: scroll parent
	 * @param props: scroll properties
	 */
	scrollTo: (parent='#content', anchor, {...props}) => {
		if (typeof anchor === 'string') {
			anchor = $(anchor);
		}
		if (anchor.exists()) {
			MyAMS.require('ajax').then(() => {
				MyAMS.ajax.check($.fn.scrollTo,
					`${MyAMS.env.baseURL}../ext/jquery-scrollto${MyAMS.env.extext}.js`).then(() => {
					$(parent).scrollTo(anchor, props);
				});
			});
		}
	},

	/**
	 * Store location hash when redirecting to log in form
	 *
	 * This helper is used to store window location hash into form input, to redirect
	 * user correctly after login.
	 */
	setLoginHash: () => {
		const
			form = $('#login_form'),
			hash = $(`input[name="login_form.widgets.hash"]`, form);
		hash.val(window.location.hash);
	},

	/**
	 * SEO input helper
	 *
	 * This helper is used to display a small coloured progress bar below a text input
	 * to display its SEO quality based on text length.
	 */
	setSEOStatus: (evt) => {
		const
			input = $(evt.target),
			progress = input.siblings('.progress').children('.progress-bar'),
			length = Math.min(input.val().length, 100);
		let status = 'success';
		if (length < 20 || length > 80) {
			status = 'danger';
		} else if (length < 40 || length > 66) {
			status = 'warning';
		}
		progress.removeClassPrefix('bg-')
				.addClass('bg-' + status)
				.css('width', length + '%');
	},

	/**
	 * Select2 change helper
	 *
	 * This helper is used to handle a change event on a Select2 input. Data attributes
	 * defined on Select2 input can be used to define behaviour of this helper:
	 *  - data-ams-select2-helper-type: can be set to "html" when HTML code is loaded via a
	 *    webservice call, and included into a *target* element
	 *  - data-ams-select2-helper-url: remote webservice URL
	 *  - data-ams-select2-helper-target: CSS selector of a DOM element which will receive
	 *    result of a webservice call
	 *  - data-ams-select2-helper-argument: name of the argument used to call webservice; if
	 *    not defined, the used name is 'value'; this argument is filled with the selected value
	 *    of the Select2 input
	 *  - data-ams-select2-helper-callback: name of a callback function which can be used to
	 *    handle webservice result; if no callback is defined, the webservice result will be
	 *    inserted directly into defined target
	 */
	select2ChangeHelper: (evt) => {
		return new Promise((resolve, reject) => {

			const
				source = $(evt.currentTarget),
				data = source.data(),
				target = $(data.amsSelect2HelperTarget),
				params = {};
			let callback;
			switch (data.amsSelect2HelperType) {

				case 'html':
					target.html('<div class="text-center"><i class="fas fa-2x fa-spinner fa-spin"></i></div>');
					params[data.amsSelect2HelperArgument || 'value'] = source.val();
					$.get(data.amsSelect2HelperUrl, params).then((result) => {
						callback = MyAMS.core.getFunctionByName(data.amsSelect2HelperCallback) || ((result) => {
							if (result) {
								target.html(result);
								MyAMS.core.initContent(target).then(() => {
									resolve();
								});
							} else {
								target.empty();
								resolve();
							}
						});
						callback(result);
					}).catch(() => {
						target.empty();
						reject();
					});
					break;

				default:
					callback = data.amsSelect2HelperCallback;
					if (callback) {
						MyAMS.core.executeFunctionByName(callback, source, data);
						resolve();
					}
			}
		});
	},

	/**
	 * Refresh a DOM element with content provided in
	 * the <code>options</code> object.
	 *
	 * @param form: optional parent element
	 * @param options: element properties:
	 *   - object_id: ID of the refreshed element
	 *   - content: new element content
	 */
	refreshElement: (form, options) => {
		return new Promise((resolve, reject) => {
			let element = $(`[id="${options.object_id}"]`);
			MyAMS.core.executeFunctionByName(MyAMS.config.clearContent, document, element).then(() => {
				element.replaceWith($(options.content));
				element = $(`[id="${options.object_id}"]`);
				const parent = element.parents().first();
				MyAMS.core.executeFunctionByName(MyAMS.config.initContent, document, parent).then(() => {
					resolve(element);
				}, reject);
			}, reject);
		});
	},

	/**
	 * Hide DOM element
	 *
	 * @param form: optional parent element
	 * @param options: element properties:
	 *   - selector: JQuery object selector
	 */
	hideElement: (form, options) => {
		$(options.selector, form).hide();
	},

	/**
	 * Remove DOM element
	 *
	 * @param form: optional parent element
	 * @param options: element properties:
	 *   - selector: JQuery object selector
	 */
	removeElement: (form, options) => {
		$(options.selector, form).remove();
	},

	/**
	 * Refresh a form widget with content provided in
	 * the <code>options</code> object
	 *
	 * @param form: optional parent form
	 * @param options: updated widget properties:
	 *   - widget_id: ID of the refreshed widget
	 *   - content: new element content
	 */
	refreshWidget: (form, options) => {
		return new Promise((resolve, reject) => {
			let widget = $(`[id="${options.widget_id}"]`),
				group = widget.parents('.widget-group');
			MyAMS.core.executeFunctionByName(MyAMS.config.clearContent, document, group).then(() => {
				group.replaceWith($(options.content));
				widget = $(`[id="${options.widget_id}"]`);
				group = widget.parents('.widget-group');
				MyAMS.core.executeFunctionByName(MyAMS.config.initContent, document, group).then(() => {
					resolve(widget);
				}, reject);
			}, reject);
		});
	},

	/**
	 * Refresh a whole table with content provided in
	 * the <code>options</code> object
	 *
	 * @param form: optional parent form
	 * @param options: updated table properties:
	 *    - table_id: ID of the refreshed table
	 *    - content: new table HTML content
	 */
	refreshTable: (form, options) => {
		return new Promise((resolve, reject) => {
			const selector = `table[id="${options.table_id}"]`;
			let table = $(selector);
			if (!table.exists()) {
				return;
			}
			if (table.hasClass('datatable')) {
				const dtTable = table.DataTable();
				if (dtTable) {
					dtTable.destroy();
				}
			}
			table.replaceWith($(options.content));
			table = $(selector);
			MyAMS.core.executeFunctionByName(MyAMS.config.initContent,
				document, table.parent()).then(() => {
				resolve(table);
			}, reject);
		});
	},

	/**
	 * Add new row to table
	 *
	 * @param form: optional parent form
	 * @param options: added row properties:
	 *    - table_id: updated table ID
	 *    - row_id: updated row ID
	 *    - data: updated row data
	 *    - content: updated row HTML content
	 */
	addTableRow: (form, options) => {
		return new Promise((resolve, reject) => {
			const
				selector = `table[id="${options.table_id}"]`,
				table = $(selector),
				dtTable = table.DataTable();
			let newRow;
			if (options.data) {
				dtTable.rows.add(options.data).draw();
				newRow = $(`tr[id="${options.row_id}"]`, table);
				resolve(newRow);
			} else {
				newRow = $(options.content);
				dtTable.rows.add(newRow).draw();
				MyAMS.core.executeFunctionByName(MyAMS.config.initContent,
					document, newRow).then(() => {
					resolve(newRow);
				}, reject);
			}
		});
	},

	/**
	 * Refresh a table row with content provided in
	 * the <code>options</code> object
	 *
	 * @param form: optional parent form
	 * @param options: updated row properties:
	 *   - row_id: ID of the refreshed row
	 *   - content: new row content
	 */
	refreshTableRow: (form, options) => {
		return new Promise((resolve, reject) => {
			const
				selector = `tr[id="${options.row_id}"]`,
				row = $(selector),
				table = row.parents('table').first();
			if (options.data) {
				if ($.fn.DataTable) {
					const dtTable = table.DataTable();
					if (typeof options.data === 'string') {
						dtTable.row(selector).remove();
						dtTable.row.add($(options.data)).draw();
					} else {
						dtTable.row(selector).data(options.data).draw();
					}
					resolve(row);
				} else {
					reject('No DataTable plug-in available!');
				}
			} else {
				const newRow = $(options.content);
				row.replaceWith(newRow);
				MyAMS.core.executeFunctionByName(MyAMS.config.initContent,
					document, newRow).then(() => {
					resolve(newRow);
				}, reject);
			}
		});
	},

	/**
	 * Delete a table row with given ID
	 *
	 * @param form: optional parent form
	 * @param options: removed row properties:
	 *   - row_id: ID of the deleted row
	 */
	deleteTableRow: (form, options) => {
		return new Promise((resolve, reject) => {
			const
				selector = `tr[id="${options.row_id}"]`,
				row = $(selector),
				table = row.parents('table').first();
			if ($.fn.DataTable) {
				const dtTable = table.DataTable();
				dtTable.row(selector).remove();
				dtTable.draw();
			} else {
				row.remove();
			}
		});
	},

	/**
	 * Refresh a single image with content provided in
	 * the <code>options</code> object.
	 *
	 * @param form: optional parent element
	 * @param options: image properties:
	 *   - image_id: ID of the refreshed image
	 *   - src: new image source URL
	 */
	refreshImage: (form, options) => {
		const image = $(`[id="${options.image_id}"]`);
		image.attr('src', options.src);
	},

	/**
	 * Move given element to the end of it's parent
	 *
	 * @param element: the element to be moved
	 * @returns {*}
	 */
	moveElementToParentEnd: (element) => {
		const parent = element.parent();
		return element.detach()
			.appendTo(parent);
	},

	/**
	 * Add given element to the end of specified parent
	 *
	 * @param source: event source
	 * @param element: the provided element
	 * @param parent: the parent to which element should be added
	 * @param props: additional props
	 * @returns {*}
	 */
	addElementToParent: (source, {element, parent, ...props}) => {
		element = $(element);
		parent = $(parent);
		const result = element.appendTo(parent);
		if (props.scrollTo) {
			MyAMS.helpers.scrollTo(props.scrollParent, element);
		}
		return result;
	},

	/**
	 * Toggle dropdown associated with given event target
	 *
	 * @param evt: source event
	 */
	hideDropdown: (evt) => {
		$(evt.target).closest('.dropdown-menu').dropdown('hide');
	}
};


/**
 * Global module initialization
 */
if (window.MyAMS) {
	if (MyAMS.env.bundle) {
		MyAMS.config.modules.push('helpers');
	} else {
		MyAMS.helpers = helpers;
		console.debug("MyAMS: helpers module loaded...");
	}
}
