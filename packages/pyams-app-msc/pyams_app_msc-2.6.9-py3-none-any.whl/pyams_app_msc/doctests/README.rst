=============================
PyAMS MSC application package
=============================

Introduction
------------

This package is composed of a set of utility functions, usable into any Pyramid application.

    >>> from pyramid.testing import setUp, tearDown
    >>> config = setUp(hook_zca=True)

    >>> from cornice import includeme as include_cornice
    >>> include_cornice(config)
    >>> from cornice_swagger import includeme as include_swagger
    >>> include_swagger(config)
    >>> from pyams_utils import includeme as include_utils
    >>> include_utils(config)
    >>> from pyams_security import includeme as include_security
    >>> include_security(config)
    >>> from pyams_form import includeme as include_form
    >>> include_form(config)
    >>> from pyams_table import includeme as include_table
    >>> include_table(config)
    >>> from pyams_portal import includeme as include_portal
    >>> include_portal(config)
    >>> from pyams_content import includeme as include_content
    >>> include_content(config)
    >>> from pyams_content_es import includeme as include_content_es
    >>> include_content_es(config)
    >>> from pyams_content_api import includeme as include_content_api
    >>> include_content_api(config)
    >>> from pyams_content_themes import includeme as include_content_themes
    >>> include_content_themes(config)

    >>> from pyams_app_msc import includeme as include_app
    >>> include_app(config)


    >>> tearDown()
