/* global MyAMS */
/**
 * MyAMS xxx module
 */

const $ = MyAMS.$;


export const _mod = {

};


/**
 * Global module initialization
 */
if (MyAMS.env.bundle) {
	MyAMS.config.modules.push('_mod');
} else {
	MyAMS._mod = _mod;
	console.debug("MyAMS: _mod module loaded...");
}
