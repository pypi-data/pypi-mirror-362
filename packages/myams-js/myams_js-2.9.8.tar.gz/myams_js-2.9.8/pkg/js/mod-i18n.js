/* global MyAMS */
/**
 * MyAMS i18n translations
 */

const $ = MyAMS.$;

let _initialized = false;


export const i18n = {

	language: 'en',

	INFO: "Information",
	WARNING: "!! WARNING !!",
	ERROR: "ERROR: ",

	LOADING: "Loading...",
	PROGRESS: "Processing",

	WAIT: "Please wait!",
	FORM_SUBMITTED: "This form was already submitted...",
	NO_SERVER_RESPONSE: "No response from server!",

	ERROR_OCCURED: "An error occured!",
	ERRORS_OCCURED: "Some errors occured!",

	BAD_LOGIN_TITLE: "Bad login!",
	BAD_LOGIN_MESSAGE:
		"Your anthentication credentials didn't allow you to open a session; " +
		"please check your credentials or contact administrator.",

	CONFIRM: "Confirm",
	CONFIRM_REMOVE: "Removing this content can't be undone. Do you confirm?",

	BTN_OK: "OK",
	BTN_CANCEL: "Cancel",
	BTN_YES: "Yes",
	BTN_NO: "No",
	BTN_CLOSE: "Close",

	CLIPBOARD_COPY: "Copy to clipboard with Ctrl+C, and Enter",
	CLIPBOARD_CHARACTER_COPY_OK: "Character copied to clipboard.",
	CLIPBOARD_TEXT_COPY_OK: "Text copied to clipboard.",

	FORM_CHANGED_WARNING: "Some changes were not saved. These updates will be lost if you leave this page.",
	DELETE_WARNING: "This change can't be undone. Are you sure that you want to delete this element?",
	NO_UPDATE: "No changes were applied.",
	DATA_UPDATED: "Data successfully updated.",

	HOME: "Home",
	LOGOUT: "Logout?",
	LOGOUT_COMMENT: "You can improve your security further after logging out by closing this opened browser",

	LAST_UPDATE: "Last update: ",

	DT_COLUMNS: "Columns",

	NO_SELECTED_VALUE: "No selected value",

	/**
	 * Plug-ins translations container
	 */
	plugins: {
		datatables: {
			search:            "",
			searchPlaceholder: "Search..."
		}
	},


	/**
	 * MyAMS i18n package
	 */
	init: (force=false) => {
		return new Promise((resolve, reject) => {
			if (_initialized && !force) {
				resolve();
				return;
			}
			_initialized = true;
			const
				html = $('html'),
				lang = html.attr('lang') || html.attr('xml:lang');
			if (lang && !lang.startsWith('en')) {
				MyAMS.core.getScript(`${MyAMS.env.baseURL}i18n/myams-${lang.substr(0, 2)}.js`)
					.then(resolve, reject);
			} else {
				resolve();
			}
		});
	}
};


/**
 * Global module initialization
 */
if (MyAMS.env.bundle) {
	MyAMS.config.modules.push('i18n');
} else {
	MyAMS.i18n = i18n;
	console.debug("MyAMS: I18n module loaded...");
}
