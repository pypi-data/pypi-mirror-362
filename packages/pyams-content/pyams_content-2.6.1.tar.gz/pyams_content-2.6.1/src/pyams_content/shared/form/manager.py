#
# Copyright (c) 2015-2021 Thierry Florac <tflorac AT ulthar.net>
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

from pyramid.events import subscriber
from zope.component.interfaces import ISite
from zope.interface import implementer
from zope.lifecycleevent.interfaces import IObjectAddedEvent

from pyams_content.component.paragraph.interfaces import IParagraphFactorySettingsTarget
from pyams_content.component.thesaurus.interfaces import IThemesManagerTarget
from pyams_content.reference.pictogram.interfaces import IPictogramManagerTarget
from pyams_content.shared.common.manager import SharedTool
from pyams_content.shared.common.types import TypedSharedToolMixin
from pyams_content.shared.form.interfaces import FORM_CONTENT_TYPE
from pyams_content.shared.form.interfaces import IFormManager
from pyams_fields.interfaces import ICaptchaManagerTarget
from pyams_utils.factory import factory_config
from pyams_utils.traversing import get_parent


@factory_config(IFormManager)
@implementer(ICaptchaManagerTarget, IParagraphFactorySettingsTarget, IThemesManagerTarget,
             IPictogramManagerTarget)
class FormManager(SharedTool, TypedSharedToolMixin):
    """Form manager class"""

    shared_content_type = FORM_CONTENT_TYPE
    shared_content_menu = False


@subscriber(IObjectAddedEvent, context_selector=IFormManager)
def handle_added_form_manager(event):
    """Register form manager when added"""
    site = get_parent(event.newParent, ISite)
    registry = site.getSiteManager()
    if registry is not None:
        registry.registerUtility(event.object, IFormManager)
