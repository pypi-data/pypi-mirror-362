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
    global.modAjax = mod.exports;
  }
})(typeof globalThis !== "undefined" ? globalThis : typeof self !== "undefined" ? self : this, function (_exports) {
  "use strict";

  Object.defineProperty(_exports, "__esModule", {
    value: true
  });
  _exports.ajax = void 0;
  /* global jQuery, MyAMS, Cookies */
  /**
   * MyAMS AJAX features
   */

  const $ = MyAMS.$;

  /**
   * CSRF cookie checker
   *
   * Automatically set CSRF request header when CSRF cookie was specified.
   *
   * @param request: outgoing request
   */
  function checkCsrfHeader(request /*, options */) {
    if (window.Cookies) {
      const token = Cookies.get(MyAMS.config.csrfCookieName);
      if (token) {
        request.setRequestHeader(MyAMS.config.csrfHeaderName, token);
      }
    }
  }
  const ajax = _exports.ajax = {
    /**
     * Check for a given feature, and download script if necessary
     *
     * @param checker: pointer to a resource which will be downloaded if undefined
     * @param source: URL of a javascript file containing requested resource
     */
    check: (checker, source) => {
      return new Promise((resolve, reject) => {
        const deferred = [];
        if (checker === undefined) {
          if (!(source instanceof Array)) {
            source = [source];
          }
          for (const src of source) {
            deferred.push(MyAMS.core.getScript(src));
          }
        } else {
          if (!(checker instanceof Array)) {
            checker = [checker];
          }
          checker.forEach((elt, idx) => {
            if (elt === undefined) {
              deferred.push(MyAMS.core.getScript(source[idx]));
            }
          });
        }
        $.when.apply($, deferred).then(() => {
          resolve(deferred.length > 0);
        }, reject);
      });
    },
    /**
     * Get AJAX URL relative to current page
     *
     * @param addr
     */
    getAddr: addr => {
      const href = addr || $('html head base').attr('href') || window.location.href;
      return href.substring(0, href.lastIndexOf('/') + 1);
    },
    /**
     * JQuery AJAX start callback
     */
    start: () => {
      $('#ajax-gear').show();
    },
    /**
     * JQuery AJAX stop callback
     */
    stop: () => {
      $('#ajax-gear').hide();
    },
    /**
     * Handle AJAX upload or download progress event
     *
     * @param event: source event
     */
    progress: event => {
      if (!event.lengthComputable) {
        return;
      }
      if (event.loaded >= event.total) {
        return;
      }
      if (console) {
        console.debug && console.debug(`${Math.round(event.loaded / event.total * 100)}%`);
      }
    },
    /**
     * Get data from given URL.
     * This is a simple wrapper around JQuery AJAX api to keep MyAMS API consistent
     *
     * @param url: target URL
     * @param params: url params
     * @param options: AJAX call options
     */
    get: (url, params, options) => {
      return new Promise((resolve, reject) => {
        let addr;
        if (url.startsWith(window.location.protocol)) {
          addr = url;
        } else {
          addr = MyAMS.ajax.getAddr() + url;
        }
        const defaults = {
          url: addr,
          type: 'get',
          cache: false,
          data: $.param(params || null),
          dataType: 'json',
          beforeSend: checkCsrfHeader
        };
        const settings = $.extend({}, defaults, options);
        $.ajax(settings).then((result, status, xhr) => {
          resolve(result, status, xhr);
        }, (xhr, status, error) => {
          reject(error);
        });
      });
    },
    /**
     * Post data to given URL
     *
     * @param url: target URL
     * @param data: submit data
     * @param options: AJAX call options
     */
    post: (url, data, options) => {
      return new Promise((resolve, reject) => {
        let addr;
        if (url.startsWith(window.location.protocol)) {
          addr = url;
        } else {
          addr = MyAMS.ajax.getAddr() + url;
        }
        let postData;
        if (data && options && options.contentType && options.contentType.startsWith('application/json')) {
          postData = JSON.stringify(data);
        } else {
          postData = $.param(data || null);
        }
        const defaults = {
          url: addr,
          type: 'post',
          cache: false,
          data: postData,
          dataType: 'json',
          beforeSend: checkCsrfHeader
        };
        const settings = $.extend({}, defaults, options);
        $.ajax(settings).then((result, status, xhr) => {
          resolve(result, status, xhr);
        }, (xhr, status, error) => {
          reject(error);
        });
      });
    },
    /**
     * Post data to given URL and handle result as JSON
     *
     * This form of function can be used in MyAMS "href" or "data-ams-url" attributes, like in
     * <a href="MyAMS.ajax.getJSON?url=...">Click me!</a>.
     */
    getJSON: () => {
      return (source, options) => {
        const url = options.url;
        delete options.url;
        return MyAMS.ajax.post(url, options).then(MyAMS.ajax.handleJSON);
      };
    },
    /**
     * Extract datatype and result from response object
     */
    getResponse: request => {
      let dataType = 'unknown',
        result;
      if (request) {
        let contentType = request.getResponseHeader('content-type');
        if (!contentType) {
          try {
            contentType = request.responseXML.contentType;
          } catch (e) {
            contentType = null;
          }
        }
        if (contentType) {
          // Get server response
          if (contentType.startsWith('application/javascript')) {
            result = request.responseText;
            dataType = 'script';
          } else if (contentType.startsWith('text/html')) {
            result = request.responseText;
            dataType = 'html';
          } else if (contentType.startsWith('text/xml')) {
            result = request.responseText;
            dataType = 'xml';
          } else {
            // Supposed to be JSON...
            result = request.responseJSON;
            if (result) {
              dataType = 'json';
            } else {
              try {
                result = JSON.parse(request.responseText);
                dataType = 'json';
              } catch (e) {
                result = request.responseText;
                dataType = 'binary';
              }
            }
          }
        } else {
          // Probably no response from server...
          result = {
            status: 'alert',
            alert: {
              title: MyAMS.i18n.ERROR_OCCURED,
              content: MyAMS.i18n.NO_SERVER_RESPONSE
            }
          };
          dataType = 'json';
        }
      }
      return {
        contentType: dataType,
        data: result
      };
    },
    /**
     * Handle a server response in JSON format
     *
     * Result can be an object with several attributes:
     *  - main response status: alert, error, info, success, callback, callbacks, reload or
     *    redirect
     *  - close_form: boolean indicating if current modal should be closed
     *  - location: target URL for reload or redirect status
     *  - target: target container selector for loaded content ('#content' by default)
     *  - content: available for any status producing output; can be raw HTML, or an object
     *    with attributes:
     *      - target: target container selector (source form by default)
     *      - text or html: raw text or HTML result
     *  - message: available for any status producing an output message; an object with
     *    attributes:
     *      - status: message status
     *      -
     * @param result: response content
     * @param form: source form
     * @param target
     */
    handleJSON: (result, form, target) => {
      function closeForm() {
        return new Promise((resolve, reject) => {
          if (form !== undefined) {
            MyAMS.require('form').then(() => {
              MyAMS.form.resetChanged(form);
            }).then(() => {
              if (result.closeForm !== false) {
                MyAMS.require('modal').then(() => {
                  MyAMS.modal.close(form);
                }).then(resolve, reject);
              } else {
                resolve();
              }
            });
          } else {
            resolve();
          }
        });
      }
      let url = null,
        loadTarget = null;
      const status = result.status,
        promises = [];
      if (target instanceof jQuery && !target.length) {
        target = null;
      }
      switch (status) {
        case 'alert':
          if (window.alert) {
            const alert = result.alert;
            window.alert(`${alert.title}\n\n${alert.content}`);
          }
          break;
        case 'error':
          promises.push(MyAMS.require('error').then(() => {
            MyAMS.error.showErrors(form, result);
          }));
          break;
        case 'message':
        case 'messagebox':
        case 'smallbox':
          break;
        case 'info':
        case 'success':
        case 'notify':
        case 'callback':
        case 'callbacks':
          promises.push(closeForm());
          break;
        case 'modal':
          promises.push(MyAMS.require('modal').then(() => {
            MyAMS.modal.open(result.location);
          }));
          break;
        case 'reload':
          closeForm();
          url = result.location || window.location.hash;
          if (url.startsWith('#')) {
            url = url.substring(1);
          }
          loadTarget = $(result.target || target || '#content');
          promises.push(MyAMS.require('skin').then(() => {
            MyAMS.skin.loadURL(url, loadTarget, {
              preLoadCallback: MyAMS.core.getFunctionByName(result.preReload || function () {
                $('[data-ams-pre-reload]', loadTarget).each((index, element) => {
                  MyAMS.core.executeFunctionByName($(element).data('ams-pre-reload'));
                });
              }),
              preLoadCallbackOptions: result.preReloadOptions,
              afterLoadCallback: MyAMS.core.getFunctionByName(result.postReload || function () {
                $('[data-ams-post-reload]', loadTarget).each((index, element) => {
                  MyAMS.core.executeFunctionByName($(element).data('ams-post-reload'));
                });
              }),
              afterLoadCallbackOptions: result.postReloadOptions
            });
          }));
          break;
        case 'redirect':
          closeForm();
          url = result.location || window.location.href;
          if (url.endsWith('##')) {
            url = url.replace(/##/, window.location.hash);
          }
          if (result.window) {
            window.open(url, result.window, result.options);
          } else {
            $(window).off('beforeunload');
            if (window.location.href === url) {
              window.location.reload();
            } else {
              window.location.replace(url);
            }
          }
          break;
        default:
          if (result.code) {
            // Standard HTTP error?
            promises.push(MyAMS.require('error').then(() => {
              MyAMS.error.showHTTPError(result);
            }));
          } else {
            if (window.console) {
              console.warn && console.warn(`Unhandled JSON response status: ${status}`);
            }
          }
      }

      // Single content response
      if (result.content) {
        const content = result.content,
          container = $(content.target || target || '#content');
        if (typeof content === 'string') {
          container.html(content);
        } else {
          if (content.text) {
            container.text(content.text);
          } else {
            container.html(content.html);
          }
          promises.push(MyAMS.core.executeFunctionByName(MyAMS.config.initContent, document, container).then(() => {
            if (!content.keepHidden) {
              container.removeClass('hidden');
            }
          }));
        }
      }

      // Multiple contents response
      if (result.contents) {
        for (const content of result.contents) {
          const container = $(content.target);
          if (content.text) {
            container.text(content.text);
          } else {
            container.html(content.html);
          }
          promises.push(MyAMS.core.executeFunctionByName(MyAMS.config.initContent, document, container).then(() => {
            if (!content.keepHidden) {
              container.removeClass('hidden');
            }
          }));
        }
      }

      // Response with message
      if (result.message && !result.code) {
        promises.push(MyAMS.require('alert').then(() => {
          if (typeof result.message === 'string') {
            MyAMS.alert.smallBox({
              status: status,
              message: result.message,
              icon: 'fa-info-circle',
              timeout: 3000
            });
          } else {
            const message = result.message;
            MyAMS.alert.alert({
              parent: form,
              status: message.status || status,
              header: message.header,
              subtitle: message.subtitle,
              message: message.message
            });
          }
        }));
      }

      // Response with message box
      if (result.messagebox) {
        promises.push(MyAMS.require('alert').then(() => {
          if (typeof result.messagebox === 'string') {
            MyAMS.alert.messageBox({
              status: status,
              title: MyAMS.i18n.ERROR_OCCURED,
              icon: 'fa-info-circle',
              message: result.messagebox,
              timeout: 10000
            });
          } else {
            const message = result.messagebox;
            MyAMS.alert.messageBox({
              status: message.status || status,
              title: message.title || MyAMS.i18n.ERROR_OCCURED,
              icon: message.icon || 'fa-info-circle',
              message: message.message,
              content: message.content,
              timeout: message.timeout === 0 ? 0 : message.timeout || 10000
            });
          }
        }));
      }

      // Response with small box
      if (result.smallbox) {
        promises.push(MyAMS.require('alert').then(() => {
          if (typeof result.smallbox === 'string') {
            MyAMS.alert.smallBox({
              status: status,
              message: result.smallbox,
              icon: 'fa-info-circle',
              timeout: 3000
            });
          } else {
            const message = result.smallbox;
            MyAMS.alert.smallBox({
              status: message.status || status,
              message: message.message,
              content: message.content,
              icon: message.icon || 'fa-info-circle',
              timeout: message.timeout
            });
          }
        }));
      }

      // Response with single event
      if (result.event) {
        form.trigger(result.event, result.eventOptions);
      }

      // Response with multiple events
      if (result.events) {
        for (const event of result.events) {
          if (typeof event === 'string') {
            form.trigger(event, result.eventOptions);
          } else {
            form.trigger(event.event, event.options);
          }
        }
      }

      // Response with single callback
      if (result.callback) {
        promises.push(MyAMS.core.executeFunctionByName(result.callback, document, form, result.options));
      }

      // Response with multiple callbacks
      if (result.callbacks) {
        for (const callback of result.callbacks) {
          if (typeof callback === 'string') {
            promises.push(MyAMS.core.executeFunctionByName(callback, document, form, result.options));
          } else {
            promises.push(MyAMS.require(callback.module || []).then(() => {
              MyAMS.core.executeFunctionByName(callback.callback, document, form, callback.options);
            }));
          }
        }
      }
      return Promise.all(promises);
    },
    /**
     * JQuery AJAX error handler
     */
    error: (event, response, request, error) => {
      // user shouldn't be notified of aborted requests
      if (error === 'abort') {
        return;
      }
      // don't display errors on OK status
      if (response && response.statusText && response.statusText.toUpperCase() === 'OK') {
        return;
      }
      // don't display errors twice (via AJAX HTTP error handler and JSON response)
      if (response.x_ams_handled === true) {
        return;
      }
      const parsedResponse = MyAMS.ajax.getResponse(response);
      if (parsedResponse) {
        if (parsedResponse.contentType === 'json') {
          MyAMS.ajax.handleJSON(parsedResponse.data);
          response.x_ams_handled = true;
        } else {
          MyAMS.require('i18n', 'alert').then(() => {
            const title = error || event.statusText || event.type,
              message = parsedResponse.responseText;
            MyAMS.alert.messageBox({
              status: 'error',
              title: MyAMS.i18n.ERROR_OCCURED,
              content: `<h4>${title}</h4><p>${message || ''}</p>`,
              icon: 'fa-exclamation-triangle',
              timeout: 5000
            });
          }, () => {
            if (window.console) {
              console.error && console.error(event);
              console.debug && console.debug(parsedResponse);
            }
          });
        }
      } else {
        if (window.console) {
          console.error && console.error("ERROR: Can't parse response!");
          console.debug && console.debug(response);
        }
      }
    }
  };

  /**
   * AJAX events callbacks
   */
  if (typeof jest === 'undefined') {
    // don't check cookies extension in test mode!
    ajax.check(window.Cookies, `${MyAMS.env.baseURL}../ext/js-cookie${MyAMS.env.extext}.js`).then(() => {
      const xhr = $.ajaxSettings.xhr;
      $.ajaxSetup({
        beforeSend: (request, options) => {
          if (MyAMS.config.safeMethods.indexOf(options.type) < 0) {
            if (window.Cookies !== undefined) {
              const token = Cookies.get(MyAMS.config.csrfCookieName);
              if (token) {
                request.setRequestHeader(MyAMS.config.csrfHeaderName, token);
              }
            }
          }
        },
        progress: ajax.progress,
        progressUpload: ajax.progress,
        xhr: function () {
          const request = xhr();
          if (request && typeof request.addEventListener === 'function') {
            if (ajax.progress) {
              request.addEventListener('progress', evt => {
                MyAMS.ajax.progress(evt);
              }, false);
            }
          }
          return request;
        }
      });
    });
  }
  $(document).ajaxStart(ajax.start);
  $(document).ajaxStop(ajax.stop);
  $(document).ajaxError(ajax.error);

  /**
   * Global module initialization
   */
  if (MyAMS.env.bundle) {
    MyAMS.config.modules.push('ajax');
  } else {
    MyAMS.ajax = ajax;
    console.debug("MyAMS: AJAX module loaded...");
  }
});
//# sourceMappingURL=mod-ajax-dev.js.map
