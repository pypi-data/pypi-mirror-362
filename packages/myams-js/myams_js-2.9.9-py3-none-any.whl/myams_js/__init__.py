#
# Copyright (c) 2015-2019 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""MyAMS.js package

MyAMS.js extension framework
"""

try:
    from importlib.resources import files
except ImportError:
    from importlib_resources import files

from fanstatic import Group, Library, Resource

from pyams_utils.fanstatic import ResourceWithData

__docformat__ = 'restructuredtext'


pkg_dir = str(files('myams_js') / 'static')

library = Library('myams', pkg_dir)


#
# MyAMS external resources
#

jquery = Resource(library, 'js/ext/jquery.js',
                  minified='js/ext/jquery.min.js')

jsrender = Resource(library, 'js/ext/jsrender.js',
                    minified='js/ext/jsrender.min.js',
                    depends=(jquery,))

bootstrap_css = Resource(library, 'css/ext/bootstrap.css',
                         minified='css/ext/bootstrap.min.css')

bootstrap = Resource(library, 'js/ext/bootstrap.js',
                     minified='js/ext/bootstrap.min.js',
                     depends=(jquery,))

fontawesome_css = Resource(library, 'css/ext/fontawesome-all.css',
                           minified='css/ext/fontawesome-all.min.css')

fontawesome_js = ResourceWithData(library, 'js/ext/fontawesome.js',
                                  minified='js/ext/fontawesome.min.js',
                                  data={
                                      'auto-replace-svg': 'nest',
                                      'search-pseudo-elements': ''
                                  })


#
# MyAMS bundles
#

myams_full_bundle = ResourceWithData(library, 'js/dev/myams-dev.js',
                                     minified='js/prod/myams.js')

myams_css = Resource(library, 'css/dev/myams.css',
                     minified='css/prod/myams.css')

myams_mini_js = Resource(library, 'js/dev/myams-mini-dev.js',
                         minified='js/prod/myams-mini.js',
                         depends=(jquery, bootstrap))

myams_mini_bundle = Group(depends=(fontawesome_css, myams_css, myams_mini_js))

myams_mini_svg_bundle = Group(depends=(fontawesome_js, myams_css, myams_mini_js))

myams_core_js = Resource(library, 'js/dev/myams-core-dev.js',
                         minified='js/prod/myams-core.js',
                         depends=(jquery, jsrender, bootstrap))

myams_core_bundle = Group(depends=(fontawesome_css, myams_css, myams_core_js))

myams_core_svg_bundle = Group(depends=(fontawesome_js, myams_css, myams_core_js))


#
# Emerald skin
#

emerald_full_bundle = ResourceWithData(library, 'js/dev/emerald-dev.js',
                                       minified='js/prod/emerald.js')

emerald_css = Resource(library, 'css/dev/emerald.css',
                       minified='css/prod/emerald.css')

emerald_mini_bundle = Group(depends=(fontawesome_css, emerald_css, myams_mini_js))

emerald_mini_svg_bundle = Group(depends=(fontawesome_js, emerald_css, myams_mini_js))

emerald_core_bundle = Group(depends=(fontawesome_css, emerald_css, myams_core_js))

emerald_core_svg_bundle = Group(depends=(fontawesome_js, emerald_css, myams_core_js))


#
# Darkmode skin
#

darkmode_full_bundle = ResourceWithData(library, 'js/dev/darkmode-dev.js',
                                        minified='js/prod/darkmode.js')

darkmode_css = Resource(library, 'css/dev/darkmode.css',
                        minified='css/prod/darkmode.css')

darkmode_mini_bundle = Group(depends=(fontawesome_css, darkmode_css, myams_mini_js))

darkmode_mini_svg_bundle = Group(depends=(fontawesome_js, darkmode_css, myams_mini_js))

darkmode_core_bundle = Group(depends=(fontawesome_css, darkmode_css, myams_core_js))

darkmode_core_svg_bundle = Group(depends=(fontawesome_js, darkmode_css, myams_core_js))


#
# Lightmode skin
#

lightmode_full_bundle = ResourceWithData(library, 'js/dev/lightmode-dev.js',
                                         minified='js/prod/lightmode.js')

lightmode_css = Resource(library, 'css/dev/lightmode.css',
                         minified='css/prod/lightmode.css')

lightmode_mini_bundle = Group(depends=(fontawesome_css, lightmode_css, myams_mini_js))

lightmode_mini_svg_bundle = Group(depends=(fontawesome_js, lightmode_css, myams_mini_js))

lightmode_core_bundle = Group(depends=(fontawesome_css, lightmode_css, myams_core_js))

lightmode_core_svg_bundle = Group(depends=(fontawesome_js, lightmode_css, myams_core_js))
