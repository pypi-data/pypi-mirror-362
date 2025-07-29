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
    global.modNotifications = mod.exports;
  }
})(typeof globalThis !== "undefined" ? globalThis : typeof self !== "undefined" ? self : this, function (_exports) {
  "use strict";

  Object.defineProperty(_exports, "__esModule", {
    value: true
  });
  _exports.notifications = void 0;
  /* global MyAMS */
  /**
   * MyAMS notifications handlers
   */

  const $ = MyAMS.$;
  if (!$.templates) {
    const jsrender = require('jsrender');
    $.templates = jsrender.templates;
  }

  /**
   * Notifications list template string
   */

  const ITEM_TEMPLATE_STRING = `
	<li class="p-1 my-1{{if status}} alert-{{:status}}{{/if}}">
		<a class="d-flex flex-row"{{if url}} href="{{:url}}"{{/if}}{{if modal}} data-toggle="modal"{{/if}}>
			{{if source.avatar}}
			<img class="avatar mx-1 mt-1" src="{{:source.avatar}}"
				 alt="{{:source.title}}" title="{{:source.title}}" />
			{{else}}
			<i class="avatar fa fa-fw fa-2x fa-user mx-1 mt-1"
			   title="{{:source.title}}"></i>
			{{/if}}
			<div class="flex-grow-1 ml-2">
				<small class="timestamp float-right text-muted">
					{{*: new Date(data.timestamp).toLocaleString()}}
				</small>
				<strong class="title d-block">
					{{:title}}
				</strong>
				<p class="text-muted mb-2">{{:message}}</p>
			</div>
		</a>
	</li>`;
  const ITEM_TEMPLATE = $.templates({
    markup: ITEM_TEMPLATE_STRING,
    allowCode: true
  });
  const LIST_TEMPLATE_STRING = `
	<ul class="list-style-none flex-grow-1 overflow-auto m-0 p-0">
		{{for notifications tmpl=~itemTemplate /}}
	</ul>
	{{if !~options.hideTimestamp}}
	<div class="timestamp border-top pt-1">
		<span>{{*: MyAMS.i18n.LAST_UPDATE }}{{: ~timestamp.toLocaleString() }}</span>
		<i class="fa fa-fw fa-sync float-right"
		   data-ams-click-handler="MyAMS.notifications.getNotifications"
		   data-ams-click-handler-options='{"localTimestamp": "{{: ~useLocalTime }}"}'></i>
	</div>
	{{/if}}`;
  const LIST_TEMPLATE = $.templates({
    markup: LIST_TEMPLATE_STRING,
    allowCode: true
  });
  class NotificationsList {
    /**
     * List constructor
     *
     * @param values: notifications data (may be loaded from JSON)
     * @param options: list rendering options
     */
    constructor(values) {
      let options = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : {};
      this.values = values;
      this.options = options;
    }

    /**
     * Render list into given parent
     *
     * @param parent: JQuery parent object into which the list must be rendered
     */
    render(parent) {
      $(parent).html(LIST_TEMPLATE.render(this.values, {
        itemTemplate: ITEM_TEMPLATE,
        timestamp: this.options.localTimestamp ? new Date() : new Date(this.values.timestamp),
        useLocalTime: this.options.localTimestamp ? 'true' : 'false',
        options: this.options
      }));
    }
  }
  const notifications = _exports.notifications = {
    /**
     * Check permission to display desktop notifications
     */
    checkPermission: () => {
      const checkNotificationPromise = () => {
        try {
          Notification.requestPermission().then();
        } catch (e) {
          return false;
        }
        return true;
      };
      return new Promise((resolve, reject) => {
        if (!('Notification' in window)) {
          console.debug("Notifications are not supported by this browser!");
          resolve(false);
        } else if (Notification.permission !== 'denied') {
          if (Notification.permission === 'default') {
            if (checkNotificationPromise()) {
              Notification.requestPermission().then(permission => {
                resolve(permission === 'granted');
              });
            } else {
              Notification.requestPermission(permission => {
                resolve(permission === 'granted');
              });
            }
          } else {
            resolve(true);
          }
        } else {
          resolve(false);
        }
      });
    },
    checkUserPermission: () => {
      MyAMS.notifications.checkPermission().then(() => {});
    },
    /**
     * Load user notifications
     *
     * @param evt: source event
     * @param options: notifications options (which can also be extracted from event data)
     */
    getNotifications: (evt, options) => {
      const data = $.extend({}, options, evt.data),
        target = $(evt.target),
        current = $(evt.currentTarget),
        remote = current.data('ams-notifications-source') || current.parents('[data-ams-notifications-source]').data('ams-notifications-source');
      return new Promise((resolve, reject) => {
        MyAMS.require('ajax').then(() => {
          MyAMS.ajax.get(remote, current.data('ams-notifications-params') || '', current.data('ams-notifications-options') || {}).then(result => {
            const tab = $(target.data('ams-notifications-target') || target.parents('[data-ams-notifications-target]').data('ams-notifications-target') || current.attr('href'));
            new NotificationsList(result, data).render(tab);
            $('#notifications-count').text('');
            notifications.checkUserPermission();
            localStorage.setItem('notifications-timestamp', new Date().toISOString());
            resolve();
          }, reject);
        }, reject);
      });
    },
    /**
     * Load new notifications badge
     */
    getNotificationsBadge: () => {
      const source = $('#user-notifications'),
        remote = source.data('ams-notifications-source');
      return new Promise((resolve, reject) => {
        const lastRefreshStorage = localStorage.getItem('notifications-timestamp');
        if (lastRefreshStorage === null) {
          localStorage.setItem('notifications-timestamp', new Date().toISOString());
        } else {
          MyAMS.require('ajax').then(() => {
            MyAMS.ajax.get(remote).then(result => {
              const lastRefresh = new Date(Date.parse(lastRefreshStorage)),
                newItems = (result.notifications || []).filter(item => new Date(typeof item.timestamp === 'number' ? item.timestamp : Date.parse(item.timestamp)) > lastRefresh);
              $('#notifications-count').text(newItems.length || '');
              resolve();
            }, reject);
          }, reject);
        }
      });
    },
    /**
     * Add new notification to notifications list
     *
     * @param message: notification element
     * @param showDesktop: if true, also try to display desktop notification
     */
    addNotification: (message, showDesktop) => {
      const pane = $('ul', '#notifications-pane'),
        notification = $(ITEM_TEMPLATE.render(message)),
        badge = $('#notifications-count'),
        count = parseInt(badge.text()) || 0;
      pane.prepend(notification);
      badge.text(count + 1);
      if (showDesktop) {
        notifications.showDesktopNotification(message);
      }
    },
    /**
     * Show new desktop notification
     *
     * @param message: notification elements
     */
    showDesktopNotification: message => {
      notifications.checkPermission().then(status => {
        if (!status) {
          return;
        }
        const options = {
            title: message.title,
            body: message.message,
            icon: message.source.avatar
          },
          notification = new Notification(options.title, options);
        if (message.url) {
          notification.onclick = () => {
            window.open(message.url);
          };
        }
      });
    }
  };

  /**
   * Global module initialization
   */
  if (MyAMS.env.bundle) {
    MyAMS.config.modules.push('notifications');
  } else {
    MyAMS.notifications = notifications;
    console.debug("MyAMS: notifications module loaded...");
  }
});
//# sourceMappingURL=mod-notifications-dev.js.map
