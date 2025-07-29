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

"""PyAMS_content.workflow.zmi.header module

This module defines workflow-related content headers.
"""

from datetime import datetime, timezone

from pyams_content.shared.site.interfaces import IBaseSiteItem
from pyams_sequence.interfaces import ISequentialIdTarget
from pyams_skin.interfaces.view import IModalPage
from pyams_skin.interfaces.viewlet import IHeaderViewletManager
from pyams_template.template import override_template
from pyams_utils.adapter import NullAdapter
from pyams_utils.date import format_datetime
from pyams_utils.timezone import tztime
from pyams_viewlet.viewlet import Viewlet, viewlet_config
from pyams_workflow.interfaces import IWorkflowPublicationInfo
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.zmi.viewlet.header import ContentHeaderViewlet

__docformat__ = 'restructuredtext'

from pyams_content import _


override_template(ContentHeaderViewlet,
                  template='templates/sequence-header.pt',
                  context=ISequentialIdTarget, layer=IAdminLayer)


@viewlet_config(name='workflow-status',
                context=IBaseSiteItem, layer=IAdminLayer,
                manager=IHeaderViewletManager, weight=20)
class WorkflowPublicationSupportHeaderViewlet(Viewlet):
    """Workflow publication support header viewlet"""

    def __new__(cls, context, request, view, manager):
        if IModalPage.providedBy(view):
            return None
        return Viewlet.__new__(cls)

    def render(self):
        """Status getter"""
        translate = self.request.localizer.translate
        now = tztime(datetime.now(timezone.utc))
        pub_info = IWorkflowPublicationInfo(self.context)
        if pub_info.publication_effective_date:
            if pub_info.publication_effective_date <= now:
                if pub_info.publication_expiration_date:
                    if pub_info.publication_effective_date > now:
                        state = _("Retired")
                        state_label = _("{state} since {from_date}")
                    else:
                        state = _("Published")
                        state_label = _("{state} since {from_date} until {to_date}")
                else:
                    state = _("Published")
                    state_label = _("{state} since {from_date}")
            else:
                if pub_info.publication_expiration_date:
                    state = _("To be published")
                    state_label = _("{state} from {from_date} to {to_date}")
                else:
                    state = _("Published")
                    state_label = _("{state} after {from_date}")
            state = translate(state_label).format(
                state='<span class="text-danger">{}</span>'.format(translate(state)),
                from_date=format_datetime(pub_info.publication_effective_date),
                to_date=format_datetime(pub_info.publication_expiration_date))
        else:
            state = '<span class="text-danger">{}</span>'.format(
                translate(_("Not published")))
        return '<div class="mb-1">{}</div>'.format(state)


@viewlet_config(name='workflow-status',
                context=IBaseSiteItem, layer=IAdminLayer, view=IModalPage,
                manager=IHeaderViewletManager, weight=20)
class WorkflowPublicationSupportModalHeaderViewlet(NullAdapter):
    """Workflow publication support modal header viewlet"""
