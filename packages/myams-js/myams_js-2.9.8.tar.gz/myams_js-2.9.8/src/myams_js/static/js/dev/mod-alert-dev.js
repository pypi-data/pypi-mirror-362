(function (global, factory) {
  if (typeof define === "function" && define.amd) {
    define(["exports"], factory);
  } else if (typeof exports !== "undefined") {
    factory(exports);
  } else {
    var mod = {
      exports: {}
    };
    factory(mod.exports);
    global.modAlert = mod.exports;
  }
})(typeof globalThis !== "undefined" ? globalThis : typeof self !== "undefined" ? self : this, function (_exports) {
  "use strict";

  Object.defineProperty(_exports, "__esModule", {
    value: true
  });
  _exports.alert = void 0;
  /* global MyAMS */
  /**
   * MyAMS alerts management
   */

  const $ = MyAMS.$;
  if (!$.templates) {
    const jsrender = require('jsrender');
    $.templates = jsrender.templates;
  }

  /**
   * Alert template
   */
  const ALERT_TEMPLATE_STRING = `
	<div class="alert alert-{{:status}}" role="alert">
		<button type="button" class="close" data-dismiss="alert" 
				aria-label="{{*: MyAMS.i18n.BTN_CLODE }}">
			<i class="fa fa-times" aria-hidden="true"></i>	
		</button>
		{{if header}}
		<h5 class="alert-heading">{{:header}}</h5>
		{{/if}}
		{{* if (typeof message === 'string') { }}
		<ul>
			<li>{{:message}}</li>
		</ul>
		{{* } else { }}
		<ul>
		{{for message}}
			<li>{{:}}</li>
		{{/for}}
		</ul>
		{{* } }}
	</div>`;
  const ALERT_TEMPLATE = $.templates({
    markup: ALERT_TEMPLATE_STRING,
    allowCode: true
  });

  /**
   * Standard message template
   */

  const MESSAGE_TEMPLATE_STRING = `
	<div role="alert" class="toast toast-{{:status}} fade hide"
		 data-autohide="{{*: Boolean(data.timeout !== 0).toString() }}"
		 data-delay="{{: timeout || 5000}}">
		<div class="toast-header">
		{{if icon}}
			<i class="fa {{:icon}} mr-2"></i>
		{{/if}}
			<strong class="mr-auto">{{:title}}</strong>
		{{if !hideTimestamp}}
			<small>{{*: new Date().toLocaleTimeString() }}</small>
		{{/if}}
			<button type="button" class="ml-2 mb-1 close" data-dismiss="toast">
				<i class="fa fa-times text-white"></i>
			</button>
		</div>
		<div class="toast-body">
			<div>
			{{if content}}
				{{:content}}
			{{else}}
				<p>{{:message}}</p>
			{{/if}}
			</div>
		</div>
	</div>`;
  const MESSAGE_TEMPLATE = $.templates({
    markup: MESSAGE_TEMPLATE_STRING,
    allowCode: true
  });

  /**
   * Small box message template
   */

  const SMALLBOX_TEMPLATE_STRING = `
	<div role="alert" class="toast toast-{{:status}} fade hide"
		 data-autohide="true"
		 data-delay="{{: timeout || 5000}}">
		<div class="toast-body">
			<div>
			{{if content}}
				{{:content}}
			{{else}}
				<span>
					{{if icon}}
					<i class="fa {{:icon}} mr-2"></i>
					{{/if}}
					{{:message}}
				</span>
			{{/if}}
			</div>
		</div>
	</div>`;
  const SMALLBOX_TEMPLATE = $.templates({
    markup: SMALLBOX_TEMPLATE_STRING,
    allowCode: true
  });

  /**
   * Big box message template
   */

  const BIGBOX_TEMPLATE_STRING = `
	<div class="modal fade" data-backdrop="static" role="dialog">
		<div class="modal-dialog">
			<div class="modal-content">
				<div class="modal-header alert-{{:status}}">
					<h5 class="modal-title">
					{{if icon}}
						<i class="fa {{:icon}} mr-2"></i>
					{{/if}}
					{{:title}}
					</h5>
					<button type="button" class="close" 
							data-dismiss="modal" data-modal-dismiss-value="cancel">
						<i class="fa fa-times"></i>
					</button>
				</div>
				<div class="modal-body">
					<p>{{:message}}</p>
				</div>
				<div class="modal-footer">
					<button type="button" class="btn btn-primary" 
							data-dismiss="modal" data-modal-dismiss-value="success">
						{{*: data.successLabel || MyAMS.i18n.BTN_OK }}
					</button>
					<button type="button" class="btn btn-secondary" 
							data-dismiss="modal" data-modal-dismiss-value="cancel">
						{{*: data.cancelLabel || MyAMS.i18n.BTN_CANCEL }}
					</button>
				</div>
			</div>
		</div>
	</div>`;
  const BIGBOX_TEMPLATE = $.templates({
    markup: BIGBOX_TEMPLATE_STRING,
    allowCode: true
  });

  /**
   * Main alert object
   */

  const alert = _exports.alert = {
    /**
     * Display alert message into current document
     *
     * @param props:
     *  - parent: DOM element which should receive the alert
     *  - status: alert status ('info', 'success', 'warning', 'danger'...)
     *  - header: alert header
     *  - subtitle: message sub-title
     *  - message: main alert message
     */
    alert: function () {
      let props = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
      let status = props.status || 'info';
      if (status === 'error') {
        status = 'danger';
      }
      props.status = status;
      $(`.alert-${status}`, props.parent).not('.persistent').remove();
      $(ALERT_TEMPLATE.render(props)).prependTo(props.parent);
      MyAMS.require('helpers').then(() => {
        MyAMS.helpers.scrollTo('#content', props.parent, {
          offset: -15
        });
      });
    },
    /**
     * Display notification message on bottom right
     *
     * @param props: message properties:
     *  - status: message status: 'info', 'success', 'warning', 'danger'
     *  - title: message title
     *  - icon: message icon
     *  - content: full HTML content
     *  - message: simple string message
     *  - hideTimestamp: boolean value to specify if timestamp must be hidden
     *  - timeout: timeout in ms; default to 5000, set to 0 to disable auto-hide
     */
    messageBox: function () {
      let props = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
      let status = props.status || 'info';
      if (status === 'error') {
        status = 'danger';
      }
      props.status = status;
      let wrapper = $(`.${MyAMS.config.alertsContainerClass}`);
      if (wrapper.length === 0) {
        wrapper = $('<div></div>').addClass(MyAMS.config.alertsContainerClass).appendTo(MyAMS.dom.root);
      }
      $(MESSAGE_TEMPLATE.render(props)).appendTo(wrapper).toast('show').on('hidden.bs.toast', evt => {
        $(evt.currentTarget).remove();
      });
    },
    /**
     * Display small notification message on top right
     *
     * @param props
     */
    smallBox: function () {
      let props = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
      let status = props.status || 'info';
      if (status === 'error') {
        status = 'danger';
      }
      props.status = status;
      let wrapper = $(`.${MyAMS.config.alertsContainerClass}`);
      if (wrapper.length === 0) {
        wrapper = $('<div></div>').addClass(MyAMS.config.alertsContainerClass).appendTo(MyAMS.dom.root);
      }
      $(SMALLBOX_TEMPLATE.render(props)).appendTo(wrapper).toast('show').on('hidden.bs.toast', evt => {
        $(evt.currentTarget).remove();
      });
    },
    /**
     * Modal message box
     *
     * @param props
     * @returns {Promise<unknown>}
     */
    bigBox: function () {
      let props = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
      return new Promise((resolve, reject) => {
        let status = props.status || 'info';
        if (status === 'error') {
          status = 'danger';
        }
        props.status = status;
        MyAMS.require('modal').then(() => {
          const alert = $(BIGBOX_TEMPLATE.render(props)).appendTo(MyAMS.dom.root);
          alert.on('shown.bs.modal', evt => {
            $('.btn-primary', evt.target).focus();
          });
          alert.on('hidden.bs.modal', () => {
            resolve(alert.data('modal-result'));
            alert.remove();
          });
          alert.modal('show');
        }, () => {
          reject("Missing 'modal' module!");
        });
      });
    }
  };

  /**
   * Global module initialization
   */
  if (window.MyAMS) {
    if (MyAMS.env.bundle) {
      MyAMS.config.modules.push('alert');
    } else {
      MyAMS.alert = alert;
      console.debug("MyAMS: alert module loaded...");
    }
  }
});
//# sourceMappingURL=mod-alert-dev.js.map
