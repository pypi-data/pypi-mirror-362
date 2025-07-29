/* global MyAMS */
/**
 * MyAMS datatables management
 */

const $ = MyAMS.$;


export const datatable = {

};


/**
 * Global module initialization
 */
if (window.MyAMS) {
	if (MyAMS.env.bundle) {
		MyAMS.config.modules.push('datatable');
	} else {
		MyAMS.datatable = datatable;
		console.debug("MyAMS: datatable module loaded...");
	}
}
