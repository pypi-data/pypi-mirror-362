#
# Copyright (c) 2015-2022 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_content.component.gallery.zmi.paragraph module

This module defines management interface components which are used to handle
galleries paragraphs.
"""

from pyams_content.component.gallery import IBaseGallery, IGallery, IGalleryTarget
from pyams_content.component.gallery.interfaces import GALLERY_PARAGRAPH_ICON_CLASS, \
    GALLERY_PARAGRAPH_NAME, GALLERY_PARAGRAPH_TYPE, IGalleryParagraph
from pyams_content.component.paragraph import IParagraphContainer, IParagraphContainerTarget
from pyams_content.component.paragraph.zmi import BaseParagraphAddForm, BaseParagraphAddMenu, \
    IParagraphContainerBaseTable, IParagraphContainerFullTable
from pyams_content.component.paragraph.zmi.container import ParagraphTitleToolbarItemMixin
from pyams_content.component.paragraph.zmi.interfaces import IParagraphTitleToolbar
from pyams_zmi.interfaces.form import IPropertiesEditForm
from pyams_form.ajax import ajax_form_config
from pyams_form.field import Fields
from pyams_form.interfaces.form import IFormFields
from pyams_layer.interfaces import IPyAMSLayer
from pyams_portal.zmi.widget import RendererSelectFieldWidget
from pyams_utils.adapter import adapter_config
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.viewlet import IContextAddingsViewletManager


__docformat__ = 'restructuredtext'


@viewlet_config(name='gallery',
                context=IGalleryTarget, layer=IAdminLayer,
                view=IParagraphContainerFullTable, manager=IParagraphTitleToolbar,
                weight=15)
@viewlet_config(name='gallery',
                context=IGalleryParagraph, layer=IAdminLayer,
                view=IParagraphContainerFullTable, manager=IParagraphTitleToolbar,
                weight=15)
class GalleryParagraphTitleToolbarViewlet(ParagraphTitleToolbarItemMixin):
    """Gallery paragraph marker toolbar viewlet"""

    icon_class = GALLERY_PARAGRAPH_ICON_CLASS
    icon_hint = GALLERY_PARAGRAPH_NAME

    target_intf = IBaseGallery

    def update(self):
        gallery = self.target_intf(self.context, None)
        if gallery is not None:
            self.counter = len(gallery.values())


@viewlet_config(name='add-gallery-paragraph.menu',
                context=IParagraphContainerTarget, layer=IAdminLayer,
                view=IParagraphContainerBaseTable,
                manager=IContextAddingsViewletManager, weight=65)
class GalleryParagraphAddMenu(BaseParagraphAddMenu):
    """Gallery paragraph add menu"""

    label = GALLERY_PARAGRAPH_NAME
    icon_class = GALLERY_PARAGRAPH_ICON_CLASS

    factory_name = GALLERY_PARAGRAPH_TYPE
    href = 'add-gallery-paragraph.html'


@ajax_form_config(name='add-gallery-paragraph.html',
                  context=IParagraphContainer, layer=IPyAMSLayer)
class GalleryParagraphAddForm(BaseParagraphAddForm):
    """Gallery paragraph add form"""

    content_factory = IGalleryParagraph


@adapter_config(required=(IParagraphContainer, IAdminLayer, GalleryParagraphAddForm),
                provides=IFormFields)
@adapter_config(required=(IGalleryParagraph, IAdminLayer, IPropertiesEditForm),
                provides=IFormFields)
def gallery_form_fields(context, request, form):
    """Gallery form fields"""
    fields = Fields(IGalleryParagraph).select('title', 'renderer')
    if IGalleryParagraph.providedBy(context):
        fields['renderer'].widget_factory = RendererSelectFieldWidget
    return fields
