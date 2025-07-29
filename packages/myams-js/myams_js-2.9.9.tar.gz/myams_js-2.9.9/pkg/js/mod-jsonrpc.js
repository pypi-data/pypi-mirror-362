/* global MyAMS */
/**
 * MyAMS JSON-RPC protocol support
 */

const $ = MyAMS.$;


export const jsonrpc = {

};


/**
 * Global module initialization
 */
if (window.MyAMS) {
	if (MyAMS.env.bundle) {
		MyAMS.config.modules.push('jsonrpc');
	} else {
		MyAMS.jsonrpc = jsonrpc;
		console.debug("MyAMS: jsonrpc module loaded...");
	}
}
