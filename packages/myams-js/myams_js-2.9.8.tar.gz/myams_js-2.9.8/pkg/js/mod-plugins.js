/* global MyAMS, bsCustomFileInput */
/**
 * MyAMS standard plugins
 */

const $ = MyAMS.$;

if (!$.templates) {
	const jsrender = require('jsrender');
	$.templates = jsrender.templates;
}


/**
 * FullCalendar plugin
 */
export function calendar(element) {
	return new Promise((resolve, reject) => {
		const calendars = $('.calendar', element);
		if (calendars.length > 0) {
			MyAMS.ajax.check(window.FullCalendar,
				`${MyAMS.env.baseURL}../ext/fullcalendar-global${MyAMS.env.extext}.js`).then((firstLoad) => {
				calendars.each((idx, elt) => {
					const
						element = $(elt),
						data = element.data(),
						defaultOptions = {
							plugins: [],
							initialView: 'dayGridMonth',
							themeSystem: 'bootstrap',
							locale: $('html').attr('lang'),
							headerToolbar: {
								start: 'title',
								center: 'today',
								right: 'prev,next'
							},
							bootstrapFontAwesome: {
								prev: 'fa-chevron-left',
								next: 'fa-chevron-right'
							},
							firstDay: 1,
							weekNumberCalculation: 'ISO'
						};
					let settings = $.extend({}, defaultOptions, data.calendarOptions || data.options);
					settings = MyAMS.core.executeFunctionByName(
						data.amsCalendarInitCallback || data.amsInit,
						document, element, settings) || settings;
					const veto = {veto: false};
					element.trigger('before-init.ams.calendar', [element, settings, veto]);
					if (veto.veto) {
						return;
					}
					const calendar = new FullCalendar.Calendar(elt, settings);
					element.trigger('after-init.ams.calendar', [element, calendar]);
					calendar.render();
				});
				resolve(calendars);
			}, reject);
		} else {
			resolve(null);
		}
	});
}


/**
 * Fieldset checker plug-in
 *
 * A checker is like a simple switcher, but also provides a checkbox which is used
 * as "switcher" input field.
 *
 * The "checker" class is applied to the fieldset legend; checkbox is created automatically
 * by the plug-in.
 * Check options are given as data attributes, all prefixed with "ams-checker-":
 *  - state: is 'off' by default; can be set to 'on' to automatically activate the checker
 *  - mode: is 'hide' by default, which make the fieldset hidden when the checker is not activated;
 *    you cna set it to "disable" to make fieldset content visible but disabled when the checker
 *    is not activated
 *  - fieldname: is the name of the input checkbox created by the plug-in
 *  - value: this is the "checked" value of the main checkbox field
 *  - readonly: if "true", the checkbox is disabled and in read-only mode
 *  - hidden-prefix: if not null, this is a prefix which will be assigned to an additional
 *    hidden input field, updated automatically when the checker is switched; the name of the
 *    hidden input if made of this prefix, followed by the "fieldname" value
 *  - value-on: this is the "checked" value of the hidden input; "true" by default
 *  - value-off: this is the "unchecked" value of the hidden input; "false" by default
 *  - marker: if not null, another hidden input with a fixed value of 1 will be created; the name
 *    of this input will be the "fieldname" value followed by this "marker" value
 *  - change-handler: this optional handler will be called on checker switch
 *  - cancel-default: if "true", the default behaviour will not be executed on checker switch
 */

const CHECKER_TEMPLATE_STRING = `
	<span class="custom-control custom-switch">
		<input type="checkbox"
			   id="{{: fieldId }}" name="{{: fieldName }}"
			   class="custom-control-input checker"
			   {{if checked}}checked{{/if}}
			   {{if readonly}}disabled{{/if}}
			   value="{{: value }}" />
		{{if prefix}}
		<input type="hidden" class="prefix"
			   id="{{: prefix}}{{: fieldName}}_prefix"
			   name="{{: prefix}}{{: fieldName}}"
			   value="{{if state==='on'}}{{: checkedValue}}{{else}}{{: uncheckedValue}}{{/if}}" />
		{{else marker}}
		<input type="hidden" class="marker"
			   name="{{: fieldName}}{{: marker}}"
			   value="1" />
		{{/if}}
		<label for="{{: fieldId }}"
			   class="custom-control-label">
			{{: legend }}
		</label>
	</span>
`;

const CHECKER_TEMPLATE = $.templates({
	markup: CHECKER_TEMPLATE_STRING
});

export function checker(element) {
	return new Promise((resolve) => {
		const checkers = $('legend.checker', element);
		if (checkers.length > 0) {
			checkers.each((idx, elt) => {
				const
					legend = $(elt),
					data = legend.data();
				if (!data.amsChecker) {
					const
						fieldset = legend.parent('fieldset'),
						state = data.amsCheckerState || data.amsState,
						checked = fieldset.hasClass('switched') || (state === 'on'),
						fieldName = data.amsCheckerFieldname || data.amsFieldname || `checker_${MyAMS.core.generateId()}`,
						fieldId = fieldName.replace(/\./g, '_'),
						prefix = data.amsCheckerHiddenPrefix || data.amsHiddenPrefix,
						marker = data.amsCheckerMarker || data.amsMarker || false,
						checkerMode = data.amsCheckerMode || data.amsMode || 'hide',
						checkedValue = data.amsCheckerValueOn || data.amsValueOn || 'true',
						uncheckedValue = data.amsCheckerValueOff || data.amsValueOff || 'false',
						value = data.amsCheckerValue || data.amsValue,
						readonly = data.amsCheckerReadonly || data.amsReadonly,
						props = {
							legend: legend.text(),
							fieldName: fieldName,
							fieldId: fieldId,
							value: value || true,
							checked: checked,
							readonly: readonly,
							prefix: prefix,
							state: state,
							checkedValue: checkedValue,
							uncheckedValue: uncheckedValue,
							marker: marker
						},
						veto = {veto: false};
					legend.trigger('before-init.ams.checker', [legend, props, veto]);
					if (veto.veto) {
						return;
					}
					legend.html(CHECKER_TEMPLATE.render(props));
					$('input', legend).change((evt) => {
						const
							input = $(evt.target),
							checked = input.is(':checked'),
							veto = {veto: false};
						legend.trigger('before-switch.ams.checker', [legend, veto]);
						if (veto.veto) {
							input.prop('checked', !checked);
							return;
						}
						MyAMS.core.executeFunctionByName(data.amsCheckerChangeHandler ||
							data.amsChangeHandler, document, legend, checked);
						if (!data.amsCheckerCancelDefault && !data.amsCancelDefault) {
							const prefix = input.siblings('.prefix');
							if (checkerMode === 'hide') {
								if (checked) {
									fieldset.removeClass('switched');
									prefix.val(checkedValue);
									legend.trigger('opened.ams.checker', [legend]);
								} else {
									fieldset.addClass('switched');
									prefix.val(uncheckedValue);
									legend.trigger('closed.ams.checker', [legend]);
								}
							} else {
								fieldset.prop('disabled', !checked);
								prefix.val(checked ? checkedValue : uncheckedValue);
							}
						}
					});
					legend.closest('form').on('reset', () => {
						const checker = $('.checker', legend);
						if (checker.prop('checked') !== checked) {
							checker.click();
						}
					});
					if (!checked) {
						if (checkerMode === 'hide') {
							fieldset.addClass('switched');
						} else {
							fieldset.prop('disabled', true);
						}
					}
					legend.trigger('after-init.ams.checker', [legend]);
					legend.data('ams-checker', true);
				}
			});
			resolve(checkers);
		} else {
			resolve(null);
		}
	});
}


/**
 * Colorpicker menu plug-in
 */

export function colorPicker(element) {
	return new Promise((resolve, reject) => {
		const inputs = $('.color', element);
		if (inputs.length > 0) {
			MyAMS.require('ajax').then(() => {
				MyAMS.ajax.check($.fn.colorpicker,
					`${MyAMS.env.baseURL}../ext/bootstrap-colorpicker${MyAMS.env.extext}.js`).then((firstLoad) => {
					const required = [];
					if (firstLoad) {
						required.push(MyAMS.core.getCSS(`${MyAMS.env.baseURL}../../css/ext/bootstrap-colorpicker${MyAMS.env.extext}.css`,
							'colorpicker'));
					}
					$.when.apply($, required).then(() => {
						inputs.each((idx, elt) => {
							const
								input = $(elt),
								data = input.data(),
								dataOptions = {
									format: data.amsColorpickerFormat || data.amsFormat || 'hex',
									useHashPrefix: (data.amsColorpickerUseHashPrefix || data.amsUseHashPrefix || false) !== false,
									useAlpha: (data.amsColorpickerUseAlpha || data.amsUseAlpha || false) !== false,
									change: MyAMS.core.getFunctionByName(data.amsColorpickerChange || data.amsChange),
									colorpickerChange: MyAMS.core.getFunctionByName(data.amsColorpickerPickerChange || data.amsPickerChange),
									colorpickerCreate: MyAMS.core.getFunctionByName(data.amsColorpickerPickerCreate || data.amsPickerCreate),
									colorpickerDestroy: MyAMS.core.getFunctionByName(data.amsColorpickerPickerDestroy || data.amsPickerDestroy),
									colorpickerEnable: MyAMS.core.getFunctionByName(data.amsColorpickerPickerEnable || data.amsPickerEnable),
									colorpickerDisable: MyAMS.core.getFunctionByName(data.amsColorpickerPickerDisable || data.amsPickerDisable),
									colorpickerHide: MyAMS.core.getFunctionByName(data.amsColorpickerPickerHide || data.amsPickerHide),
									colorpickerInvalid: MyAMS.core.getFunctionByName(data.amsColorpickerPickerInvalid || data.amsPickerInvalid),
									colorpickerShow: MyAMS.core.getFunctionByName(data.amsColorpickerPickerShow || data.amsPickerShow),
									colorpickerUpdate: MyAMS.core.getFunctionByName(data.amsColorpickerPickerUpdate || data.amsPickerUpdate),
									mousemove: MyAMS.core.getFunctionByName(data.amsColorpickerMousemove || data.amsMousemove),
								};
							let settings = $.extend({}, dataOptions, data.amsColorpickerOptions || data.amsOptions);
							settings = MyAMS.core.executeFunctionByName(data.amsColorpickerInitCallback || data.amsInit,
								document, input, settings) || settings;
							const veto = {veto: false};
							input.trigger('before-init.ams.colorpicker', [input, settings, veto]);
							if (veto.veto) {
								return;
							}
							const plugin = input.colorpicker(settings);
							MyAMS.core.executeFunctionByName(data.amsColorpickerAfterInitCallback || data.amsAfterInit,
								document, input, plugin, settings);
							input.trigger('after-init.ams.colorpicker', [input, plugin]);
						});
						resolve(inputs);
					}, reject);
				}, reject);
			}, reject);
		} else {
			resolve(null);
		}
	});
}


/**
 * Context menu plug-in
 */

export function contextMenu(element) {
	return new Promise((resolve, reject) => {
		const menus = $('.context-menu', element);
		if (menus.length > 0) {
			MyAMS.require('menu').then(() => {
				menus.each((idx, elt) => {
					const
						menu = $(elt),
						data = menu.data(),
						options = {
							menuSelector: data.amsContextmenuSelector || data.amsMenuSelector
						};
					let settings = $.extend({}, options, data.amsContextmenuOptions || data.amsOptions);
					settings = MyAMS.core.executeFunctionByName(
						data.amsContextmenuInitCallback || data.amsInit,
						document, menu, settings) || settings;
					const veto = {veto: false};
					menu.trigger('before-init.ams.contextmenu', [menu, settings, veto]);
					if (veto.veto) {
						return;
					}
					const plugin = menu.contextMenu(settings);
					MyAMS.core.executeFunctionByName(
						data.amsContextmenuAfterInitCallback || data.amsAfterInit,
						document, menu, plugin, settings);
					menu.trigger('after-init.ams.contextmenu', [menu, plugin]);
				});
				resolve(menus);
			}, reject);
		} else {
			resolve(null);
		}
	});
}


/**
 * JQuery Datatable plug-in
 */

const _datatablesHelpers = {

	init: () => {

		// Add autodetect formats
		const types = $.fn.dataTable.ext.type;

		types.detect.unshift((data) => {
			if (data !== null && data.match(/^(0[1-9]|[1-2][0-9]|3[0-1])\/(0[1-9]|1[0-2])\/[0-3][0-9]{3}$/)) {
				return 'date-euro';
			}
			return null;
		});

		types.detect.unshift((data) => {
			if (data !== null && data.match(/^(0[1-9]|[1-2][0-9]|3[0-1])\/(0[1-9]|1[0-2])\/[0-3][0-9]{3} - ([0-1][0-9]|2[0-3]):[0-5][0-9]$/)) {
				return 'datetime-euro';
			}
			return null;
		});

		// Add sorting methods
		$.extend(types.order, {

			// numeric values using commas separators
			"numeric-comma-asc": (a, b) => {
				let x = a.replace(/,/, ".").replace(/ /g, '');
				let y = b.replace(/,/, ".").replace(/ /g, '');
				x = parseFloat(x);
				y = parseFloat(y);
				return ((x < y) ? -1 : ((x > y) ? 1 : 0));
			},
			"numeric-comma-desc": (a, b) => {
				let x = a.replace(/,/, ".").replace(/ /g, '');
				let y = b.replace(/,/, ".").replace(/ /g, '');
				x = parseFloat(x);
				y = parseFloat(y);
				return ((x < y) ? 1 : ((x > y) ? -1 : 0));
			},

			// date-euro column sorter
			"date-euro-pre": (a) => {
				const trimmed = $.trim(a);
				let x;
				if (trimmed !== '') {
					const frDate = trimmed.split('/');
					x = (frDate[2] + frDate[1] + frDate[0]) * 1;
				} else {
					x = 10000000; // = l'an 1000 ...
				}
				return x;
			},
			"date-euro-asc": (a, b) => {
				return a - b;
			},
			"date-euro-desc": (a, b) => {
				return b - a;
			},

			// datetime-euro column sorter
			"datetime-euro-pre": (a) => {
				const trimmed = $.trim(a);
				let x;
				if (trimmed !== '') {
					const frDateTime = trimmed.split(' - ');
					const frDate = frDateTime[0].split('/');
					const frTime = frDateTime[1].split(':');
					x = (frDate[2] + frDate[1] + frDate[0] + frTime[0] + frTime[1]) * 1;
				} else {
					x = 100000000000; // = l'an 1000 ...
				}
				return x;
			},
			"datetime-euro-asc": (a, b) => {
				return a - b;
			},
			"datetime-euro-desc": (a, b) => {
				return b - a;
			}
		});
	},

	/**
	 * Store reorder source before reorder
	 *
	 * @param evt: original event
	 * @param node: source node
	 */
	preReorder: function(evt, node) {
		const table = $(evt.target);
		table.data('ams-reorder-source', node);
	},

	/**
	 * Handle table rows reordering
	 *
	 * @param evt: original event
	 */
	reorderRows: function(evt) {
		return new Promise((resolve, reject) => {
			const
				table = $(evt.target),
				dtTable = table.DataTable(),
				data = table.data();
			// extract target and URL
			let target = data.amsReorderInputTarget,
				url = data.amsReorderUrl,
				ids;
			if (!(target || url)) {
				resolve();
			}
			// extract reordered rows IDs
			const
				rows = $('>tbody >tr', table),
				getter = MyAMS.core.getFunctionByName(data.amsReorderData) || 'data-ams-row-value';
			if (typeof getter === 'function') {
				ids = $.makeArray(rows).map(getter);
			} else {
				ids = rows.listattr(getter);
			}
			// set target input value (if any)
			const separator = data.amsReorderSeparator || ';';
			if (target) {
				target = $(target);
				if (target.exists()) {
					target.val(ids.join(separator));
				}
			} else {
				ids = ids.join(separator);
			}
			// call target URL (if any)
			if (url) {
				url = MyAMS.core.executeFunctionByName(url, document, table) || url;
				if (!(url.startsWith(window.location.protocol) || url.startsWith('/'))) {
					const location = table.data('ams-location');
					url = `${location || ''}/${url}`;
				}
				if (ids.length > 0) {
					let postData;
					if (data.amsReorderPostData) {
						postData = MyAMS.core.executeFunctionByName(data.amsReorderPostData,
							document, table, ids);
					} else {
						const attr = data.amsReorderPostAttr || 'order';
						postData = {};
						postData[attr] = ids;
					}
					MyAMS.require('ajax').then(() => {
						MyAMS.ajax.post(url, postData).then((result, status, xhr) => {
							$('td.sorter', table).each((idx, elt) => {
								$(elt).removeData().attr('data-order', idx);
								dtTable.row($(elt).parents('tr').get(0)).invalidate().draw();
							});
							const callback = data.amsReorderCallback;
							if (callback) {
								MyAMS.core.executeFunctionByName(callback, document,
									table, result, status, xhr).then((...results) => {
									resolve.apply(table, ...results);
								});
							} else {
								MyAMS.ajax
									.handleJSON(result, table.parents('.dataTables_wrapper'))
									.then(() => {
										resolve(result);
									});
							}
						}, reject);
					});
				}
			}
		});
	}
};

export function datatables(element) {
	const
		baseJS = `${MyAMS.env.baseURL}../ext/datatables/`,
		baseCSS = `${MyAMS.env.baseURL}../../css/ext/datatables/`;
	return new Promise((resolve, reject) => {
		const tables = $('.datatable', element);
		if (tables.length > 0) {
			MyAMS.ajax.check($.fn.dataTable,
				`${MyAMS.env.baseURL}../ext/datatables/jquery.dataTables${MyAMS.env.extext}.js`).then((firstLoad) => {
				const required = [];
				if (firstLoad) {
					required.push(MyAMS.core.getScript(`${baseJS}dataTables.bootstrap4${MyAMS.env.extext}.js`));
					required.push(MyAMS.core.getCSS(`${baseCSS}dataTables.bootstrap4${MyAMS.env.extext}.css`, 'datatables-bs4'));
				}
				$.when.apply($, required).then(() => {
					const
						css = {},
						bases = [],
						extensions = [],
						depends = [],
						loaded = {};
					tables.each((idx, elt) => {
						const
							table = $(elt),
							data = table.data();
						if (data.buttons === 'default') {
							table.attr('data-buttons', '["copy", "print"]');
							table.removeData('buttons');
							data.buttons = table.data('buttons');
						} else if (data.buttons === 'all') {
							table.attr('data-buttons', '["copy", "csv", "excel", "print", "pdf", "colvis"]');
							table.removeData('buttons');
							data.buttons = table.data('buttons');
						}
						if (data.autoFill && !loaded.autoFill && !$.fn.dataTable.AutoFill) {
							bases.push(`${baseJS}dataTables.autoFill${MyAMS.env.extext}.js`);
							extensions.push(`${baseJS}autoFill.bootstrap4${MyAMS.env.extext}.js`);
							css['dt-autofill-bs4'] = `${baseCSS}autoFill.bootstrap4${MyAMS.env.extext}.css`;
							loaded.autoFill = true;
						}
						if (data.buttons) {
							if (!loaded.buttons && !$.fn.dataTable.Buttons) {
								bases.push(`${baseJS}dataTables.buttons${MyAMS.env.extext}.js`);
								extensions.push(`${baseJS}buttons.bootstrap4${MyAMS.env.extext}.js`);
								extensions.push(`${baseJS}buttons.html5${MyAMS.env.extext}.js`);
								css['dt-buttons-bs4'] = `${baseCSS}buttons.bootstrap4${MyAMS.env.extext}.css`;
								loaded.buttons = true;
							}
							if ($.isArray(data.buttons)) {
								const buttonDefs = [];
								for (const button of data.buttons) {
									switch (button) {
										case 'copy':
											buttonDefs.push({
												extend: 'copyHtml5',
												exportOptions: {
													columns: ":not(.no-export):visible"
												}
											});
											break;
										case 'csv':
											buttonDefs.push({
												extend: 'csvHtml5',
												exportOptions: {
													columns: ":not(.no-export):visible"
												}
											});
											break;
										case 'excel':
											if (!loaded.buttons_excel && !$.fn.dataTable.ext.buttons.excelHtml5) {
												bases.push(`${baseJS}jszip${MyAMS.env.extext}.js`);
												loaded.buttons_excel = true;
											}
											buttonDefs.push({
												extend: 'excelHtml5',
												exportOptions: {
													columns: ":not(.no-export):visible"
												}
											});
											break;
										case 'pdf':
											if (!loaded.buttons_pdf && !window.pdfMake) {
												bases.push(`${baseJS}pdfmake${MyAMS.env.extext}.js`);
												extensions.push(`${baseJS}vfs_fonts${MyAMS.env.extext}.js`);
												loaded.buttons_pdf = true;
											}
											buttonDefs.push({
												extend: 'pdfHtml5',
												exportOptions: {
													columns: ":not(.no-export):visible"
												}
											});
											break;
										case 'print':
											if (!loaded.buttons_print && !$.fn.dataTable.ext.buttons.print) {
												depends.push(`${baseJS}buttons.print${MyAMS.env.extext}.js`);
												loaded.buttons_print = true;
											}
											buttonDefs.push({
												extend: 'print',
												exportOptions: {
													columns: ":not(.no-export):visible"
												}
											});
											break;
										case 'colvis':
											if (!loaded.buttons_colvis && !$.fn.dataTable.ext.buttons.colvis) {
												depends.push(`${baseJS}buttons.colVis${MyAMS.env.extext}.js`);
												loaded.buttons_colvis = true;
											}
											buttonDefs.push({
												extend: 'colvis'
											});
									}
								}
								data.buttons = buttonDefs;
							}
						}
						if (data.colReorder && !loaded.colReorder && !$.fn.dataTable.ColReorder) {
							bases.push(`${baseJS}dataTables.colReorder${MyAMS.env.extext}.js`);
							extensions.push(`${baseJS}colReorder.bootstrap4${MyAMS.env.extext}.js`);
							css['dt-colreorder-bs4'] = `${baseCSS}colReorder.bootstrap4${MyAMS.env.extext}.css`;
							loaded.colReorder = true;
						}
						if (data.fixedColumns && !loaded.fixedColumns && !$.fn.dataTable.FixedColumns) {
							bases.push(`${baseJS}dataTables.fixedColumns${MyAMS.env.extext}.js`);
							extensions.push(`${baseJS}fixedColumns.bootstrap4${MyAMS.env.extext}.js`);
							css['dt-fixedcolumns-bs4'] = `${baseCSS}fixedColumns.bootstrap4${MyAMS.env.extext}.css`;
							loaded.fixedColumns = true;
						}
						if (data.fixedHeader && !loaded.fixedHeader && !$.fn.dataTable.FixedHeader) {
							bases.push(`${baseJS}dataTables.fixedHeader${MyAMS.env.extext}.js`);
							extensions.push(`${baseJS}fixedHeader.bootstrap4${MyAMS.env.extext}.js`);
							css['dt-fixedheader-bs4'] = `${baseCSS}fixedHeader.bootstrap4${MyAMS.env.extext}.css`;
							loaded.fixedHeader = true;
						}
						if (data.keyTable && !loaded.keyTable && !$.fn.dataTable.KeyTable) {
							bases.push(`${baseJS}dataTables.keyTable${MyAMS.env.extext}.js`);
							extensions.push(`${baseJS}keyTable.bootstrap4${MyAMS.env.extext}.js`);
							css['dt-keytable-bs4'] = `${baseCSS}keyTable.bootstrap4${MyAMS.env.extext}.css`;
							loaded.keyTable = true;
						}
						if ((data.responsive !== false) && !loaded.responsive && !$.fn.dataTable.Responsive) {
							bases.push(`${baseJS}dataTables.responsive${MyAMS.env.extext}.js`);
							extensions.push(`${baseJS}responsive.bootstrap4${MyAMS.env.extext}.js`);
							css['dt-responsive-bs4'] = `${baseCSS}responsive.bootstrap4${MyAMS.env.extext}.css`;
							loaded.responsive = true;
						}
						if (data.rowGroup && !loaded.rowGroup && !$.fn.dataTable.RowGroup) {
							bases.push(`${baseJS}dataTables.rowGroup${MyAMS.env.extext}.js`);
							extensions.push(`${baseJS}rowGroup.bootstrap4${MyAMS.env.extext}.js`);
							css['dt-rowgroup-bs4'] = `${baseCSS}rowGroup.bootstrap4${MyAMS.env.extext}.css`;
							loaded.rowGroup = true;
						}
						if (data.rowReorder && !loaded.rowReorder && !$.fn.dataTable.RowReorder) {
							bases.push(`${baseJS}dataTables.rowReorder${MyAMS.env.extext}.js`);
							extensions.push(`${baseJS}rowReorder.bootstrap4${MyAMS.env.extext}.js`);
							css['dt-rowreorder-bs4'] = `${baseCSS}rowReorder.bootstrap4${MyAMS.env.extext}.css`;
							loaded.rowReorder = true;
						}
						if (data.scroller && !loaded.scroller && !$.fn.dataTable.Scroller) {
							bases.push(`${baseJS}dataTables.scroller${MyAMS.env.extext}.js`);
							extensions.push(`${baseJS}scroller.bootstrap4${MyAMS.env.extext}.js`);
							css['dt-scroller-bs4'] = `${baseCSS}scroller.bootstrap4${MyAMS.env.extext}.css`;
							loaded.scroller = true;
						}
						if (data.searchBuilder && !loaded.searchBuilder && !$.fn.dataTable.SearchBuilder) {
							bases.push(`${baseJS}dataTables.searchBuilder${MyAMS.env.extext}.js`);
							extensions.push(`${baseJS}searchBuilder.bootstrap4${MyAMS.env.extext}.js`);
							css['dt-searchbuilder-bs4'] = `${baseCSS}searchBuilder.bootstrap4${MyAMS.env.extext}.css`;
							loaded.searchBuilder = true;
						}
						if (data.searchPanes && !loaded.searchPanes && !$.fn.dataTable.SearchPanes) {
							if (!loaded.select && !$.fn.dataTable.select) {
								bases.push(`${baseJS}dataTables.select${MyAMS.env.extext}.js`);
								extensions.push(`${baseJS}select.bootstrap4${MyAMS.env.extext}.js`);
								css['dt-select-bs4'] = `${baseCSS}select.bootstrap4${MyAMS.env.extext}.css`;
								loaded.select = true;
							}
							extensions.push(`${baseJS}dataTables.searchPanes${MyAMS.env.extext}.js`);
							depends.push(`${baseJS}searchPanes.bootstrap4${MyAMS.env.extext}.js`);
							css['dt-searchpanes-bs4'] = `${baseCSS}searchPanes.bootstrap4${MyAMS.env.extext}.css`;
							loaded.searchPanes = true;
						}
						if (data.select && !loaded.select && !$.fn.dataTable.select) {
							bases.push(`${baseJS}dataTables.select${MyAMS.env.extext}.js`);
							extensions.push(`${baseJS}select.bootstrap4${MyAMS.env.extext}.js`);
							css['dt-select-bs4'] = `${baseCSS}select.bootstrap4${MyAMS.env.extext}.css`;
							loaded.select = true;
						}
						if (data.stateRestore && !loaded.stateRestore && !$.fn.dataTables.stateRestore) {
							bases.push(`${baseJS}dataTables.stateRestore${MyAMS.env.extext}.js`);
							extensions.push(`${baseJS}stateRestore.bootstrap4${MyAMS.env.extext}.js`);
							css['dt-staterestore-bs4'] = `${baseCSS}stateRestore.bootstrap4${MyAMS.env.extext}.css`;
							loaded.stateRestore = true;
						}
					});
					$.when.apply($, bases.map(MyAMS.core.getScript)).then(() => {
						return $.when.apply($, extensions.map(MyAMS.core.getScript)).then(() => {
							return $.when.apply($, depends.map(MyAMS.core.getScript)).then(() => {
								if (firstLoad) {
									_datatablesHelpers.init();
								}
								for (const [name, url] of Object.entries(css)) {
									MyAMS.core.getCSS(url, name);
								}
								tables.each((idx, elt) => {
									const table = $(elt);
									if ($.fn.dataTable.isDataTable(table)) {
										return;
									}
									const data = table.data();

									// initialize dom property
									let dom = data.amsDatatableDom || data.amsDom || data.dom || '';
									if (!dom) {
										if (data.buttons) {
											dom += "<'row px-4 float-right'B>";
										}
										if (data.searchBuilder) {
											dom += "Q";
										}
										if (data.searchPanes) {
											dom += "P";
										}
										if (data.searching !== false || data.lengthChange !== false) {
											dom += "<'row px-2'";
											if (data.searching !== false) {
												dom += "<'col-sm-6 col-md-8'f>";
											}
											if (data.lengthChange !== false) {
												dom += "<'col-sm-6 col-md-4'l>";
											}
											dom += ">";
										}
										dom += "<'row'<'col-sm-12'tr>>";
										if (data.info !== false || data.paging !== false) {
											dom += "<'row px-2 py-1'";
											if (data.info !== false) {
												dom += "<'col-sm-12 col-md-5'i>";
											}
											if (data.paging !== false) {
												dom += "<'col-sm-12 col-md-7'p>";
											}
											dom += ">"
										}
									}
									if (!data.buttons && !data.searchBuilder && !data.searchPanes &&
										(data.searching === false) || (data.lengthChange === false)) {
										table.siblings('h3').addClass('mb-0');
									}

									// initialize default options
									const
										defaultOptions = {
											language: data.amsDatatableLanguage || data.amsLanguage ||
												MyAMS.i18n.plugins.datatables,
											responsive: true,
											dom: dom
										};

									// initialize sorting
									let order = data.amsDatatableOrder || data.amsOrder;
									if (typeof order === 'string') {
										const orders = order.split(';');
										order = [];
										for (const col of orders) {
											const colOrder = col.split(',');
											colOrder[0] = parseInt(colOrder[0]);
											order.push(colOrder);
										}
									}
									if (order) {
										defaultOptions.order = order;
									}

									// initialize columns definition based on header settings
									const
										heads = $('thead th', table),
										columns = [];
									heads.each((idx, th) => {
										columns[idx] = $(th).data('ams-column') || {};
									});
									const sortables = heads.listattr('data-ams-sortable');
									for (const iterator of sortables.entries()) {
										const [idx, sortable] = iterator;
										if (data.rowReorder) {
											columns[idx].sortable = false;
										} else if (sortable !== undefined) {
											columns[idx].sortable =
												typeof sortable === 'string' ? JSON.parse(sortable) : sortable;
										}
									}
									const types = heads.listattr('data-ams-type');
									for (const iterator of types.entries()) {
										const [idx, stype] = iterator;
										if (stype !==  undefined) {
											columns[idx].type = stype;
										}
									}
									defaultOptions.columns = columns;

									// initialize final settings and initialize plug-in
									let settings = $.extend({}, defaultOptions, data.amsDatatableOptions || data.amsOptions);
									settings = MyAMS.core.executeFunctionByName(
										data.amsDatatableInitCallback || data.amsInit,
										document, table, settings) || settings;
									const veto = {veto: false};
									table.trigger('before-init.ams.datatable', [table, settings, veto]);
									if (veto.veto) {
										return;
									}
									setTimeout(() => {
										if ($.fn.dataTable.Buttons) {
											$.fn.dataTable.Buttons.defaults.dom.button.className = data.amsDatatableButtonsClassname ||
												data.amsButtonsClassname || 'btn btn-sm btn-secondary';
										}
										const plugin = table.DataTable(settings);
										MyAMS.core.executeFunctionByName(
											data.amsDatatableAfterInitCallback || data.amsAfterInit,
											document, table, plugin, settings);
										table.trigger('after-init.ams.datatable', [table, plugin]);

										// set reorder events
										if (settings.rowReorder) {
											plugin.on('pre-row-reorder', MyAMS.core.getFunctionByName(
													data.amsDatatablePreReorder || data.amsPreReorder) ||
												_datatablesHelpers.preReorder);
											plugin.on('row-reorder', MyAMS.core.getFunctionByName(
													data.amsDatatableReordered || data.amsReordered) ||
												_datatablesHelpers.reorderRows);
										}
									}, 100);
								});
								resolve(tables);
							}, reject);
						}, reject);
					}, reject);
				}, reject);
			}, reject);
		} else {
			resolve(null);
		}
	});
}


/**
 * Bootstrap 4 Tempus/Dominus date/time picker
 */
export function datetime(element) {
	return new Promise((resolve, reject) => {
		const inputs = $('.datetime', element);
		if (inputs.length > 0) {
			MyAMS.ajax.check(window.moment,
				`${MyAMS.env.baseURL}../ext/moment${MyAMS.env.extext}.js`).then(() => {
				MyAMS.ajax.check($.fn.datetimepicker,
					`${MyAMS.env.baseURL}../ext/tempusdominus-bootstrap4${MyAMS.env.extext}.js`).then((firstLoad) => {
					const required = [];
					if (firstLoad) {
						required.push(MyAMS.core.getCSS(
							`${MyAMS.env.baseURL}../../css/ext/tempusdominus-bootstrap4${MyAMS.env.extext}.css`,
							'tempusdominus'));
					}
					$.when.apply($, required).then(() => {
						inputs.each((idx, elt) => {
							const
								input = $(elt),
								data = input.data(),
								defaultOptions = {
									locale: data.amsDatetimeLanguage || data.amsLanguage || MyAMS.i18n.language,
									icons: {
										time: 'far fa-clock',
										date: 'far fa-calendar',
										up: 'fas fa-arrow-up',
										down: 'fas fa-arrow-down',
										previous: 'fas fa-chevron-left',
										next: 'fas fa-chevron-right',
										today: 'far fa-calendar-check-o',
										clear: 'far fa-trash',
										close: 'far fa-times'
									},
									date: input.val(),
									format: data.amsDatetimeFormat || data.amsFormat
								};
							let settings = $.extend({}, defaultOptions, data.datetimeOptions || data.options);
							settings = MyAMS.core.executeFunctionByName(
								data.amsDatetimeInitCallback || data.amsInit,
								document, input, settings) || settings;
							const veto = {veto: false};
							input.trigger('before-init.ams.datetime', [input, settings, veto]);
							if (veto.veto) {
								return;
							}
							input.datetimepicker(settings);
							const plugin = input.data('datetimepicker');
							if (data.amsDatetimeIsoTarget || data.amsIsoTarget) {
								input.on('change.datetimepicker', (evt) => {
									const
										source = $(evt.currentTarget),
										data = source.data(),
										target = $(data.amsDatetimeIsoTarget || data.amsIsoTarget);
									target.val(evt.date ? evt.date.toISOString(true) : null);
								});
							}
							input.trigger('after-init.ams.datetime', [input, plugin]);
						});
						resolve(inputs);
					});
				}, reject);
			}, reject);
		} else {
			resolve(null);
		}
	});
}


/**
 * JQuery-UI drag and drop plug-ins
 */

export function dragdrop(element) {
	return new Promise((resolve, reject) => {
		const dragitems = $('.draggable, .droppable, .sortable, .resizable', element);
		if (dragitems.length > 0) {
			MyAMS.ajax.check($.fn.draggable,
				`${MyAMS.env.baseURL}../ext/jquery-ui${MyAMS.env.extext}.js`).then(() => {
				MyAMS.core.getCSS(`${MyAMS.env.baseURL}../../css/ext/jquery-ui.structure${MyAMS.env.extext}.css`, 'jquery-ui').then(() => {
					dragitems.each((idx, elt) => {
						const
							item = $(elt),
							data = item.data();
						// draggable components
						if (item.hasClass('draggable')) {
							const dragOptions = {
								axis: data.amsDraggableAxis || data.amsAxis,
								cursor: data.amsDraggableCursor || 'move',
								containment: data.amsDraggableContainment || data.amsContainment,
								delay: data.amsDraggableDelay || data.amsDelay,
								handle: data.amsDraggableHandle || data.amsHandle,
								connectToSortable: data.amsDraggableConnectSortable || data.amsConnectSortable,
								revert: data.amsDraggableRevert || data.amsRevert,
								revertDuration: data.amsDraggableRevertDuration || data.amsRevertDuration,
								helper: MyAMS.core.getFunctionByName(data.amsDraggableHelper) || data.amsDraggableHelper,
								start: MyAMS.core.getFunctionByName(data.amsDraggableStart) || function(evt, ui) {
									$(evt.currentTarget).data('is-dragging', true);
								},
								stop: MyAMS.core.getFunctionByName(data.amsDraggableStop) || function(evt, ui) {
									setTimeout(() => {
										$(evt.currentTarget).data('is-dragging', false);
									}, 100);
								}
							};
							let settings = $.extend({}, dragOptions,
								data.amsDraggableOptions || data.amsOptions);
							settings = MyAMS.core.executeFunctionByName(
								data.amsDraggableInitCallback || data.amsInit,
								document, item, settings) || settings;
							const veto = {veto: false};
							item.trigger('before-init.ams.draggable', [item, settings, veto]);
							if (veto.veto) {
								return;
							}
							const plugin = item.draggable(settings);
							item.disableSelection();
							MyAMS.core.executeFunctionByName(
								data.amsDraggableAfterInitCallback || data.amsAfterInit,
								document, item, plugin, settings);
							item.trigger('after-init.ams.draggable', [item, plugin]);
						}
						// droppable components
						if (item.hasClass('droppable')) {
							const dropOptions = {
								accept: data.amsDroppableAccept || data.amsAccept,
								classes: data.amsDroppableClasses,
								drop: MyAMS.core.getFunctionByName(data.amsDroppableDrop)
							};
							let settings = $.extend({}, dropOptions,
								data.amsDroppableOptions || data.amsOptions);
							settings = MyAMS.core.executeFunctionByName(
								data.amsDroppableInitCallback || data.amsInit,
								document, item, settings) || settings;
							const veto = {veto: false};
							item.trigger('before-init.ams.droppable', [item, settings, veto]);
							if (veto.veto) {
								return;
							}
							const plugin = item.droppable(settings);
							MyAMS.core.executeFunctionByName(
								data.amsDroppableAfterInitCallback || data.amsAfterInit,
								document, item, plugin, settings);
							item.trigger('after-init.ams.droppable', [item, plugin]);
						}
						// sortable components
						if (item.hasClass('sortable')) {
							const sortOptions = {
								items: data.amsSortableItems,
								handle: data.amsSortableHandle,
								helper: MyAMS.core.getFunctionByName(data.amsSortableHelper) || data.amsSortableHelper,
								connectWith: data.amsSortableConnectwith,
								containment: data.amsSortableContainment,
								placeholder: data.amsSortablePlaceholder,
								start: MyAMS.core.getFunctionByName(data.amsSortableStart),
								over: MyAMS.core.getFunctionByName(data.amsSortableOver),
								stop: MyAMS.core.getFunctionByName(data.amsSortableStop)
							};
							let settings = $.extend({}, sortOptions,
								data.amsSortableOptions || data.amsOptions);
							settings = MyAMS.core.executeFunctionByName(
								data.amsSortableInitCallback || data.amsInit,
								document, item, settings) || settings;
							const veto = {veto: false};
							item.trigger('before-init.ams.sortable', [item, settings, veto]);
							if (veto.veto) {
								return;
							}
							const plugin = item.sortable(settings);
							item.disableSelection();
							MyAMS.core.executeFunctionByName(
								data.amsSortableAfterInitCallback || data.amsAfterInit,
								document, item, plugin, settings);
							item.trigger('after-init.ams.sortable', [item, plugin]);
						}
						// resizable components
						if (item.hasClass('resizable')) {
							const resizeOptions = {
								autoHide: data.amsResizableAutohide === false ? true : data.amsResizableAutohide,
								containment: data.amsResizableContainment,
								grid: data.amsResizableGrid,
								handles: data.amsResizableHandles,
								start: MyAMS.core.getFunctionByName(data.amsResizableStart),
								resize: MyAMS.core.getFunctionByName(data.amsResizableResize),
								stop: MyAMS.core.getFunctionByName(data.amsResizableStop)
							};
							let settings = $.extend({}, resizeOptions,
								data.amsResizableOptions || data.amsOptions);
							settings = MyAMS.core.executeFunctionByName(
								data.amsResizableInitCallback || data.amsInit,
								document, item, settings) || settings;
							const veto = {veto: false};
							item.trigger('before-init.ams.resizable', [item, settings, veto]);
							if (veto.veto) {
								return;
							}
							const plugin = item.resizable(settings);
							item.disableSelection();
							MyAMS.core.executeFunctionByName(
								data.amsResizableAfterInitCallback || data.amsAfterInit,
								document, item, plugin, settings);
							item.trigger('after-init.ams.resizable', [item, plugin]);
						}
					});
					resolve(dragitems);
				});
			}, reject);
		} else {
			resolve(null);
		}
	});
}


/**
 * Dropzone drag&drop file input
 */

export function dropzone(element) {
	return new Promise((resolve, reject) => {
		const inputs = $('.dropzone', element);
		if (inputs.length > 0) {
			MyAMS.require('ajax').then(() => {
				MyAMS.ajax.check($.fn.dropzone,
					`${MyAMS.env.baseURL}../ext/dropzone.min.js`).then((firstLoad) => {
					const required = [];
					if (firstLoad) {
						required.push(MyAMS.core.getCSS(
							`${MyAMS.env.baseURL}../../css/ext/dropzone${MyAMS.env.extext}.css`,
							'dropzone'));
					}
					$.when.apply($, required).then(() => {
						inputs.each((idx, elt) => {
							const
								input = $(elt),
								data = input.data(),
								defaultOptions = {
									paramName: data.amsDropzoneParamName || data.amsParamName || 'form.widgets.data',
									url: data.amsDropzoneUrl || data.amsUrl || 'upload-file.json',
									uploadMultiple: data.amsDropzoneUploadMultiple !== false && data.amsUploadMultiple !== false,
									parallelUploads: data.amsDropzoneParallelUploads || data.amsParallelUploads || 10,
									maxFilesize: data.amsDropzoneMaxFilesize || data.amsMaxFilesize,
									thumbnailWidth: data.amsDropzoneThumbnailWidth || data.amsThumbnailWidth || 128,
									thumbnailHeight: data.amsDropzoneThumbnailHeight || data.amsThumbnailHeight || 128,
									thumbnailMethod: data.amsDropzoneThumbnailMethod || data.amsThumbnailMethod || 'contain',
									clickable: data.amsDropzoneClickable != false && data.amsCLickable !== false,
									acceptedFiles: data.amsDropzoneAcceptedFiles || data.amsAcceptedFiles,
									success: MyAMS.core.getFunctionByName(data.amsDropzoneSuccess || data.amsSuccess) || function (file, result, evt) {
										MyAMS.ajax.handleJSON(result);
									}
								}
							let settings = $.extend({}, defaultOptions, data.amsDropzoneOptions || data.amsOptions);
							settings = MyAMS.core.executeFunctionByName(
								data.amsDropzoneInitCallback || data.amsInit,
								document, input, settings) || settings;
							const veto = {veto: false};
							input.trigger('before-init.ams.dropzone', [input, settings, veto]);
							if (veto.veto) {
								return;
							}
							const plugin = input.dropzone(settings);
							input.trigger('after-init.ams.dropzone', [input, plugin]);
						});
						resolve(inputs);
					});
				}, reject);
			}, reject);
		} else {
			resolve(null);
		}
	});
}


/**
 * ACE text editor
 */

export function editor(element) {
	return new Promise((resolve, reject) => {
		const editors = $('.editor textarea', element);
		if (editors.length > 0) {
			MyAMS.require('ajax').then(() => {
				MyAMS.ajax.check(window.ace,
					`${MyAMS.env.baseURL}../ext/ace/ace${MyAMS.env.extext}.js`).then((firstLoad) => {

					const
						ace = window.ace,
						deferred = [];
					if (firstLoad) {
						ace.config.set('basePath', `${MyAMS.env.baseURL}../ext/ace`);
						deferred.push(MyAMS.core.getScript(
							`${MyAMS.env.baseURL}../ext/ace/ext-modelist${MyAMS.env.extext}.js`));
					}
					$.when.apply($, deferred).then(() => {
						editors.each((idx, elt) => {
							const
								textarea = $(elt),
								widget = textarea.parents('.editor'),
								data = textarea.data(),
								modeList = ace.require('ace/ext/modelist'),
								mode = data.amsEditorMode || data.amsMode ||
									modeList.getModeForPath(data.amsEditorFilename || data.amsFilename || 'text.txt').mode;

							setTimeout(() => {
								// create editor DIV
								const textEditor = $('<div>', {
									position: 'absolute',
									width: textarea.width(),
									height: textarea.height(),
									'class': textarea.attr('class')
								}).insertBefore(textarea);
								textarea.css('display', 'none');
								// initialize editor
								const defaultOptions = {
									mode: mode,
									fontSize: '12px',
									tabSize: 4,
									useSoftTabs: false,
									showGutter: true,
									showLineNumbers: true,
									printMargin: 132,
									showInvisibles: true
								};
								let settings = $.extend({}, defaultOptions, data.amsEditorOptions || data.amsOptions);
								settings = MyAMS.core.executeFunctionByName(data.amsEditorInitCallback || data.amsInit,
									document, textarea, settings) || settings;
								const veto = {veto: false};
								textarea.trigger('before-init.ams.editor', [textarea, settings, veto]);
								if (veto.veto) {
									return;
								}
								const editor = ace.edit(textEditor[0]);
								editor.setOptions(settings);
								if (MyAMS.theme === 'darkmode') {
									editor.setTheme('ace/theme/dracula');
								} else {
									editor.setTheme('ace/theme/textmate');
								}
								editor.session.setValue(textarea.val());
								if (textarea.attr('disabled')) {
									editor.setReadOnly(true);
								}
								editor.session.on('change', () => {
									textarea.val(editor.session.getValue());
								});
								widget.data('editor', editor);
								MyAMS.core.executeFunctionByName(
									data.amsEditorAfterEditCallback || data.amsAfterInit,
									document, textarea, editor, settings);
								textarea.trigger('after-init.ams.editor', [textarea, editor]);
							}, 200);
						});
						resolve(editors);
					});
				});
			}, reject);
		} else {
			resolve(null);
		}
	});
}


/**
 * Bootstrap custom file input manager
 */

export function fileInput(element) {
	return new Promise((resolve, reject) => {
		const inputs = $('.custom-file-input', element);
		if (inputs.length > 0) {
			MyAMS.require('ajax').then(() => {
				MyAMS.ajax.check(window.bsCustomFileInput,
					`${MyAMS.env.baseURL}../ext/bs-custom-file-input${MyAMS.env.extext}.js`).then(() => {
					setTimeout(() => {  // use timeout to handle file inputs in modals!
						inputs.each((idx, elt) => {
							const
								input = $(elt),
								inputId = input.attr('id'),
								inputSelector = inputId ? `#${inputId}` : input.attr('name'),
								form = $(elt.form),
								formId = form.attr('id'),
								formSelector = formId ? `#${formId}` : form.attr('name'),
								veto = {veto: false};
							input.trigger('before-init.ams.fileinput', [input, veto]);
							if (veto.veto) {
								return;
							}
							bsCustomFileInput.init(inputSelector, formSelector);
							input.trigger('after-init.ams.fileinput', [input]);
						});
						resolve(inputs);
					}, 250);
				}, reject);
			}, reject);
		} else {
			resolve(null);
		}
	});
}


/**
 * Image area select plug-in integration
 */

export function imgAreaSelect(element) {
	return new Promise((resolve, reject) => {
		const images = $('.imgareaselect', element);
		if (images.length > 0) {
			MyAMS.require('ajax').then(() => {
				MyAMS.ajax.check($.fn.imgAreaSelect,
					`${MyAMS.env.baseURL}../ext/jquery-imgareaselect${MyAMS.env.extext}.js`).then((firstLoad) => {
					const required = [];
					if (firstLoad) {
						required.push(MyAMS.core.getCSS(
							`${MyAMS.env.baseURL}../../css/ext/imgareaselect-animated${MyAMS.env.extext}.css`,
							'imgareaselect'));
					}
					$.when.apply($, required).then(() => {
						images.each((idx, elt) => {
							const image = $(elt);
							if (image.data('imgAreaSelect')) {
								return;  // already initialized
							}
							const
								data = image.data(),
								parentSelector = data.amsImgareaselectParent || data.amsParent,
								parent = parentSelector ? image.parents(parentSelector) : 'body',
								defaultOptions = {
									instance: true,
									handles: true,
									parent: parent,
									x1: data.amsImgareaselectX1 || data.amsX1 || 0,
									y1: data.amsImgareaselectY1 || data.amsY1 || 0,
									x2: data.amsImgareaselectX2 || data.amsX2 ||
										data.amsImgareaselectImageWidth || data.amsImageWidth,
									y2: data.amsImgareaselectY2 || data.amsY2 ||
										data.amsImgareaselectImageHeight || data.amsImageHeight,
									imageWidth: data.amsImgareaselectImageWidth || data.amsImageWidth,
									imageHeight: data.amsImgareaselectImageHeight || data.amsImageHeight,
									imgWidth: data.amsImgareaselectThumbWidth || data.amsThumbWidth,
									imgHeight: data.amsImgareaselectThumbHeight || data.amsThumbHeight,
									minWidth: 128,
									minHeight: 128,
									aspectRatio: data.amsImgareaselectAspectRatio || data.amsAspectRatio,
									onSelectEnd: MyAMS.core.getFunctionByName(data.amsImgareaselectSelectEnd || data.amsSelectedEnd) || function(img, selection) {
										const target = data.amsImgareaselectTargetField || data.amsTargetField || 'image_';
										$(`input[name="${target}x1"]`, parent).val(selection.x1);
										$(`input[name="${target}y1"]`, parent).val(selection.y1);
										$(`input[name="${target}x2"]`, parent).val(selection.x2);
										$(`input[name="${target}y2"]`, parent).val(selection.y2);
									}
								};
							let settings = $.extend({}, defaultOptions, data.amsImgareaselectOptions || data.amsOptions);
							settings = MyAMS.core.executeFunctionByName(
								data.amsImgareaselectInitCallback || data.amsInit,
								document, image, settings) || settings;
							const veto = {veto: false};
							image.trigger('before-init.ams.imgareaselect', [image, settings, veto]);
							if (veto.veto) {
								return;
							}
							// add timeout to update plug-in if displayed into a modal dialog
							setTimeout(() => {
								const plugin = image.imgAreaSelect(settings);
								image.trigger('after-init.ams.imgareaselect', [image, plugin]);
							}, 200);
						});
						resolve(images);
					}, reject);
				}, reject);
			}, reject);
		} else {
			resolve(null);
		}
	});
}


/**
 * Inputmask plug-in integration
 */
export function inputMask(element) {
	return new Promise((resolve, reject) => {
		const inputs = $('input[data-input-mask]', element);
		if (inputs.length > 0) {
			MyAMS.require('ajax').then(() => {
				MyAMS.ajax.check($.fn.inputmask,
					`${MyAMS.env.baseURL}../ext/jquery-inputmask${MyAMS.env.extext}.js`).then(() => {
					inputs.each((idx, elt) => {
						const
							input = $(elt),
							data = input.data();
						let options;
						if (typeof(data.inputMask) === 'object') {
							options = data.inputMask;
						} else {
							options = {
								mask: data.inputMask.toString()
							};
						}
						let settings = $.extend({}, options, data.amsInputMaskOptions || data.amsOptions);
						settings = MyAMS.core.executeFunctionByName(data.amsInputmaskInitCallback || data.amsInit,
							document, input, settings) || settings;
						const veto = {veto: false};
						input.trigger('before-init.ams.inputmask', [input, settings, veto]);
						if (veto.veto) {
							return;
						}
						const plugin = input.inputmask(settings);
						MyAMS.core.executeFunctionByName(data.amsInputmaskAfterInitCallback || data.amsAfterInit,
							document, input, plugin, settings);
						input.trigger('after-init.ams.inputmask', [input, plugin]);
					});
					resolve(inputs);
				}, reject);
			}, reject);
		} else {
			resolve(null);
		}
	});
}


/**
 * Select2 plug-in integration
 */

const _select2Helpers = {

	select2UpdateHiddenField: (input) => {
		const values = [];
		input.parent().find('ul.select2-selection__rendered').children('li[title]').each((idx, elt) => {
			values.push(input.children(`option[data-content="${elt.title}"]`).attr('value'));
		});
		input.data('select2-target').val(values.join(input.data('ams-select2-separator') || ','));
	},

	select2AjaxParamsHelper: (params, data) => {
		return Object.assign({}, params, data);
	}
};

export function select2(element) {
	return new Promise((resolve, reject) => {
		const selects = $('.select2', element);
		if (selects.length > 0) {
			MyAMS.require('ajax', 'helpers').then(() => {
				MyAMS.ajax.check($.fn.select2,
					`${MyAMS.env.baseURL}../ext/select2/select2${MyAMS.env.extext}.js`).then((firstLoad) => {
					const required = [];
					if (firstLoad) {
						required.push(MyAMS.core.getScript(`${MyAMS.env.baseURL}../ext/select2/i18n/${MyAMS.i18n.language}.js`));
					}
					$.when.apply($, required).then(() => {
						selects.each((idx, elt) => {
							const
								select = $(elt),
								data = select.data();
							if (data.select2) {
								return;  // already initialized
							}
							const defaultOptions = {
								theme: data.amsSelect2Theme || data.amsTheme || 'bootstrap4',
								language: data.amsSelect2Language || data.amsLanguage || MyAMS.i18n.language,
								escapeMarkup: MyAMS.core.getFunctionByName(
									data.amsSelect2EscapeMarkup || data.amsEscapeMarkup),
								matcher: MyAMS.core.getFunctionByName(
									data.amsSelect2Matcher || data.amsMatcher),
								sorter: MyAMS.core.getFunctionByName(
									data.amsSelect2Sorter || data.amsSorter),
								templateResult: MyAMS.core.getFunctionByName(
									data.amsSelect2TemplateResult || data.amsTemplateResult),
								templateSelection: MyAMS.core.getFunctionByName(
									data.amsSelect2TemplateSelection || data.amsTemplateSelection),
								tokenizer: MyAMS.core.getFunctionByName(
									data.amsSelect2Tokenizer || data.amsTokenizer)
							};
							const ajaxUrl = data.amsSelect2AjaxUrl || data.amsAjaxUrl || data['ajax-Url'];
							if (ajaxUrl) {
								// check AJAX data helper function
								let ajaxParamsHelper;
								const ajaxParams = MyAMS.core.getFunctionByName(
									data.amsSelect2AjaxParams || data.amsAjaxParams || data['ajax-Params']) ||
									data.amsSelect2AjaxParams || data.amsAjaxParams || data['ajax-Params'];
								if (typeof ajaxParams === 'function') {
									ajaxParamsHelper = ajaxParams;
								} else if (ajaxParams) {
									ajaxParamsHelper = (params) => {
										return _select2Helpers.select2AjaxParamsHelper(params, ajaxParams);
									}
								}
								defaultOptions.ajax = {
									url: MyAMS.core.getFunctionByName(
										data.amsSelect2AjaxUrl || data.amsAjaxUrl) ||
										data.amsSelect2AjaxUrl || data.amsAjaxUrl,
									data: ajaxParamsHelper || MyAMS.core.getFunctionByName(
										data.amsSelect2AjaxData || data.amsAjaxData) ||
										data.amsSelect2AjaxData || data.amsAjaxData,
									processResults: MyAMS.core.getFunctionByName(
										data.amsSelect2AjaxProcessResults || data.amsAjaxProcessResults) ||
										data.amsSelect2AjaxProcessResults || data.amsAjaxProcessResults,
									transport: MyAMS.core.getFunctionByName(
										data.amsSelect2AjaxTransport || data.amsAjaxTransport) ||
										data.amsSelect2AjaxTransport || data.amsAjaxTransport
								};
								defaultOptions.minimumInputLength = data.amsSelect2MinimumInputLength ||
									data.amsMinimumInputLength || data.minimumInputLength;
								if (defaultOptions.minimumInputLength === undefined) {
									defaultOptions.minimumInputLength = 1;
								}
							}
							if (select.hasClass('sortable')) {
								// create hidden input for sortable selections
								const hidden = $(`<input type="hidden" name="${select.attr('name')}">`).insertAfter(select);
								hidden.val($('option:selected', select).listattr('value').join(data.amsSelect2Separator || ','));
								select.data('select2-target', hidden)
									.removeAttr('name');
								defaultOptions.templateSelection = (data) => {
									const elt = $(data.element);
									elt.attr('data-content', elt.html());
									return data.text;
								};
							}
							let settings = $.extend({}, defaultOptions, data.amsSelect2Options || data.amsOptions);
							settings = MyAMS.core.executeFunctionByName(
								data.amsSelect2InitCallback || data.amsInit,
								document, select, settings) || settings;
							const veto = {veto: false};
							select.trigger('before-init.ams.select2', [select, settings, veto]);
							if (veto.veto) {
								return;
							}
							const plugin = select.select2(settings);
							select.on('select2:opening select2:selecting select2:unselecting select2:clearing', (evt) => {
								// handle disabled selects
								if ($(evt.target).is(':disabled')) {
									return false;
								}
							});
							select.on('select2:opening', (evt) => {
								// handle z-index in modals
								const modal = $(evt.currentTarget).parents('.modal').first();
								if (modal.exists()) {
									const zIndex = parseInt(modal.css('z-index'));
									plugin.data('select2').$dropdown.css('z-index', zIndex + 1);
								}
							});
							select.on('select2:open', () => {
								// handle dropdown automatic focus
								setTimeout(() => {
									const dropdown = $('.select2-search__field', plugin.data('select2').$dropdown);
									if (dropdown.exists()) {
										dropdown.get(0).focus();
									}
								}, 50);
							});
							if (select.hasClass('sortable')) {
								MyAMS.ajax.check($.fn.sortable,
									`${MyAMS.env.baseURL}../ext/jquery-ui${MyAMS.env.extext}.js`).then(() => {
									select.parent().find('ul.select2-selection__rendered').sortable({
										containment: 'parent',
										update: () => {
											_select2Helpers.select2UpdateHiddenField(select);
										}
									});
									select.on('select2:select select2:unselect', (evt) => {
										const
											id = evt.params.data.id,
											target = $(evt.currentTarget),
											option = target.children(`option[value="${id}"]`);
										MyAMS.helpers.moveElementToParentEnd(option);
										target.trigger('change');
										_select2Helpers.select2UpdateHiddenField(target);
									});
								});
							}
							MyAMS.core.executeFunctionByName(
								data.amsSelect2AfterInitCallback || data.amsAfterInit,
								document, select, plugin, settings);
							select.trigger('after-init.ams.select2', [select, plugin]);
						});
						resolve(selects);
					}, reject);
				}, reject);
			}, reject);
		} else {
			resolve(null);
		}
	});
}


/**
 * SVG image plug-in
 */

export function svgPlugin(element) {
	return new Promise((resolve) => {
		const svgs = $('.svg-container', element);
		if (svgs.length > 0) {
			svgs.each((idx, elt) => {
				const
					container = $(elt),
					svg = $('svg', container),
					width = svg.attr('width'),
					height = svg.attr('height');
				if (width && height) {
					elt.setAttribute('viewBox',
						`0 0 ${Math.round(parseFloat(width))} ${Math.round(parseFloat(height))}`);
				}
				svg.attr('width', '100%').attr('height', 'auto');
			});
			resolve(svgs);
		} else {
			resolve(null);
		}
	});
}


/**
 * Fieldset switcher plug-in
 *
 * A switcher is a simple fieldset with a "switch" icon in it's legend, which can
 * be used to hide or show fieldset content.
 */

export function switcher(element) {
	return new Promise((resolve) => {
		const switchers = $('legend.switcher', element);
		if (switchers.length > 0) {
			switchers.each((idx, elt) => {
				const
					legend = $(elt),
					fieldset = legend.parent('fieldset'),
					data = legend.data(),
					state = data.amsSwitcherState || data.amsState,
					minusClass = data.amsSwitcherMinusClass || data.amsMinusClass || 'chevron-down',
					plusClass = data.amsSwitcherPlusClass || data.amsPlusClass || 'chevron-right';
				if (!data.amsSwitcher) {
					const veto = {veto: false};
					legend.trigger('before-init.ams.switcher', [legend, data, veto]);
					if (veto.veto) {
						return;
					}
					$(`<i class="fa fa-fw fa-${state === 'open' ? minusClass : plusClass} mr-2"></i>`)
						.prependTo(legend);
					legend.on('click', (evt) => {
						evt.preventDefault();
						const veto = {};
						legend.trigger('before-switch.ams.switcher', [legend, veto]);
						if (veto.veto) {
							return;
						}
						if (fieldset.hasClass('switched')) {
							fieldset.removeClass('switched');
							MyAMS.core.switchIcon($('i', legend), plusClass, minusClass);
							legend.trigger('opened.ams.switcher', [legend]);
							const id = legend.attr('id');
							if (id) {
								$(`legend.switcher[data-ams-switcher-sync="${id}"]`, fieldset).each((idx, elt) => {
									const switcher = $(elt);
									if (switcher.parents('fieldset').hasClass('switched')) {
										switcher.click();
									}
								});
							}
						} else {
							fieldset.addClass('switched');
							MyAMS.core.switchIcon($('i', legend), minusClass, plusClass);
							legend.trigger('closed.ams.switcher', [legend]);
						}
					});
					if (state !== 'open') {
						fieldset.addClass('switched');
					}
					legend.trigger('after-init.ams.switcher', [legend]);
					legend.data('ams-switcher', true);
				}
			});
			resolve(switchers);
		} else {
			resolve(null);
		}
	});
}


/**
 * TinyMCE HTML editor plug-in
 */

export function tinymce(element) {
	return new Promise((resolve, reject) => {
		const editors = $('.tinymce', element);
		if (editors.length > 0) {
			MyAMS.require('ajax', 'i18n').then(() => {
				const baseURL = `${MyAMS.env.baseURL}../ext/tinymce${MyAMS.env.devmode ? '/dev': ''}`;
				MyAMS.ajax.check(window.tinymce,
					`${baseURL}/tinymce${MyAMS.env.extext}.js`).then((firstLoad) => {
					const deferred = [];
					if (firstLoad) {
						tinymce.baseURL = baseURL;
						tinymce.suffix = MyAMS.env.extext;
						deferred.push(MyAMS.core.getScript(`${baseURL}/jquery.tinymce.min.js`));
						deferred.push(MyAMS.core.getScript(`${baseURL}/themes/silver/theme${MyAMS.env.extext}.js`));
						// Prevent Bootstrap dialog from blocking focusin
						$(document).on('focusin', (evt) => {
							if ($(evt.target).closest(".tox-tinymce, .tox-tinymce-aux, " +
								".moxman-window, .tam-assetmanager-root").length) {
								evt.stopImmediatePropagation();
							}
						});
						// Remove editor before cleaning content
						$(document).on('clear.ams.content', (evt, veto, element) => {
							$('.tinymce', element).each((idx, elt) => {
								const
									editorId = $(elt).attr('id'),
									editor = window.tinymce.get(editorId);
								if (editor !== null) {
									editor.remove();
								}
							});
						});
					}
					$.when.apply($, deferred).then(() => {
						editors.each((idx, elt) => {
							const
								editor = $(elt),
								data = editor.data(),
								defaultOptions = {
									selector: `textarea#${editor.attr('id')}`,
									base_url: baseURL,
									theme: data.amsTinymceTheme || data.amsTheme || 'silver',
									language: MyAMS.i18n.language,
									menubar: (data.amsTinymceMenubar !== false) && (data.amsMenubar !== false),
									statusbar: (data.amsTinymceStatusbar !== false) && (data.amsStatusbar !== false),
									plugins: data.amsTinymcePlugins || data.amsPlugins || [
										"advlist autosave autolink lists link charmap print preview hr anchor pagebreak",
										"searchreplace wordcount visualblocks visualchars code fullscreen",
										"insertdatetime nonbreaking save table contextmenu directionality",
										"emoticons paste textcolor colorpicker textpattern autoresize"
									],
									toolbar: data.amsTinymceToolbar || data.amsToolbar,
									toolbar1: ((data.amsTinymceToolbar1 === false) || (data.amsToolbar1 === false)) ? false :
										data.amsTinymceToolbar1 || data.amsToolbar1 ||
										"undo redo | pastetext | styleselect | bold italic | " +
										"alignleft aligncenter alignright alignjustify | " +
										"bullist numlist outdent indent",
									toolbar2: ((data.amsTinymceToolbar2 === false) || (data.amsToolbar2 === false)) ? false :
										data.amsTinymceToolbar2 || data.amsToolbar2 ||
										"forecolor backcolor emoticons | charmap link image media | " +
										"fullscreen preview print | code",
									content_css: data.amsTinymceContentCss || data.amsContentCss,
									formats: data.amsTinymceFormats || data.amsFormats,
									style_formats: data.amsTinymceStyleFormats || data.amsStyleFormats,
									block_formats: data.amsTinymceBlockFormats || data.amsBlockFormats,
									valid_classes: data.amsTinymceValidClasses || data.amsValidClasses,
									relative_urls: false,
									remove_script_host: false,
									convert_urls: false,
									image_advtab: true,
									image_list: MyAMS.core.getFunctionByName(data.amsTinymceImageList || data.amsImageList) ||
										data.amsTinymceImageList || data.amsImageList,
									image_class_list: data.amsTinymceImageClassList || data.amsImageClassList,
									link_list: MyAMS.core.getFunctionByName(data.amsTinymceLinkList || data.amsLinkList) ||
										data.amsTinymceLinkList || data.amsLinkList,
									link_class_list: data.amsTinymceLinkClassList || data.amsLinkClassList,
									paste_as_text: ((data.amsTinymcePasteAsText === undefined) && (data.amsPasteAsText === undefined)) ?
										true : data.amsTinymcePasteAsText || data.amsPasteAsText,
									paste_auto_cleanup_on_paste: ((data.amsTinymcePasteAutoCleanup === undefined) && (data.amsPasteAutoCleanup === undefined)) ?
										true : data.amsTinymcePasteAutoCleanup || data.amsPasteAutoCleanup,
									paste_strip_class_attributes: data.amsTinymcePasteStripClassAttributes || data.amsPasteStripClassAttributes || 'all',
									paste_remove_spans: ((data.amsTinymcePasteRemoveSpans === undefined) && (data.amsPasteRemoveSpans === undefined)) ?
										true : data.amsTinymcePasteRemoveSpans || data.amsPasteRemoveSpans,
									paste_remove_styles: ((data.amsTinymcePasteRemoveStyles === undefined) || (data.amsPasteRemoveStyles === undefined)) ?
										true : data.amsTinymcePasteRemoveStyles || data.amsPasteRemoveStyles,
									height: data.amsTinymceHeight || data.amsHeight || 50,
									min_height: 50,
									resize: true,
									autoresize_min_height: 50,
									autoresize_max_height: 500
								};
							const plugins = data.amsTinymceExternalPlugins || data.amsExternalPlugins;
							if (plugins) {
								const names = plugins.split(/\s+/);
								for (const name of names) {
									const src = editor.data(`ams-tinymce-plugin-${name}`) || editor.data(`ams-plugin-${name}`);
									window.tinymce.PluginManager.load(name, MyAMS.core.getSource(src));
								}
							}
							let settings = $.extend({}, defaultOptions, data.amsTinymceOptions || data.amsOptions);
							settings = MyAMS.core.executeFunctionByName(
								data.amsTinymceInitCallback || data.amsInit,
								document, editor, settings) || settings;
							const veto = {veto: false};
							editor.trigger('before-init.ams.tinymce', [editor, settings, veto]);
							if (veto.veto) {
								return;
							}
							setTimeout(() => {
								const plugin = editor.tinymce(settings);
								MyAMS.core.executeFunctionByName(
									data.amsTinymceAfterInitCallback || data.amsAfterInit,
									document, editor, plugin, settings);
								editor.trigger('after-init.ams.tinymce', [editor, settings]);
							}, 250);
						});
						resolve(editors);
					}, reject);
				}, reject);
			}, reject);
		} else {
			resolve(null);
		}
	});
}


/**
 * Bootstrap treeview plug-in
 */

export function treeview(element) {
	return new Promise((resolve, reject) => {
		const trees = $('.treeview', element);
		if (trees.length > 0) {
			MyAMS.require('ajax').then(() => {
				MyAMS.ajax.check($.fn.treview,
					`${MyAMS.env.baseURL}../ext/bootstrap-treeview${MyAMS.env.extext}.js`).then((firstLoad) => {
					const required = [];
					if (firstLoad) {
						required.push(MyAMS.core.getCSS(`${MyAMS.env.baseURL}../../css/ext/bootstrap-treeview${MyAMS.env.extext}.css`,
							'treeview'));
					}
					$.when.apply($, required).then(() => {
						trees.each((idx, elt) => {
							const
								treeview = $(elt),
								data = treeview.data(),
								dataOptions = {
									data: data.amsTreeviewData,
									levels: data.amsTreeviewLevels,
									injectStyle: data.amsTreeviewInjectStyle,
									expandIcon: data.amsTreeviewExpandIcon || 'far fa-fw fa-plus-square',
									collapseIcon: data.amsTreeviewCollaspeIcon || 'far fa-fw fa-minus-square',
									emptyIcon: data.amsTreeviewEmptyIcon,
									nodeIcon: data.amsTreeviewNodeIcon,
									selectedIcon: data.amsTreeviewSelectedIcon,
									checkedIcon: data.amsTreeviewCheckedIcon || 'far fa-fw fa-check-square',
									uncheckedIcon: data.amsTreeviewUncheckedIcon || 'far fa-fw fa-square',
									color: data.amsTreeviewColor,
									backColor: data.amsTreeviewBackColor,
									borderColor: data.amsTreeviewBorderColor,
									onHoverColor: data.amsTreeviewHoverColor,
									selectedColor: data.amsTreeviewSelectedColor,
									selectedBackColor: data.amsTreeviewSelectedBackColor,
									unselectableColor: data.amsTreeviewUnselectableColor || 'rgba(1,1,1,0.25)',
									unselectableBackColor: data.amsTreeviewUnselectableBackColor || 'rgba(1,1,1,0.25)',
									enableLinks: data.amsTreeviewEnableLinks,
									highlightSelected: data.amsTreeviewHighlightSelected,
									highlightSearchResults: data.amsTreeviewhighlightSearchResults,
									showBorder: data.amsTreeviewShowBorder,
									showIcon: data.amsTreeviewShowIcon,
									showCheckbox: data.amsTreeviewShowCheckbox,
									showTags: data.amsTreeviewShowTags,
									toggleUnselectable: data.amsTreeviewToggleUnselectable,
									multiSelect: data.amsTreeviewMultiSelect,
									onNodeChecked: MyAMS.core.getFunctionByName(data.amsTreeviewNodeChecked),
									onNodeCollapsed: MyAMS.core.getFunctionByName(data.amsTreeviewNodeCollapsed),
									onNodeDisabled: MyAMS.core.getFunctionByName(data.amsTreeviewNodeDisabled),
									onNodeEnabled: MyAMS.core.getFunctionByName(data.amsTreeviewNodeEnabled),
									onNodeExpanded: MyAMS.core.getFunctionByName(data.amsTreeviewNodeExpanded),
									onNodeSelected: MyAMS.core.getFunctionByName(data.amsTreeviewNodeSelected),
									onNodeUnchecked: MyAMS.core.getFunctionByName(data.amsTreeviewNodeUnchecked),
									onNodeUnselected: MyAMS.core.getFunctionByName(data.amsTreeviewNodeUnselected),
									onSearchComplete: MyAMS.core.getFunctionByName(data.amsTreeviewSearchComplete),
									onSearchCleared: MyAMS.core.getFunctionByName(data.amsTreeviewSearchCleared)
								};
							let settings = $.extend({}, dataOptions, data.amsTreeviewOptions);
							settings = MyAMS.core.executeFunctionByName(data.amsTreeviewInitCallback || data.amsInit,
								document, treeview, settings) || settings;
							const veto = {veto: false};
							treeview.trigger('before-init.ams.treeview', [treeview, settings, veto]);
							if (veto.veto) {
								return;
							}
							const plugin = treeview.treeview(settings);
							MyAMS.core.executeFunctionByName(data.amsTreeviewAfterInitCallback || data.amsAfterInit,
								document, treeview, plugin, settings);
							treeview.trigger('after-init.ams.treeview', [treeview, plugin]);
						});
						resolve(trees);
					}, reject);
				}, reject);
			}, reject);
		} else {
			resolve(null);
		}
	});
}


/**
 * Form validation plug-in
 */

export function validate(element) {
	return new Promise((resolve, reject) => {
		const forms = $('form:not([novalidate])', element);
		if (forms.length > 0) {
			MyAMS.require('ajax', 'i18n').then(() => {
				MyAMS.ajax.check($.fn.validate,
					`${MyAMS.env.baseURL}../ext/validate/jquery-validate${MyAMS.env.extext}.js`).then((firstLoad) => {
					if (firstLoad && (MyAMS.i18n.language !== 'en')) {
						MyAMS.core.getScript(`${MyAMS.env.baseURL}../ext/validate/i18n/messages_${MyAMS.i18n.language}${MyAMS.env.extext}.js`).then(() => {
						});
					}
					forms.each((idx, elt) => {
						const
							form = $(elt),
							data = form.data(),
							dataOptions = {
								ignore: null,
								invalidHandler: MyAMS.core.getFunctionByName(data.amsValidateInvalidHandler) || (
									(evt, validator) => {
										// automatically display hidden fields with errors!
										$('span.is-invalid', form).remove();
										$('.is-invalid', form).removeClass('is-invalid');
										for (const error of validator.errorList) {
											const
												element = $(error.element),
												panels = element.parents('.tab-pane'),
												fieldsets = element.parents('fieldset.switched');
											fieldsets.each((idx, elt) => {
												$('legend.switcher', elt).click();
											})
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
									}
								),
								errorElement: data.amsValidateErrorElement || 'span',
								errorClass: data.amsValidateErrorClass || 'is-invalid',
								errorPlacement: MyAMS.core.getFunctionByName(data.amsValidateErrorPlacement) ||
									((error, element) => {
										error.addClass('invalid-feedback');
										element.closest('.form-widget').append(error);
									}),
								submitHandler: MyAMS.core.getFunctionByName(data.amsValidateSubmitHandler) ||
									(form.attr('data-async') !== undefined ?
										() => {
											MyAMS.require('form').then(() => {
												MyAMS.form.submit(form);
											});
										}
										: () => {
											form.get(0).submit();
										})
							};
						$('[data-ams-validate-rules]', form).each((idx, elt) => {
							if (idx === 0) {
								dataOptions.rules = {};
							}
							dataOptions.rules[$(elt).attr('name')] = $(elt).data('ams-validate-rules');
						});
						$('[data-ams-validate-messages]', form).each((idx, elt) => {
							if (idx === 0) {
								dataOptions.messages = {};
							}
							dataOptions.messages[$(elt).attr('name')] = $(elt).data('ams-validate-messages');
						});
						let settings = $.extend({}, dataOptions, data.amsValidateOptions || data.amsOptions);
						settings = MyAMS.core.executeFunctionByName(data.amsValidateInitCallback ||
							data.amsInit, document, form, settings) || settings;
						const veto = {veto: false};
						form.trigger('before-init.ams.validate', [form, settings, veto]);
						if (veto.veto) {
							return;
						}
						const plugin = form.validate(settings);
						MyAMS.core.executeFunctionByName(data.amsValidateAfterInitCallback ||
							data.amsAfterInit, document, form, plugin, settings);
						form.trigger('after-init.ams.validate', [form, plugin]);
					});
					resolve(forms);
				}, reject);
			}, reject);
		}
	});
}


/**
 * Global module initialization
 */

if (window.MyAMS) {

	// register loaded plug-ins
	MyAMS.registry.register(calendar, 'calendar');
	MyAMS.registry.register(checker, 'checker');
	MyAMS.registry.register(colorPicker, 'colorPicker');
	MyAMS.registry.register(contextMenu, 'contextMenu');
	MyAMS.registry.register(datatables, 'datatables');
	MyAMS.registry.register(datetime, 'datetime');
	MyAMS.registry.register(dragdrop, 'dragdrop');
	MyAMS.registry.register(dropzone, 'dropzone');
	MyAMS.registry.register(editor, 'editor');
	MyAMS.registry.register(fileInput, 'fileInput');
	MyAMS.registry.register(imgAreaSelect, 'imgAreaSelect');
	MyAMS.registry.register(inputMask, 'inputMask');
	MyAMS.registry.register(select2, 'select2');
	MyAMS.registry.register(svgPlugin, 'svg');
	MyAMS.registry.register(switcher, 'switcher');
	MyAMS.registry.register(tinymce, 'tinymce');
	MyAMS.registry.register(treeview, 'treeview');
	MyAMS.registry.register(validate, 'validate');

	// register module
	MyAMS.config.modules.push('plugins');
	if (!MyAMS.env.bundle) {
		console.debug("MyAMS: plugins module loaded...");
	}
}
