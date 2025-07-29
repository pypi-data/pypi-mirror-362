/**
 * MyAMS core features
 *
 * This script is used to build MyAMS core-package.
 *
 * This package only includes MyAMS core features, but not CSS or external modules
 * which can be loaded using MyAMS.require function.
 */

import MyAMS, { init } from "./ext-base";
import myams_require from "./ext-require";


MyAMS.$.extend(MyAMS, {
	require: myams_require
});

const html = MyAMS.$('html');
if (html.data('ams-init') !== false) {
	init(MyAMS.$);
}


/** Version: $version$  */
