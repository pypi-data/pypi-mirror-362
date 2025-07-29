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

"""PyAMS_content.component.frame.portlet module

This module defines a framed text portlet.
"""

from zope.interface import alsoProvides
from zope.schema.fieldproperty import FieldProperty

from pyams_content.component.frame.portlet.interfaces import IFramePortletSettings
from pyams_content.component.illustration import IIllustration, IParagraphIllustration, \
    illustration_factory
from pyams_portal.portlet import Portlet, PortletSettings, portlet_config
from pyams_utils.adapter import adapter_config
from pyams_utils.factory import factory_config

__docformat__ = 'restructuredtext'

from pyams_content import _


FRAME_PORTLET_NAME = 'pyams_content.portlet.frame'


@factory_config(IFramePortletSettings)
class FramePortletSettings(PortletSettings):
    """Frame portlet settings"""

    title = FieldProperty(IFramePortletSettings['title'])
    body = FieldProperty(IFramePortletSettings['body'])


@adapter_config(required=IFramePortletSettings,
                provides=IIllustration)
def frame_portlet_settings_illustration(context):
    """Frame portlet settings illustration factory"""
    result = illustration_factory(context)
    if not IParagraphIllustration.providedBy(result):
        alsoProvides(result, IParagraphIllustration)
    return result


@portlet_config(permission=None)
class FramePortlet(Portlet):
    """Frame portlet"""

    name = FRAME_PORTLET_NAME
    label = _("Framed text")

    settings_factory = IFramePortletSettings
    toolbar_css_class = 'fas fa-window-maximize'
