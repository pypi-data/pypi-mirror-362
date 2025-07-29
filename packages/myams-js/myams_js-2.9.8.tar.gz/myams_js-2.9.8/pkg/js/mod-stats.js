/* global MyAMS */
/**
 * MyAMS stats management
 */

const $ = MyAMS.$;


export const stats = {

	logPageview: function() {

	},

	logEvent: function() {

	}
};


/**
 * Global module initialization
 */
if (window.MyAMS) {
	if (MyAMS.env.bundle) {
		MyAMS.config.modules.push('stats');
	} else {
		MyAMS.stats = stats;
		console.debug("MyAMS: stats module loaded...");
	}
}
