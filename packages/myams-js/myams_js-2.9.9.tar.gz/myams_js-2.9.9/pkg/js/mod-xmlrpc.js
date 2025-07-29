/* global MyAMS */
/**
 * MyAMS XML-RPC protocol support
 */

const $ = MyAMS.$;


export const xmlrpc = {

};


/**
 * Global module initialization
 */
if (window.MyAMS) {
	if (MyAMS.env.bundle) {
		MyAMS.config.modules.push('xmlrpc');
	} else {
		MyAMS.xmlrpc = xmlrpc;
		console.debug("MyAMS: xmlrpc module loaded...");
	}
}
