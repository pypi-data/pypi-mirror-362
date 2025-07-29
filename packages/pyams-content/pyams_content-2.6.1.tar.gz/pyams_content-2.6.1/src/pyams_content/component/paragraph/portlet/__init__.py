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

"""PyAMS_*** module

"""

__docformat__ = 'restructuredtext'

from zope.schema.fieldproperty import FieldProperty

from pyams_content.component.paragraph import IBaseParagraph, IParagraphContainer, \
    IParagraphContainerTarget
from pyams_content.component.paragraph.portlet.interfaces import \
    IParagraphContainerPortletSettings, IParagraphNavigationPortletSettings
from pyams_portal.portlet import Portlet, PortletSettings, portlet_config
from pyams_security.interfaces.base import VIEW_PERMISSION
from pyams_sequence.reference import InternalReferenceMixin
from pyams_utils.factory import factory_config, get_object_factory
from pyams_utils.interfaces import MISSING_INFO
from pyams_utils.request import check_request
from pyams_utils.traversing import get_parent
from pyams_zmi.utils import get_object_label

from pyams_content import _


class ParagraphPortletSettingsMixin:
    """Paragraph container portlet settings mixin class"""

    def get_paragraphs_labels(self):
        """Paragraphs labels getter"""
        if not self.paragraphs:
            yield MISSING_INFO
        else:
            target = get_parent(self, IParagraphContainerTarget)
            if target is not None:
                container = IParagraphContainer(target)
                request = check_request()
                for name in self.paragraphs:
                    paragraph = container.get(name)
                    if name is not None:
                        yield get_object_label(paragraph, request)

    def get_paragraph_types_labels(self):
        """Paragraphs types labels getter"""
        if not self.factories:
            yield MISSING_INFO
        else:
            request = check_request()
            for factory_name in self.factories:
                factory = get_object_factory(IBaseParagraph, name=factory_name)
                if factory is not None:
                    yield request.localizer.translate(factory.factory.factory_name)


#
# Paragraph container portlet
#

PARAGRAPH_CONTAINER_PORTLET_NAME = 'pyams_content.portlet.paragraphs'


@factory_config(IParagraphContainerPortletSettings)
class ParagraphContainerPortletSettings(ParagraphPortletSettingsMixin, InternalReferenceMixin,
                                        PortletSettings):
    """Paragraph container portlet settings"""

    title = FieldProperty(IParagraphContainerPortletSettings['title'])
    button_label = FieldProperty(IParagraphContainerPortletSettings['button_label'])
    paragraphs = FieldProperty(IParagraphContainerPortletSettings['paragraphs'])
    factories = FieldProperty(IParagraphContainerPortletSettings['factories'])
    excluded_factories = FieldProperty(IParagraphContainerPortletSettings['excluded_factories'])
    anchors_only = FieldProperty(IParagraphContainerPortletSettings['anchors_only'])
    exclude_anchors = FieldProperty(IParagraphContainerPortletSettings['exclude_anchors'])
    display_navigation_links = FieldProperty(
        IParagraphContainerPortletSettings['display_navigation_links'])
    limit = FieldProperty(IParagraphContainerPortletSettings['limit'])


@portlet_config(permission=None)
class ParagraphContainerPortlet(Portlet):
    """Paragraphs container portlet"""

    name = PARAGRAPH_CONTAINER_PORTLET_NAME
    label = _("Content paragraphs")

    settings_factory = IParagraphContainerPortletSettings
    toolbar_css_class = 'fas fa-paragraph'


#
# Paragraph navigation portlet
#

PARAGRAPH_NAVIGATION_PORTLET_NAME = 'pyams_content.portlet.paragraphs.navigation'


@factory_config(IParagraphNavigationPortletSettings)
class ParagraphNavigationPortletSettings(ParagraphPortletSettingsMixin, PortletSettings):
    """Paragraph navigation portlet settings"""

    paragraphs = FieldProperty(IParagraphNavigationPortletSettings['paragraphs'])
    factories = FieldProperty(IParagraphNavigationPortletSettings['factories'])
    excluded_factories = FieldProperty(IParagraphNavigationPortletSettings['excluded_factories'])
    anchors_only = FieldProperty(IParagraphNavigationPortletSettings['anchors_only'])


@portlet_config(permission=None)
class ParagraphNavigationPortlet(Portlet):
    """Paragraphs navigation portlet"""

    name = PARAGRAPH_NAVIGATION_PORTLET_NAME
    label = _("Paragraphs navigation anchors")

    settings_factory = IParagraphNavigationPortletSettings
    toolbar_css_class = 'fas fa-angle-double-down'
