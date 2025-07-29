=====================
PyAMS content package
=====================

.. contents::


What is PyAMS?
==============

PyAMS (Pyramid Application Management Suite) is a small suite of packages written for applications
and content management with the Pyramid framework.

**PyAMS** is actually mainly used to manage websites through content management applications (CMS,
see PyAMS_content package), but many features are generic and can be used inside any kind of web
application.

All PyAMS documentation is available on `ReadTheDocs <https://pyams.readthedocs.io>`_; source code
is available on `Gitlab <https://gitlab.com/pyams>`_ and pushed to `Github
<https://github.com/py-ams>`_. Doctests are available in the *doctests* source folder.


What is PyAMS content?
======================

PyAMS_content is the main "content management" package. It provides sites, blogs and content
types which allows you to manage a whole website. It relies on several packages like
PyAMS_workflow for workflow management, PyAMS_portal to handle presentation templates, or
PyAMS_elastic to handle Elasticsearch integration.

Please note that PyAMS_content only provide a basic Bootstrap based skin, so you will have to
include other extension packages (like PyAMS_content_themes) to get more advanced graphical themes.
