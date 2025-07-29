/* global MyAMS, FontAwesome, Hammer */
/**
 * MyAMS navigation module
 */

const $ = MyAMS.$;


/**
 * Dynamic navigation menu class
 */
class MenuHeader {

	constructor(props) {
		this.props = props;
	}

	render() {
		return $('<li class="header"></li>')
			.text(this.props.header || '');
	}
}

class MenuDivider {

	render() {
		return $('<li class="divider"></li>');
	}
}

class Menu {

	constructor(items) {
		this.items = items;
	}

	render() {
		const menu = $('<div></div>');
		for (const item of this.items) {
			if (item.label) {
				const
					props = $('<li></li>'),
					link = $('<a></a>')
						.attr('href', item.href || '#')
						.attr('title', item.label);
				for (const [key, val] of Object.entries(item.attrs || {})) {
					link.attr(key, val);
				}
				if (item.icon) {
					$('<i class="fa-lg fa-fw mr-1"></i>')
						.addClass(item.icon)
						.appendTo(link);
				}
				$('<span class="menu-item-parent"></span>')
					.text(item.label)
					.appendTo(link);
				if (item.badge) {
					$('<span class="badge ml-1 mr-3 float-right"></span>')
						.addClass(`bg-${item.badge.status}`)
						.text(item.badge.value)
						.appendTo(link);
				}
				link.appendTo(props);
				if (item.items) {
					$('<ul></ul>')
						.append(new Menu(item.items).render())
						.appendTo(props);
				}
				props.appendTo(menu);
			} else {
				new MenuDivider().render().appendTo(menu);
			}
		}
		return menu.children();
	}
}

export class NavigationMenu {

	constructor(menus, parent, settings) {
		this.menus = menus;
		this.parent = parent;
		this.settings = settings;
	}

	getMenus() {
		const nav = $('<ul></ul>');
		for (const props of this.menus) {
			if (props.header !== undefined) {
				nav.append(new MenuHeader(props).render());
			}
			nav.append(new Menu(props.items).render());
		}
		return nav;
	}

	render() {
		const menus = this.getMenus();
		this.init(menus);
		this.parent.append(menus);
	}

	init(menus) {
		const settings = this.settings;
		// add mark to menus with children
		menus.find('li').each((idx, elt) => {
			const menuItem = $(elt);
			if (menuItem.find('ul').length > 0) {
				const firstLink = menuItem.find('a:first');
				// add multi-level sign next to link
				const sign = $(`<b class="collapse-sign">${settings.closedSign}</b>`);
				sign.on('click', (evt) => {
					evt.preventDefault();
				});
				firstLink.append(sign);
				// avoid jumping to top of page when href is a #
				if (firstLink.attr('href') === '#') {
					firstLink.click(() => {
						return false;
					});
				}
			}
		});
		// slide down open menus
		menus.find('li.open').each((idx, elt) => {
			const
				menu = $(elt),
				subMenu = $('> ul', menu);
			subMenu.slideDown(settings.speed);
			menu.find('>a b.collapse-sign').html(settings.openedSign);
		});
		// open active level
		menus.find('li.active').each((idx, elt) => {
			const
				activeParent = $(elt).parents('ul'),
				activeItem = activeParent.parent('li');
			activeParent.slideDown(settings.speed);
			activeItem.find('b:first').html(settings.openedSign);
			activeItem.addClass('open');
		});
		// handle click event
		menus.find("li a").on('click', (evt) => {
			const link = $(evt.currentTarget);
			if (link.hasClass('active')) {
				return;
			}
			link.parents('li').removeClass('active');
			const
				href = link.attr('href').replace(/^#/, ''),
				parentUL = link.parent().find("ul");
			if (settings.accordion) {
				const
					parents = link.parent().parents("ul"),
					visibleMenus = menus.find("ul:visible");
				visibleMenus.each((visibleIndex, visibleElt) => {
					let close = true;
					parents.each((parentIndex, parentElt) => {
						if (parentElt === visibleElt) {
							close = false;
							return false;
						}
					});
					if (close && (parentUL !== visibleElt)) {
						const visibleItem = $(visibleElt);
						if (href || !visibleItem.hasClass('active')) {
							visibleItem.slideUp(settings.speed, () => {
								visibleItem.parent("li")
									.removeClass('open')
									.find("b:first")
									.delay(settings.speed)
									.html(settings.closedSign);
							});
						}
					}
				});
			}
			const firstUL = link.parent().find("ul:first");
			if (!href && firstUL.is(":visible") && !firstUL.hasClass("active")) {
				firstUL.slideUp(settings.speed, () => {
					link.parent("li")
						.removeClass("open")
						.find("b:first")
						.delay(settings.speed)
						.html(settings.closedSign);
				});
			} else {
				firstUL.slideDown(settings.speed, () => {
					link.parent("li")
						.addClass("open")
						.find("b:first")
						.delay(settings.speed)
						.html(settings.openedSign);
				});
			}
		});
	}
}


let _initialized = false,
	_hammer = null;


/**
 * Main navigation module
 */

function _openPage(href) {
	if (location && href.startsWith('#')) {
		if (href !== location.hash) {
			location.hash = href;
		}
	} else {
		if (location.toString() === href) {
			location.reload();
		} else {
			window.location = href;
		}
	}
}

/**
 * Main link click event handler
 *
 * @param evt
 */
export function linkClickHandler(evt) {
	return new Promise((resolve, reject) => {
		const
			link = $(evt.currentTarget),
			handlers = link.data('ams-disabled-handlers');
		if ((handlers === true) || (handlers === 'click') || (handlers === 'all')) {
			return;
		}
		let href = link.attr('href') || link.data('ams-url');
		if (!href ||
			href.startsWith('javascript:') ||
			link.attr('target') ||
			(link.data('ams-context-menu') === true)) {
			return;
		}
		evt.preventDefault();
		evt.stopPropagation();

		let url,
			target,
			params;
		if (href.indexOf('?') >= 0) {
			url = href.split('?');
			target = url[0];
			params = url[1].unserialize();
		} else {
			target = href;
			params = undefined;
		}
		const hrefGetter = MyAMS.core.getFunctionByName(target);
		if (typeof hrefGetter === 'function') {
			href = hrefGetter(link, params);
		}
		if (!href) {
			resolve(null);
		}
		else if (typeof href === 'function') {
			resolve(href(link, params));
		} else {
			// Standard AJAX or browser URL call
			// Convert %23 characters to #
			href = href.replace(/%23/, '#');
			if (evt.ctrlKey) {
				window.open && window.open(href);
				resolve();
			} else {
				const linkTarget = link.data('ams-target') || link.attr('target');
				if (linkTarget) {
					if (linkTarget === '_blank') {
						window.open && window.open(href);
						resolve();
					} else if (linkTarget === '_top') {
						window.location = href;
						resolve();
					} else {
						if (MyAMS.form) {
							MyAMS.form.confirmChangedForm().then((result) => {
								if (result !== 'success') {
									return;
								}
								MyAMS.skin && MyAMS.skin.loadURL(href, linkTarget,
									link.data('ams-link-options'),
									link.data('ams-link-callback')).then(resolve, reject);
							});
						} else {
							MyAMS.skin && MyAMS.skin.loadURL(href, linkTarget,
								link.data('ams-link-options'),
								link.data('ams-link-callback')).then(resolve, reject);
						}
					}
				} else {
					if (MyAMS.form) {
						MyAMS.form.confirmChangedForm().then((result) => {
							if (result !== 'success') {
								return;
							}
							_openPage(href);
						}).then(resolve);
					} else {
						_openPage(href);
						resolve();
					}
				}
			}
		}
	});
}


export const nav = {

	/**
	 * initialize navigation through data attributes
	 */
	init: () => {

		if (_initialized) {
			return;
		}
		_initialized = true;

		$.fn.extend({

			navigationMenu: function(options) {
				if (this.length === 0) {
					return;
				}
				const data = this.data();
				const defaults = {
					accordion: data.amsMenuAccordion !== false,
					speed: 200
				}
				if (MyAMS.config.useSVGIcons) {
					const
						downIcon = FontAwesome.findIconDefinition({iconName: 'angle-down'}),
						upIcon = FontAwesome.findIconDefinition({iconName: 'angle-up'});
					$.extend(defaults, {
						closedSign: `<em data-fa-i2svg>${FontAwesome.icon(downIcon).html}</em>`,
						openedSign: `<em data-fa-i2svg>${FontAwesome.icon(upIcon).html}</em>`
					});
				} else {
					$.extend(defaults, {
						closedSign: '<em class="fa fa-angle-down"></em>',
						openedSign: '<em class="fa fa-angle-up"></em>'
					});
				}
				const
					settings = $.extend({}, defaults, options),
					menuFactory = MyAMS.core.getObject(data.amsMenuFactory) || NavigationMenu;
				if (data.amsMenuConfig) {
					MyAMS.require('ajax', 'skin').then(() => {
						MyAMS.ajax.get(data.amsMenuConfig).then(result => {
							new menuFactory(result, $(this), settings).render();
							MyAMS.skin.checkURL();
						});
					});
				} else {  // static menus
					const menus = $('ul', this);
					new menuFactory(null, $(this), settings).init(menus);
				}
			}
		});

		if (MyAMS.config.ajaxNav) {

			// Disable clicks on # hrefs
			$(document).on('click', 'a[href="#"]', (evt) => {
				evt.preventDefault();
				evt.stopPropagation();
			});

			// Activate clicks
			$(document).on('click',
				'a[href!="#"]:not([data-toggle]), [data-ams-url]:not([data-toggle])', (evt) => {
				// disable click on dragging element
				if ($(evt.currentTarget).data('is-dragging')) {
					return;
				}
				// check for specific click handler
				const handler = $(evt).data('ams-click-handler');
				if (handler) {
					return;
				}
				// check for DataTable collapse handler
				if (evt.target.tagName === 'TD') {
					const target = $(evt.target);
					if (target.hasClass('dtr-control')) {
						const table = target.parents('table.datatable');
						if (table.hasClass('collapsed')) {
							return;
						}
					}
				}
				return linkClickHandler(evt);
			});

			// Blank target clicks
			$(document).on('click', 'a[target="_blank"]', (evt) => {
				evt.preventDefault();
				evt.stopPropagation();
				const target = $(evt.currentTarget);
				window.open && window.open(target.attr('href'));
				MyAMS.stats && MyAMS.stats.logEvent(
					target.data('ams-stats-category') || 'Navigation',
					target.data('ams-stats-action') || 'External',
					target.data('ams-stats-label') || target.attr('href'));
			});

			// Top target clicks
			$(document).on('click', 'a[target="_top"]', (evt) => {
				evt.preventDefault();
				MyAMS.form && MyAMS.form.confirmChangedForm().then((result) => {
					if (result !== 'success') {
						return;
					}
					window.location = $(evt.currentTarget).attr('href');
				})
			});

			// Disable clicks on disabled tabs
			$(document).on("click", '.nav-tabs a[data-toggle=tab]', (evt) => {
				if ($(evt.currentTarget).parent('li').hasClass("disabled")) {
					evt.preventDefault();
					evt.stopPropagation();
					return false;
				}
			});

			// Enable tabs dynamic loading
			$(document).on('show.bs.tab', (evt) => {
				let link = $(evt.target);
				if (link.exists() && (link.get(0).tagName !== 'A')) {
					link = $('a[href]', link);
				}
				const data = link.data();
				if (data && data.amsUrl) {
					if (data.amsTabLoaded) {
						return;
					}
					link.append('<i class="fa fa-spin fa-cog ml-1"></i>');
					MyAMS.require('skin').then(() => {
						MyAMS.skin.loadURL(data.amsUrl, link.attr('href')).then(() => {
							if (data.amsTabLoadOnce) {
								data.amsTabLoaded = true;
							}
							$('i', link).remove();
						}, () => {
							$('i', link).remove();
						});
					});
				}
			});

			if (!MyAMS.config.isMobile) {
				MyAMS.dom.root.addClass('desktop-detected');
			} else {
				MyAMS.dom.root.addClass('mobile-detected');
				MyAMS.require('ajax').then(() => {
					if (MyAMS.config.enableFastclick) {
						MyAMS.ajax.check($.fn.noClickDelay,
							`${MyAMS.env.baseURL}../ext/js-smartclick${MyAMS.env.extext}.js`).then(() => {
							$('a', MyAMS.dom.nav).noClickDelay();
							$('a', '#hide-menu').noClickDelay();
						});
					}
					if (MyAMS.dom.root.exists()) {
						MyAMS.ajax.check(window.Hammer,
							`${MyAMS.env.baseURL}../ext/hammer${MyAMS.env.extext}.js`).then(() => {
							_hammer = new Hammer.Manager(MyAMS.dom.root.get(0));
							_hammer.add(new Hammer.Pan({
								direction: Hammer.DIRECTION_HORIZONTAL,
								threshold: 200
							}));
							_hammer.on('panright', () => {
								if (!MyAMS.dom.root.hasClass('hidden-menu')) {
									MyAMS.nav.switchMenu();
								}
							});
							_hammer.on('panleft', () => {
								if (MyAMS.dom.root.hasClass('hidden-menu')) {
									MyAMS.nav.switchMenu();
								}
							});
						});
					}
				});
			}
		}

		nav.restoreState();
	},

	initElement: (element) => {

		$('nav', element).navigationMenu({
			speed: MyAMS.config.menuSpeed
		});
	},

	/**
	 * Display current active menu
	 *
 	 * @param menu: current active menu
	 */
	setActiveMenu: (menu) => {
		const nav = MyAMS.dom.nav;
		$('.active', nav).removeClass('active');
		menu.addClass('open')
			.addClass('active');
		menu.parents('li').addClass('open active')
			.children('ul').addClass('active')
			.show();
		menu.parents('li:first').removeClass('open');
		menu.parents('ul').addClass(menu.attr('href').replace(/^#/, '') ? 'active' : '')
			.show();
		if (menu.exists()) {
			const
				scroll = nav.scrollTop(),
				position = $(menu).parents('li:last').position();
			if (position.top < scroll) {
				nav.scrollTop(position.top);
			} else if (position.top > nav.height() + scroll) {
				nav.scrollTop(position.top);
			}
		}
	},

	/**
	 * Internal breadcrumbs drawing function
	 *
	 * @private
	 */
	drawBreadcrumbs: () => {
		const crumb = $('ol.breadcrumb', '#ribbon');
		$('li', crumb).not('.persistent').remove();
		if (!$('li', crumb).exists()) {
			const template = `<li class="breadcrumb-item">
					<a class="p-r-1" href="${$('a[href!="#"]:first', MyAMS.dom.nav).attr('href')}">
						${MyAMS.i18n.HOME}
					</a>
				</li>`;
			crumb.append($(template));
		}
		$('li.active >a', MyAMS.dom.nav).each((idx, elt) => {
			const
				menu = $(elt),
				text = $.trim(menu.clone()
					.children('.badge')
					.remove()
					.end()
					.text()),
				href = menu.attr('href'),
				item = $('<li class="breadcrumb-item"></li>').append(href.replace(/^#/, '') ?
					$('<a></a>').html(text).attr('href', href) : text);
			crumb.append(item);
		});
	},

	/**
	 * Click handler for navigation menu "minify" button
	 *
	 * @param evt: original click event
	 */
	minifyMenu: (evt) => {
		evt && evt.preventDefault();
		MyAMS.dom.root.toggleClass('minified');
		if (MyAMS.dom.root.hasClass('minified')) {
			MyAMS.core.switchIcon($('i', evt.currentTarget),
				'arrow-circle-left', 'arrow-circle-right');
		} else {
			MyAMS.core.switchIcon($('i', evt.currentTarget),
				'arrow-circle-right', 'arrow-circle-left');
		}
		if (window.localStorage) {
			if (MyAMS.dom.root.hasClass('minified')) {
				localStorage.setItem('window-state', 'minified');
			} else {
				localStorage.setItem('window-state', '');
			}
		}
	},

	/**
	 * Click handler for menu hide button
	 *
	 * @param evt: original click event
	 */
	switchMenu: (evt) => {
		evt && evt.preventDefault();
		MyAMS.dom.root.toggleClass('hidden-menu');
		if (window.localStorage) {
			if (MyAMS.dom.root.hasClass('hidden-menu')) {
				localStorage.setItem('window-state', 'hidden-menu');
			} else {
				localStorage.setItem('window-state', '');
			}
		}
	},

	/**
	 * Restore window state on application startup
	 *
	 * Previous window state is stored in local storage.
	 */
	restoreState: () => {
		// restore window state
		if (window.localStorage) {
			const state = localStorage.getItem('window-state');
			if (state === 'minified') {
				MyAMS.nav.minifyMenu({
					currentTarget: $('#minifyme'),
					preventDefault: () => {}
				});
			} else {
				MyAMS.dom.root.addClass(state);
			}
		}
	}
};


/**
 * Global module initialization
 */
if (MyAMS.env.bundle) {
	MyAMS.config.modules.push('nav');
} else {
	MyAMS.nav = nav;
	console.debug("MyAMS: nav module loaded...");
}
