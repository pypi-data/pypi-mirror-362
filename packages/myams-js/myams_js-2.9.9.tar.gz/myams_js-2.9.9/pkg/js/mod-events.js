/* global MyAMS */
/**
 * MyAMS events management
 */

const $ = MyAMS.$;

let _initialized = false;


export const events = {

	init: () => {

		if (_initialized) {
			return;
		}
		_initialized = true;

		// Initialize custom click handlers
		$(document).on('click', '[data-ams-click-handler]', MyAMS.events.clickHandler);

		// Initialize custom change handlers
		$(document).on('change', '[data-ams-change-handler]', MyAMS.events.changeHandler);

		// Initialize custom event on click
		$(document).on('click', '[data-ams-click-event]', MyAMS.events.triggerEvent);

	},

	initElement: (element) => {
		$('[data-ams-events-handlers]', element).each((idx, elt) => {
			const
				source = $(elt),
				handlers = source.data('ams-events-handlers');
			if (handlers) {
				const
					selector = source.data('ams-events-handlers-context'),
					context = selector ? source.parents(selector) : source;
				for (const [event, handler] of Object.entries(handlers)) {
					context.on(event, (event, ...options) => {
						if (options.length > 0) {
							MyAMS.core.executeFunctionByName(handler, document, event, ...options);
						} else {
							MyAMS.core.executeFunctionByName(handler, document, event,
								source.data('ams-events-options') || {});
						}
					});
				}
			}
		});
	},

	/**
	 * Get events handlers on given element for a specific event
	 *
	 * @param element: the checked element
	 * @param event: event for which handlers lookup is made
	 * @returns: an array of elements for which the event handler is defined
	 */
	getHandlers: (element, event) => {

		const
			result = [],
			handlers = element.data('ams-events-handlers');
		if (handlers && handlers[event]) {
			result.push(element);
		}
		$('[data-ams-events-handlers]', element).each((idx, elt) => {
			const
				context = $(elt),
				handlers = context.data('ams-events-handlers');
			if (handlers && handlers[event]) {
				result.push(context);
			}
		});
		return result;
	},

	/**
	 * Generic click event handler
	 */
	clickHandler: (event) => {
		const
			source = $(event.currentTarget),
			handlers = source.data('ams-disabled-handlers');
		if ((handlers === true) || (handlers === 'click') || (handlers === 'all')) {
			return;
		}
		const data = source.data();
		if (data.amsClickHandler) {
			if ((data.amsPreventDefault !== false) && (data.amsClickPreventDefault !== false)) {
				event.preventDefault();
			}
			if ((data.amsStopPropagation !== false) && (data.amsClickStopPropagation !== false)) {
				event.stopPropagation();
			}
			for (const handler of data.amsClickHandler.split(/[\s,;]+/)) {
				const callback = MyAMS.core.getFunctionByName(handler);
				if (callback !== undefined) {
					callback.call(document, event, data.amsClickHandlerOptions);
				}
			}
		}
	},

	/**
	 * Generic change event handler
	 */
	changeHandler: (event) => {
		const source = $(event.currentTarget);
		// Disable change handlers for readonly inputs
		// These change handlers are activated by IE!!!
		if (source.prop('readonly')) {
			return;
		}
		const handlers = source.data('ams-disabled-handlers');
		if ((handlers === true) || (handlers === 'change') || (handlers === 'all')) {
			return;
		}
		const data = source.data();
		if (data.amsChangeHandler) {
			if ((data.amsKeepDefault !== false) && (data.amsChangeKeepDefault !== false)) {
				event.preventDefault();
			}
			if ((data.amsStopPropagation !== false) && (data.amsChangeStopPropagation !== false)) {
				event.stopPropagation();
			}
			for (const handler of data.amsChangeHandler.split(/[\s,;]+/)) {
				const callback = MyAMS.core.getFunctionByName(handler);
				if (callback !== undefined) {
					callback.call(document, event, data.amsChangeHandlerOptions);
				}
			}
		}
	},

	/**
	 * Generic click event trigger
	 */
	triggerEvent: (event) => {
		const source = $(event.currentTarget);
		$(event.target).trigger(source.data('ams-click-event'),
			source.data('ams-click-event-options'));
	}
};


/**
 * Global module initialization
 */
if (MyAMS.env.bundle) {
	MyAMS.config.modules.push('events');
} else {
	MyAMS.events = events;
	console.debug("MyAMS: events module loaded...");
}
