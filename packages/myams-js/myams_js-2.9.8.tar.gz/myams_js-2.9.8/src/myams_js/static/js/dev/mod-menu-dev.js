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
    global.modMenu = mod.exports;
  }
})(typeof globalThis !== "undefined" ? globalThis : typeof self !== "undefined" ? self : this, function (_exports) {
  "use strict";

  Object.defineProperty(_exports, "__esModule", {
    value: true
  });
  _exports.menu = void 0;
  /* global MyAMS */
  /**
   * MyAMS menus management
   */

  const $ = MyAMS.$;

  /**
   * Context menu handler
   */
  function _contextMenuHandler(menu, source) {
    if (menu.get(0).tagName !== 'A') {
      menu = menu.parents('a').first();
    }
    const menuData = menu.data();
    if (menuData.toggle === 'modal') {
      MyAMS.require('modal').then(() => {
        MyAMS.modal.open(menu);
      });
    } else {
      let href = menu.attr('href') || menuData.amsUrl;
      if (!href || href.startsWith('javascript:') || menu.attr('target')) {
        return;
      }
      const hrefGetter = MyAMS.core.getFunctionByName(href);
      if (typeof hrefGetter === 'function') {
        href = hrefGetter(menu, source);
      }
      if (typeof href === 'undefined') {
        return;
      }
      if (typeof href === 'function') {
        href(menu);
      } else {
        MyAMS.require('form', 'skin').then(() => {
          href = href.replace(/%23/, '#');
          const target = menu.data('ams-target');
          if (target) {
            MyAMS.form.confirmChangedForm(target).then(status => {
              if (status !== 'success') {
                return;
              }
              MyAMS.skin.loadURL(href, target, menu.data('ams-link-options'), menu.data('ams-link-callback'));
            });
          } else {
            MyAMS.form.confirmChangedForm().then(status => {
              if (status !== 'success') {
                return;
              }
              if (href.startsWith('#')) {
                if (href !== location.hash) {
                  if (MyAMS.dom.root.hasClass('mobile-view-activated')) {
                    MyAMS.dom.root.removeClass('hidden-menu');
                    setTimeout(() => {
                      window.location.hash = href;
                    }, 50);
                  } else {
                    window.location.hash = href;
                  }
                }
              } else {
                window.location = href;
              }
            });
          }
        });
      }
    }
  }
  let _initialized = false;

  /**
   * MyAMS "menu" module
   */
  const menu = _exports.menu = {
    /**
     * Global module initialization.
     * This function extends jQuery with a "contextMenu()" function, which
     * allows to create a new context menu.
     */
    init: () => {
      if (_initialized) {
        return;
      }
      _initialized = true;
      $.fn.extend({
        /**
         * JQuery context menu constructor
         */
        contextMenu: function (settings) {
          function getMenuPosition(mouse, direction) {
            const win = $(window)[direction](),
              menu = $(settings.menuSelector)[direction]();
            let position = mouse;
            // opening menu would pass the side of the page
            if (mouse + menu > win && menu < mouse) {
              position -= menu;
            }
            return position;
          }
          return this.each((idx, elt) => {
            const source = $(elt),
              menu = $(settings.menuSelector);

            // Set flag on menu items
            $('a', menu).each((idx, elt) => {
              $(elt).data('ams-context-menu', true);
            });
            source.on("contextmenu", function (evt) {
              // return native menu if pressing CTRL key
              if (evt.ctrlKey) {
                return;
              }
              // open menu
              menu.data('contextmenu-event-source', source).dropdown('show').css({
                position: 'fixed',
                left: getMenuPosition(evt.clientX, 'width') - 10,
                top: getMenuPosition(evt.clientY, 'height') - 10
              }).off('click').on('click', clickEvt => {
                clickEvt.stopPropagation();
                clickEvt.preventDefault();
                menu.dropdown('hide');
                _contextMenuHandler($(clickEvt.target), source);
              });
              return false;
            });

            // make sure menu closes on any click
            $(document).click(() => {
              menu.dropdown('hide');
            });
          });
        }
      });

      // Automatically set orientation of dropdown menus
      $(document).on('show.bs.dropdown', '.btn-group', evt => {
        // check menu height
        const menu = $(evt.currentTarget),
          ul = menu.children('.dropdown-menu'),
          menuRect = menu.get(0).getBoundingClientRect(),
          position = menuRect.top,
          buttonHeight = menuRect.height,
          menuHeight = ul.outerHeight();
        if (position > menuHeight && $(window).height() - position < buttonHeight + menuHeight) {
          menu.addClass("dropup");
        }
        // activate first input
        $('input, select, textarea', ul).first().focus();
      }).on('hidden.bs.dropdown', '.btn-group', evt => {
        // always reset after close
        $(evt.currentTarget).removeClass('dropup');
      });
      $(document).on('hide.bs.dropdown', evt => {
        if (evt.clickEvent) {
          const dropdown = $(evt.clickEvent.target).parents('.dropdown-menu');
          if (dropdown.data('ams-click-dismiss') === false) {
            evt.preventDefault();
            return false;
          }
        }
      });
    }
  };

  /**
   * Global module initialization
   */
  if (window.MyAMS) {
    if (MyAMS.env.bundle) {
      MyAMS.config.modules.push('menu');
    } else {
      MyAMS.menu = menu;
      console.debug("MyAMS: menu module loaded...");
    }
  }
});
//# sourceMappingURL=mod-menu-dev.js.map
