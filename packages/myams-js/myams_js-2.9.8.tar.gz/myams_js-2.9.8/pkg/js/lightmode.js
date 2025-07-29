/**
 * MyAMS core features
 *
 * This script is used to build MyAMS complete package.
 * This package includes jQuery, Bootstrap and MyAMS base package, and all modules
 * which can be loaded using MyAMS.require function.
 *
 * Alternate MyAMS bundles include:
 *  - mini: all MyAMS features, without JQuery / Bootstrap / FontAwesome resources (which
 *    are available separately)
 *  - core: MyAMS base features, without loadable modules or external resources (which
 *    are available separately)
 */

import "popper.js";
import "bootstrap";
import "hammerjs";


import MyAMS, { init } from "./ext-base";
import myams_require from "./ext-require";

import { error } from "./mod-error";
import { ajax } from "./mod-ajax";
import { i18n } from "./mod-i18n";
import { nav } from "./mod-nav";
import { skin } from "./mod-skin";
import { alert } from "./mod-alert";
import { modal } from "./mod-modal";
import { form } from "./mod-form";
import { events } from "./mod-events";
import { callbacks } from "./mod-callbacks";
import { clipboard } from "./mod-clipboard";
import { container } from "./mod-container";
import { datatable } from "./mod-datatable";
import { graph } from "./mod-graph";
import { helpers } from "./mod-helpers";
import { menu } from "./mod-menu";
import { notifications } from "./mod-notifications";
import { tree } from "./mod-tree";
import { jsonrpc } from "./mod-jsonrpc";
import { xmlrpc } from "./mod-xmlrpc";
import { stats } from "./mod-stats";

import "./mod-plugins";


import "@fortawesome/fontawesome-free/css/all.css";
import "../../src/myams_js/static/css/prod/lightmode.css";


MyAMS.$.extend(MyAMS, {
	theme: 'lightmode',
	require: myams_require,
	ajax: ajax,
	alert: alert,
	callbacks: callbacks,
	clipboard: clipboard,
	container: container,
	datatable: datatable,
	error: error,
	events: events,
	form: form,
	graph: graph,
	helpers: helpers,
	i18n: i18n,
	jsonrpc: jsonrpc,
	menu: menu,
	modal: modal,
	nav: nav,
	notifications: notifications,
	skin: skin,
	stats: stats,
	tree: tree,
	xmlrpc: xmlrpc
});

const html = MyAMS.$('html');
if (html.data('ams-init') !== false) {
	init(MyAMS.$);
}


/** Version: $version$  */
