/* global MyAMS */
/**
 * MyAMS modal dialogs support
 */

const $ = MyAMS.$;


let _initialized = false;


/*
 * Standard data-toggle="modal" handler
 */
export function modalToggleEventHandler(evt) {
	return new Promise((resolve, reject) => {
		const
			source = $(evt.currentTarget),
			handlers = source.data('ams-disabled-handlers');
		if (source.attr('disabled') ||
			source.hasClass('disabled') ||
			(handlers === true) ||
			(handlers === 'click') ||
			(handlers === 'all')) {
			resolve(false);
			return;
		}
		if (source.data('ams-context-menu') === true) {
			resolve(false);
			return;
		}
		if (source.data('ams-stop-propagation') === true) {
			evt.stopPropagation();
		}
		evt.preventDefault();
		source.tooltip('hide');
		MyAMS.modal.open(source).then(() => {
			resolve(true);
		}, reject);
	});
}

/**
 * Standard modal shown event handler
 * This handler is used to allow modals stacking
 */
export function modalShownEventHandler(evt) {

	const zIndexModal = 1100;

	// Enable modals stacking
	const
		dialog = $(evt.target),
		visibleModalsCount = $('.modal:visible').length,
		zIndex = zIndexModal + (100 * visibleModalsCount);
	dialog.css('z-index', zIndex);
	setTimeout(() => {
		$('.modal-backdrop').not('.modal-stack')
			.first()
			.css('z-index', zIndex - 10)
			.addClass('modal-stack')
			.insertBefore(dialog);
	}, 0);
	// Check form contents before closing modals
	$(dialog).off('click', '[data-dismiss="modal"]')
		.on('click', '[data-dismiss="modal"]', (evt) => {
			const handler = $(evt.currentTarget).data('ams-dismiss-handler') || modalDismissEventHandler;
			return MyAMS.core.executeFunctionByName(handler, document, evt);
		});
}


/**
 * Dynamic modal 'show' callback
 * This callback is used to initialize modal's viewport size
 *
 * @param evt: source event
 */
export function dynamicModalShowEventHandler(evt) {
	const dialog = $(evt.target);
	return MyAMS.core.executeFunctionByName(dialog.data('ams-init-content') ||
		MyAMS.config.initContent, document, dialog);
}


/**
 * Dynamic modal 'shown' callback
 * This callback is used to set focus on first modal input
 *
 * @param evt: source event
 */
export function dynamicModalShownEventHandler(evt) {
	return new Promise((resolve, reject) => {
		MyAMS.require('form').then(() => {
			const modal = $(evt.target);
			MyAMS.form.setFocus(modal);
			resolve(modal);
		}, reject);
	});
}


/**
 * Modal dismiss handler
 */
export function modalDismissEventHandler(evt) {
	return new Promise((resolve, reject) => {
		const
			source = $(evt.currentTarget),
			dialog = source.parents('.modal').first();
		dialog.data('modal-result', $(evt.currentTarget).data('modal-dismiss-value'));
		if (MyAMS.form) {
			MyAMS.form.confirmChangedForm(dialog).then((status) => {
				if (status === 'success') {
					dialog.modal('hide');
				}
			}).then(resolve, reject);
		} else {
			dialog.modal('hide');
			resolve();
		}
	});
}


/**
 * Standard modal hidden event handler
 *
 * If several visible modals are still, a "modal-open" class is added to body to ensure
 * modals are still visible.
 */
export function modalHiddenEventHandler() {
	if ($('.modal:visible').length > 0) {
		$.fn.modal.Constructor.prototype._checkScrollbar();
		$.fn.modal.Constructor.prototype._setScrollbar();
		$('body').addClass('modal-open');
	}
}


/**
 * Dynamic modal 'hidden' callback
 * This callback is used to clear and remove dynamic modals
 *
 * @param evt: source event
 */
export function dynamicModalHiddenEventHandler(evt) {
	const dialog = $(evt.target);
	MyAMS.core.executeFunctionByName(dialog.data('ams-clear-content') ||
		MyAMS.config.clearContent, document, dialog).then(() => {
		if (dialog.data('dynamic') === true) {
			dialog.remove();
			if (MyAMS.form) {
				MyAMS.form.setFocus($('.modal-dialog').last());
			}
		}
	});
}


/**
 * Main modal module definition
 */
export const modal = {

	init: () => {

		if (_initialized) {
			return;
		}
		_initialized = true;

		if (MyAMS.config.ajaxNav) {
			// Initialize modal dialogs links
			// Standard Bootstrap handlers are removed!!
			$(document).off('click', '[data-toggle="modal"]')
				.on('click', '[data-toggle="modal"]', (evt) => {
					// disable click on dragging element
					if ($(evt.currentTarget).data('is-dragging')) {
						return;
					}
					// disable click on datatable expand control
					const target = $(evt.target);
					if (target.hasClass('dtr-control')) {
						const table = target.parents('.datatable');
						if (table.hasClass('collapsed')) {
							return;
						}
					}
					evt.stopPropagation();
					const handler = $(evt.currentTarget).data('ams-modal-handler') || modalToggleEventHandler;
					MyAMS.core.executeFunctionByName(handler, document, evt);
				});
		}

		// Handle modal shown event to allow modals stacking
		$(document).on('shown.bs.modal', '.modal', (evt) => {
			const handler = $(evt.currentTarget).data('ams-shown-handler') || modalShownEventHandler;
			MyAMS.core.executeFunctionByName(handler, document, evt);
		});

		// Handle modal hidden event to check remaining modals
		$(document).on('hidden.bs.modal', '.modal', (evt) => {
			const handler = $(evt.currentTarget).data('ams-hidden-handler') || modalHiddenEventHandler;
			MyAMS.core.executeFunctionByName(handler, document, evt);
		});
	},

	open: (source, options) => {
		return new Promise((resolve, reject) => {
			let sourceData = {},
				url = source;
			if (typeof source !== 'string') {
				sourceData = source.data();
				url = source.attr('href') || sourceData.amsUrl;
			}
			const urlGetter = MyAMS.core.getFunctionByName(url);
			if (typeof urlGetter === 'function') {
				url = urlGetter(source);
			}
			if (!url) {
				reject("No provided URL!");
			}
			if (url.startsWith('#')) {  // Open inner modal
				$(url).modal('show');
				resolve();
			} else {
				$.ajax({
					type: 'get',
					url: url,
					cache: sourceData.amsAllowCache === undefined ? false : sourceData.amsAllowCache,
					data: options
				}).then((data, status, request) => {
					let modal = null;
					MyAMS.require('ajax').then(() => {
						const
							response = MyAMS.ajax.getResponse(request),
							dataType = response.contentType,
							result = response.data;
						let content,
							dialog,
							dialogData,
							dialogOptions,
							settings;
						switch (dataType) {
							case 'json':
								MyAMS.ajax.handleJSON(result,
									$($(source).data('ams-json-target') || '#content'));
								break;
							case 'script':
							case 'xml':
								break;
							case 'html':
							case 'text':
							default:
								content = $(result),
								dialog = $('.modal-dialog', content.wrap('<div></div>').parent()),
								dialogData = dialog.data() || {},
								dialogOptions = {
									backdrop: dialogData.backdrop === undefined ? 'static' : dialogData.backdrop,
									keyboard: dialogData.keyboard === undefined ? true : dialogData.keyboard
								};
								settings = $.extend({}, dialogOptions, dialogData.amsOptions);
								settings = MyAMS.core.executeFunctionByName(dialogData.amsInit, dialog, settings) || settings;
								modal = $('<div>').addClass('modal fade')
									.attr('tabIndex', '-1')
									.data('dynamic', true)
									.append(content)
									.on('show.bs.modal', dynamicModalShowEventHandler)
									.on('shown.bs.modal', dynamicModalShownEventHandler)
									.on('hidden.bs.modal', dynamicModalHiddenEventHandler)
									.modal(settings);
								if (MyAMS.stats &&
									!((sourceData.amsLogEvent === false) ||
										(dialogData.amsLogEvent === false))) {
									MyAMS.stats.logPageview(url);
								}
						}
					}).then(() => {
						resolve(modal);
					});
				});
			}
		});
	},

	fitWidthToImage: (evt, options) => {
		setTimeout(() => {
			const
				source = evt.currentTarget,
				image = options ? $(options['resize-target']) : source;
			if (image.exists()) {
				const
					dialog = image.parents('.modal-dialog'),
					padding = dialog.width() - image.width();
				dialog.css('max-width',
					Math.min($(window).width(), image.get(0).naturalWidth + padding));
			}
		}, 150);
	},

	/**
	 * Close modal associated with given element
	 *
	 * @param element: the element contained into closed modal
	 */
	close: (element) => {
		if (typeof element === 'string') {
			element = $(element);
		} else if (typeof element === 'undefined') {
			element = $('.modal-dialog:last');
		}
		const dialog = element.objectOrParentWithClass('modal');
		if (dialog.length > 0) {
			dialog.modal('hide');
		}
	}
};


/**
 * Global module initialization
 */
if (MyAMS.env.bundle) {
	MyAMS.config.modules.push('modal');
} else {
	MyAMS.modal = modal;
	console.debug("MyAMS: modal module loaded...");
}
