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
    global.modSkin = mod.exports;
  }
})(typeof globalThis !== "undefined" ? globalThis : typeof self !== "undefined" ? self : this, function (_exports) {
  "use strict";

  Object.defineProperty(_exports, "__esModule", {
    value: true
  });
  _exports.skin = void 0;
  var _this = void 0;
  /* global MyAMS */
  /**
   * MyAMS generic skin features
   */

  const $ = MyAMS.$;
  let _initialized = false;
  const skin = _exports.skin = {
    /**
     * Main *skin* module initialization
     */
    init: () => {
      if (_initialized) {
        return;
      }
      _initialized = true;

      // handle tooltips
      if (MyAMS.config.enableTooltips) {
        MyAMS.dom.root.tooltip({
          selector: '.hint',
          html: MyAMS.config.enableHtmlTooltips
        });
      }
      $('.hint').mousedown(evt => {
        $(evt.currentTarget).tooltip('hide');
      });
      $(document).on('clear.ams.content', () => {
        $('.tooltip').remove();
      });

      // check URL when hash is changed
      skin.checkURL();
      $(window).on('hashchange', skin.checkURL);
    },
    /**
     * Specific content initialization
     *
     * @param element: the element to initialize
     */
    initElement: element => {
      if (!MyAMS.config.enableTooltips) {
        $('.hint', element).tooltip({
          html: MyAMS.config.enableHtmlTooltips
        });
      }
    },
    /**
     * URL checking function.
     *
     * This function is an event handler for window's "hashchange" event, which is
     * triggered when the window location hash is modified; this can notably occur when a
     * navigation menu, for example, is clicked.
     */
    checkURL: () => {
      return new Promise((resolve, reject) => {
        const nav = MyAMS.dom.nav;
        let hash = location.hash,
          url = hash.replace(/^#/, ''),
          tag = null;
        const tagPosition = url.indexOf('!');
        if (tagPosition > 0) {
          hash = hash.substring(0, tagPosition + 1);
          tag = url.substring(tagPosition + 1);
          url = url.substring(0, tagPosition);
        }
        let menu;
        if (url) {
          // new hash
          let container = $('#content');
          if (!container.exists()) {
            container = MyAMS.dom.root;
          }
          menu = $(`a[href="${hash}"]`, nav);
          // load specified URL into '#content'
          MyAMS.skin.loadURL(url, container).then(() => {
            const prefix = $('html head title').data('ams-title-prefix'),
              fullPrefix = prefix ? `${prefix} > ` : '';
            document.title = `${fullPrefix}${$('[data-ams-page-title]:first', container).data('ams-page-title') || menu.attr('title') || menu.text().trim() || document.title}`;
            if (tag) {
              const anchor = $(`#${tag}`);
              if (anchor.exists()) {
                MyAMS.require('helpers').then(() => {
                  MyAMS.helpers.scrollTo('#main', anchor, {
                    offset: -15
                  });
                });
              }
            }
            // try to activate matching navigation menu
            if (menu.exists()) {
              MyAMS.require('nav').then(() => {
                MyAMS.nav.setActiveMenu(menu);
                MyAMS.nav.drawBreadcrumbs();
              }).then(resolve);
            } else {
              resolve();
            }
          }, reject);
        } else {
          // empty hash! We try to check if a specific menu was activated with a custom
          // data attribute, otherwise we go to the first navigation menu!
          const activeUrl = $('[data-ams-active-menu]').data('ams-active-menu');
          if (activeUrl) {
            menu = $(`a[href="${activeUrl}"]`, nav);
          } else {
            menu = $('ul li a[href!="#"]', nav).first();
          }
          if (menu.length > 0) {
            MyAMS.require('nav').then(() => {
              MyAMS.nav.setActiveMenu(menu);
              if (activeUrl) {
                MyAMS.nav.drawBreadcrumbs();
              } else {
                // we use location.replace to avoid storing intermediate URL
                // into browser's history
                window.location.replace(window.location.href + menu.attr('href'));
              }
            }).then(resolve, reject);
          } else {
            resolve();
          }
        }
      });
    },
    /**
     * Load specific URL into given container target.
     *
     * The function returns a Promise which is resolved when the remote content is actually
     * loaded and initialized
     *
     * @param url: remote content URL
     * @param target: jQuery selector or target container
     * @param options: additional options to AJAX call
     * @returns {Promise<string>}
     */
    loadURL: function (url, target) {
      let options = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : {};
      return new Promise((resolve, reject) => {
        if (url.startsWith('#')) {
          url = url.substr(1);
        }
        target = $(target);
        MyAMS.core.executeFunctionByName(MyAMS.config.clearContent, document, target).then(status => {
          if (!status) {
            // applied veto!
            return;
          }
          const defaults = {
            type: 'GET',
            url: url,
            dataType: 'html',
            cache: false,
            beforeSend: () => {
              target.html(`<h1 class="loading"><i class="fa fa-cog fa-spin"></i> ${MyAMS.i18n.LOADING}</h1>`);
              if (options && options.preLoadCallback) {
                MyAMS.core.executeFunctionByName(options.preLoadCallback, _this, options.preLoadCallbackOptions);
              }
              if (target.attr('id') === 'content') {
                MyAMS.require('nav').then(() => {
                  const prefix = $('html head title').data('ams-title-prefix'),
                    fullPrefix = prefix ? `${prefix} > ` : '';
                  document.title = `${fullPrefix}${$('.breadcrumb li:last-child').text()}`;
                  MyAMS.dom.root.animate({
                    scrollTop: 0
                  }, 'fast');
                });
              }
            }
          };
          const settings = $.extend({}, defaults, options),
            veto = {
              veto: false
            };
          target.trigger('before-load.ams.content', [settings, veto]);
          if (veto.veto) {
            return;
          }
          $.ajax(settings).then((result, status, xhr) => {
            if ($.isArray(result)) {
              [result, status, xhr] = result;
            }
            MyAMS.require('ajax').then(() => {
              const response = MyAMS.ajax.getResponse(xhr);
              if (response) {
                const dataType = response.contentType,
                  result = response.data;
                $('.loading', target).remove();
                switch (dataType) {
                  case 'json':
                    MyAMS.ajax.handleJSON(result, target);
                    resolve(result, status, xhr);
                    break;
                  case 'script':
                  case 'xml':
                    resolve(result, status, xhr);
                    break;
                  case 'html':
                  case 'text':
                  default:
                    target.parents('.hidden').removeClass('hidden');
                    MyAMS.core.executeFunctionByName(target.data('ams-clear-content') || MyAMS.config.clearContent, document, target).then(() => {
                      target.css({
                        opacity: '0.0'
                      }).html(result).removeClass('hidden').delay(30).animate({
                        opacity: '1.0'
                      }, 300);
                      MyAMS.core.executeFunctionByName(target.data('ams-init-content') || MyAMS.config.initContent, window, target).then(() => {
                        MyAMS.form && MyAMS.form.setFocus(target);
                        if (options && options.afterLoadCallback) {
                          MyAMS.core.executeFunctionByName(options.afterLoadCallback, _this, options.afterLoadCallbackOptions).then(() => {
                            target.trigger('after-load.ams.content');
                            resolve(result, status, xhr);
                          }, reject);
                        } else {
                          target.trigger('after-load.ams.content');
                          resolve(result, status, xhr);
                        }
                      }, reject);
                    }, reject);
                }
                MyAMS.stats && MyAMS.stats.logPageview();
              }
            });
          }, (xhr, status, error) => {
            target.html(`<h3 class="error"><i class="fa fa-exclamation-triangle text-danger"></i> 
								${MyAMS.i18n.ERROR} ${error}</h3>${xhr.responseText}`);
            reject(error);
          });
        });
      });
    }
  };

  /**
   * Global module initialization
   */
  if (window.MyAMS) {
    if (MyAMS.env.bundle) {
      MyAMS.config.modules.push('skin');
    } else {
      MyAMS.skin = skin;
      console.debug("MyAMS: skin module loaded...");
    }
  }
});
//# sourceMappingURL=mod-skin-dev.js.map
