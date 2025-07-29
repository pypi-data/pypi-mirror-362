#
# Copyright (c) 2015-2023 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_*** module

"""

from persistent import Persistent
from pyramid_mailer.interfaces import IMailer
from zope.container.contained import Contained
from zope.schema.fieldproperty import FieldProperty

from pyams_app_msc.feature.messaging.interfaces import IMessagingSettings, MESSAGING_SETTINGS_KEY
from pyams_site.interfaces import ISiteRoot
from pyams_utils.adapter import adapter_config, get_annotation_adapter
from pyams_utils.factory import factory_config

__docformat__ = 'restructuredtext'

from pyams_utils.registry import query_utility


@factory_config(IMessagingSettings)
class MessagingSettings(Persistent, Contained):
    """Messaging settings persistent class"""

    mailer_name = FieldProperty(IMessagingSettings['mailer_name'])
    source_name = FieldProperty(IMessagingSettings['source_name'])
    source_address = FieldProperty(IMessagingSettings['source_address'])
    subject_prefix = FieldProperty(IMessagingSettings['subject_prefix'])

    def get_mailer(self):
        """Mailer utility getter"""
        return query_utility(IMailer, name=self.mailer_name)


@adapter_config(required=ISiteRoot,
                provides=IMessagingSettings)
def messaging_settings(context):
    """Messaging settings adapter"""
    return get_annotation_adapter(context, MESSAGING_SETTINGS_KEY, IMessagingSettings)
