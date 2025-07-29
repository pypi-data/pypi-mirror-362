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

"""PyAMS_content.component.fields.handler.mail module

This module defines a custom form handler used to send emails.
"""

from persistent import Persistent
from zope.container.contained import Contained
from zope.schema.fieldproperty import FieldProperty

from pyams_content.component.fields.handler.interfaces import IMailtoHandlerInfo, IMailtoHandlerTarget, \
    MAILTO_HANDLER_ANNOTATION_KEY
from pyams_fields.interfaces import IFormFieldContainer, IFormHandler, IFormHandlerInfo, IFormHandlersInfo
from pyams_i18n.interfaces import II18n
from pyams_mail.message import HTMLMessage
from pyams_security.interfaces import ISecurityManager
from pyams_security.interfaces.notification import INotificationSettings
from pyams_utils.adapter import adapter_config, get_annotation_adapter
from pyams_utils.factory import factory_config
from pyams_utils.interfaces import MISSING_INFO
from pyams_utils.list import boolean_iter
from pyams_utils.registry import get_utility, utility_config
from pyams_utils.request import query_request


__docformat__ = 'restructuredtext'

from pyams_content import _


@factory_config(IMailtoHandlerInfo)
class MailtoHandlerInfo(Persistent, Contained):
    """Mailto handler persistent class"""

    service_name = FieldProperty(IMailtoHandlerInfo['service_name'])
    source_name = FieldProperty(IMailtoHandlerInfo['source_name'])
    source_address = FieldProperty(IMailtoHandlerInfo['source_address'])
    target_name = FieldProperty(IMailtoHandlerInfo['target_name'])
    target_address = FieldProperty(IMailtoHandlerInfo['target_address'])
    notification_message = FieldProperty(IMailtoHandlerInfo['notification_message'])
    confirm_message = FieldProperty(IMailtoHandlerInfo['confirm_message'])


@adapter_config(required=IMailtoHandlerTarget,
                provides=IMailtoHandlerInfo)
@adapter_config(name='mailto',
                required=IMailtoHandlerTarget,
                provides=IFormHandlerInfo)
def mailto_handler_info(context):
    """Mailto form handler info"""
    return get_annotation_adapter(context, MAILTO_HANDLER_ANNOTATION_KEY,
                                  IMailtoHandlerInfo,
                                  name='++handler++mailto')


@utility_config(name='mailto',
                provides=IFormHandler)
class SimpleMailtoFormHandler:
    """Simple mail form handler"""

    label = _("Simple mail handler")
    weight = 10

    target_interface = IMailtoHandlerTarget

    @staticmethod
    def build_message(template, data):
        """Message builder"""
        if template:
            return template.format(**data)
        return '<br />'.join((
            f"{k}: {v or MISSING_INFO}"
            for k, v in data.items()
        ))

    def handle(self, form, data, user_data):
        """Form data handler"""
        sm = get_utility(ISecurityManager)
        settings = INotificationSettings(sm)
        if not settings.enable_notifications:
            return
        mailer = settings.get_mailer()
        request = query_request()
        handlers = IFormHandlersInfo(form, None)
        if handlers is None:
            return
        handler_info = IMailtoHandlerInfo(handlers, None)
        if handler_info is None:
            return
        i18n_handler = II18n(handler_info)
        service_name = i18n_handler.query_attribute('service_name', request=request)
        if handler_info.target_address:
            body = self.build_message(
                i18n_handler.query_attribute('notification_message', request=request),
                user_data)
            target = f'{handler_info.target_name} <{handler_info.target_address}>' \
                if handler_info.target_name else handler_info.target_address
            message = HTMLMessage(
                subject=f'[{settings.subject_prefix}] {service_name}',
                from_addr=f'{handler_info.source_name} <{handler_info.source_address}>',
                to_addr=target,
                html=body)
            mailer.send(message)
        fields = IFormFieldContainer(form, None)
        if fields is None:
            return
        has_email, email_field = boolean_iter(fields.find_fields('mail'))
        if not has_email:
            return
        email_address = data.get(next(email_field).name)
        confirm_message = i18n_handler.query_attribute('confirm_message', request=request)
        if not (email_address and confirm_message):
            return
        message = HTMLMessage(
            subject=f'[{settings.subject_prefix}] {service_name}',
            from_addr=f'{handler_info.source_name} <{handler_info.source_address}>',
            to_addr=email_address,
            html=confirm_message.format(**user_data))
        mailer.send(message)
