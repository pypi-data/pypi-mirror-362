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

"""PyAMS_content.shared.form.skin module

Form help viewlet.
"""

__docformat__ = 'restructuredtext'

from pyams_content.shared.form import IWfForm
from pyams_content.skin.interfaces import IContentTitle
from pyams_fields.skin import IFormFieldContainerInputForm
from pyams_i18n.interfaces import II18n
from pyams_layer.interfaces import IPyAMSUserLayer
from pyams_skin.interfaces.viewlet import IFormHeaderViewletManager
from pyams_skin.viewlet.help import AlertMessage
from pyams_utils.adapter import adapter_config
from pyams_viewlet.viewlet import viewlet_config


@adapter_config(required=(IWfForm, IPyAMSUserLayer),
                provides=IContentTitle)
def form_title(context, request):
    """Custom form title getter"""
    i18n = II18n(context)
    return i18n.query_attribute('alt_title', request=request) or \
        i18n.query_attribute('title', request=request)


@viewlet_config(name='form-header.help',
                context=IWfForm, layer=IPyAMSUserLayer, view=IFormFieldContainerInputForm,
                manager=IFormHeaderViewletManager, weight=10)
class FormInputHelpMessage(AlertMessage):
    """Form input form help"""

    def __new__(cls, context, request, view, manager):
        header = II18n(context).query_attribute('form_header', request=request)
        if not header:
            return None
        return AlertMessage.__new__(cls)

    @property
    def message(self):
        """Message getter"""
        return II18n(self.context).query_attribute('form_header', request=self.request)

    message_renderer = 'raw'
