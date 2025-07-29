/* global MyAMS */
/**
 * MyAMS graphs management
 */

const $ = MyAMS.$;


export const graph = {

};


/**
 * Global module initialization
 */
if (window.MyAMS) {
	if (MyAMS.env.bundle) {
		MyAMS.config.modules.push('graph');
	} else {
		MyAMS.graph = graph;
		console.debug("MyAMS: graph module loaded...");
	}
}
