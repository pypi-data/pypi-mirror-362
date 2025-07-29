/* global MyAMS, clipboardData */
/**
 * MyAMS i18n translations
 */

const $ = MyAMS.$;


/**
 * Internal function used to copy text to clipboard
 *
 * @param text: text to be copied
 */
function doCopy(text) {
	let copied = false;
	if (window.clipboardData && window.clipboardData.setData) {
		// IE specific code
		copied = clipboardData.setData("Text", text);
	} else if (document.queryCommandSupported && document.queryCommandSupported('copy')) {
		const textarea = $('<textarea>');
		textarea.val(text)
			.css('position', 'fixed')  // prevent scrolling to bottom of page in Edge
			.appendTo(MyAMS.dom.root);
		textarea.get(0).select();
		try {
			document.execCommand('copy');  // security exception may be thrown by some browsers!
			copied = true;
		} catch (e) {
			console.warn("Clipboard copy failed!", e);
		} finally {
			textarea.remove();
		}
	}
	if (copied) {
		MyAMS.require('i18n', 'alert').then(() => {
			MyAMS.alert.smallBox({
				status: 'success',
				message: text.length > 1 ? MyAMS.i18n.CLIPBOARD_TEXT_COPY_OK
					: MyAMS.i18n.CLIPBOARD_CHARACTER_COPY_OK,
				icon: 'fa-info-circle',
				timeout: 3000
			});
		});
	} else {
		MyAMS.require('i18n').then(() => {
			prompt(MyAMS.i18n.CLIPBOARD_COPY, text);
		});
	}
}


export const clipboard = {

	/**
	 * Copy given text to system's clipboard
	 *
	 * @param text: text to be copied
	 */
	copy: (text) => {
		if (typeof text === 'undefined') {
			return function() {
				const
					source = $(this),
					text = source.text();
				source.parents('.btn-group').removeClass('open');
				doCopy(text);
			};
		} else {
			doCopy(text);
		}
	},

	/**
	 * Copy input value or text to system's clipboard
	 */
	copyText: (event) => {
		const
			source = $(event.currentTarget),
			input = $(source.data('ams-clipboard-target')),
			value = input.val() || input.text();
		doCopy(value);
	}
};


/**
 * Global module initialization
 */
if (window.MyAMS) {
	if (MyAMS.env.bundle) {
		MyAMS.config.modules.push('clipboard');
	} else {
		MyAMS.clipboard = clipboard;
		console.debug("MyAMS: clipboard module loaded...");
	}
}
