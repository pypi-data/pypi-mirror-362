================
MyAMS.js package
================

.. contents::


What is PyAMS?
==============

PyAMS (Pyramid Application Management Suite) is a small suite of packages written for applications
and content management with the Pyramid framework.

**PyAMS** is actually mainly used to manage web sites through content management applications (CMS,
see PyAMS_content package), but many features are generic and can be used inside any kind of web
application.

All PyAMS documentation is available on `ReadTheDocs <https://pyams.readthedocs.io>`_; source code
is available on `Gitlab <https://gitlab.com/pyams>`_ and pushed to `Github
<https://github.com/py-ams>`_.


What is MyAMS.js?
=================

MyAMS.js is a "small" extension package over JQuery and Bootstrap. It provides a small set of
features using the HTML "data" API to enable components configuration without using any
javascript code.

MyAMS documentation and demo site are available at http://myams.ztfy.org.


Integrating MyAMS.js
====================

You can include MyAMS resources manually as usual in your HTML pages.

A Python package is also provided, which is declaring MyAMS resources as Fanstatic resources,
for easy integration into any Pyramid application; you can also use *PyAMS_zmi* package, which
is relying on MyAMS.js.
