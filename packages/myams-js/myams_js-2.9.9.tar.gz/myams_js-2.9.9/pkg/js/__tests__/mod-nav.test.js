/* global describe, beforeAll, afterAll, jest, test, expect */
/*
 * MyAMS nav module tests
 */

import $ from "jquery";

import MyAMS, { init } from "../ext-base";
import { form } from "../mod-form";
import { i18n } from "../mod-i18n";

import {
	nav,
	NavigationMenu
} from "../mod-nav";


import myams_require from "../ext-require";

const bs = require("bootstrap");
// Bootstrap tabs are required...
$.fn.tab = bs.Tab._jQueryInterface;
$.fn.tab.Constructor = bs.Tab;


if (!MyAMS.nav) {
	MyAMS.nav = nav;
	MyAMS.config.modules.push('nav');
}
if (!MyAMS.form) {
	MyAMS.form = form;
	MyAMS.config.modules.push('form');
}
if (!MyAMS.i18n) {
	MyAMS.i18n = i18n;
	MyAMS.config.modules.push('i18n');
}
MyAMS.require = myams_require;

init($);


describe("MyAMS.ajax unit tests", () => {

	let oldOpen = null,
		oldAlert = null,
		oldLocation = null;

	beforeAll(() => {
		oldOpen = window.open;
		window.open = jest.fn();

		oldAlert = window.alert;
		window.alert = jest.fn();

		oldLocation = window.location;
		delete window.location;
		window.location = {
			protocol: oldLocation.protocol,
			href: oldLocation.href,
			url: oldLocation.url,
			hash: oldLocation.hash,
			reload: jest.fn()
		}
	});

	afterAll(() => {
		window.open = oldOpen;
		window.alert = oldAlert;
		window.location = oldLocation;
	});

	// Test MyAMS.nav initialization
	test("Test MyAMS.nav init function", () => {

		document.body.innerHTML = `<div>
			<nav></nav>
		</div>`;

		const body = $(document.body);
		MyAMS.dom = {
			root: body
		};
		nav.init();
		expect($.fn.navigationMenu).toBeDefined();
		expect(MyAMS.dom.root.hasClass('desktop-detected')).toBe(true);

	});


	// Test MyAMS.nav initElement
	test("Test MyAMS.nav initElement function", () => {

		document.body.innerHTML = `<div>
			<div id="ribbon">
				<ol class="breadcrumb"></ol>
			</div>
			<nav data-ams-menu-accordion="true">
				<ul>
					<li class="header">MyAMS.js</li>
					<li class="active">
						<a id="menu1" href="#summary.html">
							<i class="fa fa-lg fa-fw fa-question-circle mr-1"></i>
							What is MyAMS?
						</a>
					</li>
					<li>
						<a id="menu2" href="blank.html" target="_blank">Blank link</a>
					</li>
					<li class="divider"></li>
					<li>
						<a id="menu3" href="top.html" target="_top">Top link</a>
					</li>
					<li>
						<a id="menu4" href="#">Empty link</a>
						<ul>
							<li>
								<a id="menu5" href="#submenu.html">Sub menu</a>
							</li>
						</ul>
					</li>
					<li>
						<a id="menu6" href="MyAMS.test.caller1">JS call</a>
					</li>
					<li>
						<a id="menu7" href="MyAMS.test.caller2">JS call</a>
					</li>
					<li>
						<a id="menu8" href="MyAMS.test.caller3?param=2">JS call</a>
					</li>
				</ul>
			</nav>
		</div>`;

		const
			body = $(document.body),
			nav = $('nav', body);
		MyAMS.dom = {
			root: body,
			nav: nav
		};
		MyAMS.test = {
			caller1: (link, params) => {
				$(link).data('called', true);
				return '#called1.html'
			},
			caller2: (link, params) => {
				return () => {
					$(link).data('called', true);
				}
			},
			caller3: (link, params) => {
				return () => {
					$(link).data('param', params.param);
				}
			}
		}
		MyAMS.nav.init();
		MyAMS.nav.initElement(body);

		// check menu contents
		expect($('.collapse-sign', '#menu4').exists()).toBe(true);

		// check menu click
		$('#menu1').click();
		expect($('#menu1').parent('li').hasClass('open')).toBe(false);

		$('#menu4').click();
		expect($('#menu4').parent('li').hasClass('open')).toBe(true);

		const menu5 = $('#menu5');
		menu5.click();
		MyAMS.nav.setActiveMenu(menu5);
		MyAMS.nav.drawBreadcrumbs();
		expect($('li', '#ribbon').length).toBe(3);
		expect($('li:eq(0) a', '#ribbon').attr('href')).toBe('#summary.html');
		expect($('li:eq(0) a', '#ribbon').text().trim()).toBe(MyAMS.i18n.HOME);
		expect($('li:eq(1) a', '#ribbon').attr('href')).toBe(undefined);
		expect($('li:eq(2) a', '#ribbon').attr('href')).toBe('#submenu.html');

		// test simple callback
		$('#menu6').click();
		expect($('#menu6').data('called')).toBe(true);

		// test function callback
		$('#menu7').click();
		expect($('#menu7').data('called')).toBe(true);

		// test function callback with params
		$('#menu8').click();
		expect($('#menu8').data('param')).toBe('2');

		// coverage tests!
		// $('#menu2').click();
		// expect(window.open).toHaveBeenCalled();
		//
		// $('#menu3').click();

		delete MyAMS.test;

	});

	test("Test MyAMS.nav NavigationMenu class", () => {

		document.body.innerHTML = `<div>
			<div id="ribbon">
				<ol class="breadcrumb">
					<li class="persistent">
						<a href="/">MyAMS.js</a>
					</li>
				</ol>
			</div>
			<nav data-ams-menu-accordion="true"></nav>
		</div>`;

		const
			body = $(document.body),
			nav = $('nav', body);
		MyAMS.dom = {
			root: body,
			nav: nav
		};
		MyAMS.nav.init();
		const
			settings = {
				accordion: true,
				speed: 200
			},
			config = [
				{
					header: "MyAMS.js",
					items: [
						{
							label: "What is MyAMS?",
							href: "#summary.html",
							icon: "fa fa-question-circle",
							badge: {
								value: "1",
								status: "danger"
							},
							attrs: {
								id: 'menu1'
							}
						},
						{
							label: "Blank link",
							href: "#blank.html",
							attrs: {
								id: 'menu2',
								target: '_blank'
							}
						},
						{
							label: ""
						},
						{
							label: "Top link",
							href: "#top.html",
							attrs: {
								id: 'menu3',
								target: '_top'
							}
						},
						{
							label: "Empty link",
							attrs: {
								id: 'menu4'
							},
							items: [
								{
									label: "Sub menu",
									href: "#submenu.html",
									attrs: {
										id: 'menu5'
									}
								}
							]
						}
					]
				}
			];
		new NavigationMenu(config, nav, settings).render();

		// check menu contents
		expect($('li', nav).length).toBe(7);
		expect($('.collapse-sign', '#menu4').exists()).toBe(true);
		expect($('#menu1').exists()).toBe(true);
		expect($('#menu2').attr('target')).toBe('_blank');

		// check menu click
		$('#menu1').click();
		expect($('#menu1').parent('li').hasClass('open')).toBe(false);

		const menu4 = $('#menu4');
		menu4.click();
		expect(menu4.parent('li').hasClass('open')).toBe(true);

		MyAMS.nav.setActiveMenu(menu4);
		expect(menu4.hasClass('open')).toBe(true);
		expect(menu4.hasClass('active')).toBe(true);

		const menu5 = $('#menu5');
		menu5.click();
		MyAMS.nav.setActiveMenu(menu5);
		MyAMS.nav.drawBreadcrumbs();
		expect($('li', '#ribbon').length).toBe(3);
		expect($('li:eq(0) a', '#ribbon').attr('href')).toBe('/');
		expect($('li:eq(1) a', '#ribbon').attr('href')).toBe(undefined);
		expect($('li:eq(2) a', '#ribbon').attr('href')).toBe('#submenu.html');

	});


	// Test MyAMS.nav minifyMenu
	test("Test MyAMS.nav minifyMenu function", () => {

		document.body.innerHTML = `<div>
			<a id="minifymenu"><i></i></a>
		</div>`;
		const body = $(document.body);
		MyAMS.dom = {
			root: body
		};
		const event = {
			currentTarget: $('#minifymenu'),
			preventDefault: () => {
			}
		};

		MyAMS.nav.minifyMenu(event);
		expect(body.hasClass('minified')).toBe(true);
		expect($('i', '#minifymenu').hasClass('fa-arrow-circle-right')).toBe(true);

		MyAMS.nav.minifyMenu(event);
		expect(body.hasClass('minified')).toBe(false);
		expect($('i', '#minifymenu').hasClass('fa-arrow-circle-left')).toBe(true);

	});


	// Test MyAMS.nav switchMenu
	test("Test MyAMS.nav switchMenu function", () => {

		document.body.innerHTML = `<div></div>`;

		const body = $(document.body);
		MyAMS.dom = {
			root: body
		};
		const event = {
			preventDefault: () => {
			}
		};

		MyAMS.nav.switchMenu(event);
		expect(body.hasClass('hidden-menu')).toBe(true);

		MyAMS.nav.switchMenu(event);
		expect(body.hasClass('hidden-menu')).toBe(false);

	});
});
