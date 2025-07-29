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

"""PyAMS MSC application package

PyAMS application for cinema reservation management
"""

__docformat__ = 'restructuredtext'

from pyramid.i18n import TranslationStringFactory


_ = TranslationStringFactory('pyams_app_msc')


def includeme(config):
    """pyams_app_msc features include"""
    from .include import include_package  # pylint: disable=import-outside-toplevel
    include_package(config)
