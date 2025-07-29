#
# Copyright (c) 2015-2024 Thierry Florac <tflorac AT ulthar.net>
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

from zope.contentprovider.interfaces import IContentProvider
from zope.interface import Interface

from pyams_content.shared.common.interfaces.types import IWfTypedSharedContent
from pyams_i18n.interfaces import II18n
from pyams_layer.interfaces import IPyAMSLayer
from pyams_template.template import template_config
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config
from pyams_utils.interfaces.tales import ITALESExtension
from pyams_viewlet.viewlet import ViewContentProvider, contentprovider_config

__docformat__ = 'restructuredtext'


@contentprovider_config(name='pyams_content.card.datatype',
                        layer=IPyAMSLayer, view=Interface)
@template_config(template='templates/card-datatype.pt', layer=IPyAMSLayer)
class SharedContentDatatypeProvider(ViewContentProvider):
    """Shared content datatype content provider"""

    label = None

    def update(self):
        super().update()
        tsc = IWfTypedSharedContent(self.context, None)
        if tsc is not None:
            datatype = tsc.get_data_type()
            if (datatype is not None) and datatype.display_as_tag:
                self.label = II18n(datatype).query_attributes_in_order(('navigation_label', 'label'),
                                                                       request=self.request)


@adapter_config(name='pyams_card_datatype',
                required=(Interface, Interface, Interface),
                provides=ITALESExtension)
class DataTypeContentProvider(ContextRequestViewAdapter):
    """Datatype content provider"""

    def render(self, context=None):
        if context is None:
            context = self.context
        provider = self.request.registry.queryMultiAdapter((context, self.request, self.view),
                                                           IContentProvider,
                                                           name='pyams_content.card.datatype')
        if provider is None:
            return ''
        provider.update()
        return provider.render()
