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
from zope.container.contained import Contained
from zope.schema.fieldproperty import FieldProperty

from pyams_app_msc.shared.theater import IMailTemplatesTarget
from pyams_app_msc.shared.theater.interfaces.mail import IMailTemplates, MAIL_TEMPLATES_KEY
from pyams_utils.adapter import adapter_config, get_annotation_adapter
from pyams_utils.factory import factory_config

__docformat__ = 'restructuredtext'


@factory_config(IMailTemplates)
class MailTemplates(Persistent, Contained):
    """Mail templates"""

    send_copy_to_sender = FieldProperty(IMailTemplates['send_copy_to_sender'])
    cancel_subject = FieldProperty(IMailTemplates['cancel_subject'])
    cancel_template = FieldProperty(IMailTemplates['cancel_template'])
    refuse_subject = FieldProperty(IMailTemplates['refuse_subject'])
    refuse_template = FieldProperty(IMailTemplates['refuse_template'])
    option_subject = FieldProperty(IMailTemplates['option_subject'])
    option_template = FieldProperty(IMailTemplates['option_template'])
    accept_subject = FieldProperty(IMailTemplates['accept_subject'])
    accept_template = FieldProperty(IMailTemplates['accept_template'])
    update_subject = FieldProperty(IMailTemplates['update_subject'])
    update_template = FieldProperty(IMailTemplates['update_template'])
    reminder_subject = FieldProperty(IMailTemplates['reminder_subject'])
    reminder_template = FieldProperty(IMailTemplates['reminder_template'])


@adapter_config(required=IMailTemplatesTarget,
                provides=IMailTemplates)
def mail_templates(context):
    """Mail templates adapter"""
    return get_annotation_adapter(context, MAIL_TEMPLATES_KEY, IMailTemplates)
