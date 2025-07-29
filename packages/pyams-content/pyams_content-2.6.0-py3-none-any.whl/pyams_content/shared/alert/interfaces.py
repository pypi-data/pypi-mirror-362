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

"""PyAMS_content.shared.common.alert.interfaces module

This module defines interfaces of alerts tool and contents.
"""

from collections import OrderedDict
from enum import Enum

from zope.container.constraints import contains
from zope.container.interfaces import IContainer
from zope.interface import Invalid, invariant
from zope.location.interfaces import ILocation
from zope.schema import Bool, Choice, Int, TextLine, URI

from pyams_content.reference.pictogram import PICTOGRAM_VOCABULARY
from pyams_content.shared.common import ISharedContent, IWfSharedContent
from pyams_content.shared.common.interfaces import ISharedTool
from pyams_i18n.schema import I18nTextField, I18nTextLineField
from pyams_sequence.interfaces import IInternalReferencesList
from pyams_sequence.schema import InternalReferenceField, InternalReferencesListField
from pyams_utils.schema import ColorField

__docformat__ = 'restructuredtext'

from pyams_content import _

ALERT_TYPES_MANAGER_ANNOTATION_KEY = 'pyams_content.alerts.types'
ALERT_TYPES_VOCABULARY = 'pyams_content.alerts.types'


class IAlertType(ILocation):
    """Alert type interface"""

    visible = Bool(title=_("Visible?"),
                   description=_("An hidden alert type can't be assigned to new alerts"),
                   required=True,
                   default=True)

    label = I18nTextLineField(title=_("Label"),
                              required=True)

    dashboard_label = I18nTextLineField(title=_("Dashboards label"),
                                        description=_("Optional label used for dashboards presentation"),
                                        required=False)

    pictogram = Choice(title=_("Pictogram"),
                       description=_("Pictogram associated with this alert type"),
                       vocabulary=PICTOGRAM_VOCABULARY,
                       required=False)

    color = ColorField(title=_("Color"),
                       description=_("Base color associated with this alert type"),
                       required=False,
                       default='dc3545')


class IAlertTypesManager(IContainer):
    """Alert types manager interface"""

    contains(IAlertType)

    def get_visible_items(self):
        """Visible alert types iterator"""


ALERT_CONTENT_TYPE = 'alert'
ALERT_CONTENT_NAME = _("Alert")


class IWfAlert(IWfSharedContent, IInternalReferencesList):
    """Alert interface"""

    alert_type = Choice(title=_("Alert type"),
                        description=_("Alert type can affect renderer alert style"),
                        required=True,
                        vocabulary=ALERT_TYPES_VOCABULARY)

    def get_alert_type(self):
        """Alert type getter"""

    body = I18nTextField(title=_("Message content"),
                         description=_("Message body"),
                         required=False)

    reference = InternalReferenceField(title=_("Internal reference"),
                                       description=_("Internal link target reference. You can "
                                                     "search a reference using '+' followed by "
                                                     "internal number, or by entering text "
                                                     "matching content title"),
                                       required=False)

    external_url = URI(title=_("External URL"),
                       description=_("Alternate external URL"),
                       required=False)

    @invariant
    def check_url(self):
        if self.reference and self.external_url:
            raise Invalid(_("You can't set internal reference and external URI simultaneously!"))

    references = InternalReferencesListField(title=_("Concerned contents"),
                                             description=_("If any, these contents will "
                                                           "automatically display this alert"),
                                             required=False)

    maximum_interval = Int(title=_("Maximum interval"),
                           description=_("Maximum interval between alert displays on a given "
                                         "device, given in hours; set to 0 to always display "
                                         "the alert"),
                           required=True,
                           min=0,
                           default=48)


class IAlert(ISharedContent):
    """Workflow managed alert interface"""


class IAlertManager(ISharedTool):
    """Alert manager interface"""

    def find_context_alerts(self, context=None, request=None):
        """Find alerts associated with given context"""
