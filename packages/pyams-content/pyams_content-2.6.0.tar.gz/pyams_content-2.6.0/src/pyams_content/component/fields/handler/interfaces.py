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

"""PyAMS_content.component.fields.handler.interfaces module

This module defines custom form handlers interfaces.
"""

from zope.interface import Interface
from zope.schema import TextLine

from pyams_fields.interfaces import IFormHandlerInfo
from pyams_i18n.schema import I18nHTMLField, I18nTextLineField
from pyams_utils.schema import MailAddressField


__docformat__ = 'restructuredtext'

from pyams_content import _


MAILTO_HANDLER_ANNOTATION_KEY = 'pyams_content.handler::mailto'


class IMailtoHandlerInfo(IFormHandlerInfo):
    """Simple mailto handler info interface"""

    service_name = I18nTextLineField(title=_("Service name"),
                                     description=_("This name will be used as subject in all email "
                                                   "messages sent by this contact form"),
                                     required=False)

    source_name = TextLine(title=_("Source name"),
                           description=_("Name of mail data sender"),
                           required=False)

    source_address = MailAddressField(title=_("Source address"),
                                      description=_("Mail address from which form data is sent"),
                                      required=True)

    target_name = TextLine(title=_("Recipient name"),
                           description=_("Name of data recipient"),
                           required=False)

    target_address = MailAddressField(title=_("Recipient address"),
                                      description=_("Mail address to which form data is sent"),
                                      required=True)

    notification_message = I18nHTMLField(title=_("Notification message"),
                                         description=_("This message will be sent to target address defined just "
                                                       "before; you can include form fields values by including "
                                                       "their name, enclosed in {brackets}, or {_reference} to get "
                                                       "the submission ID; if you don't provide any template, message "
                                                       "will be filled only with the raw data entered into this form"),
                                         required=False)

    confirm_message = I18nHTMLField(title=_("Confirmation message"),
                                    description=_("If an email address is provided in the form, this message will be "
                                                  "returned to the contact; you can include all form fields values by "
                                                  "including their name, enclosed in {brackets}, or {_reference} to "
                                                  "include submission ID"),
                                    required=False)


class IMailtoHandlerTarget(Interface):
    """Simple mailto handler target interface"""
