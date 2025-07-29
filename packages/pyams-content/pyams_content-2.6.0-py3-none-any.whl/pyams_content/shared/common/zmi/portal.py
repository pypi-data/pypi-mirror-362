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

"""PyAMS_content.shared.common.zmi.portal module

This modules defines custom components used for presentation templates management.
"""

from pyams_content.shared.common.interfaces import ISharedToolPortalContext, \
    IWfSharedContentPortalContext
from pyams_portal.zmi.presentation import PortalContextPresentationEditForm
from pyams_skin.interfaces.viewlet import IHelpViewletManager
from pyams_skin.viewlet.help import AlertMessage
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.interfaces import IAdminLayer


__docformat__ = 'restructuredtext'

from pyams_content import _


@viewlet_config(name='presentation-template.help',
                context=ISharedToolPortalContext, layer=IAdminLayer,
                view=PortalContextPresentationEditForm,
                manager=IHelpViewletManager, weight=10)
class SharedToolPortalContextPresentationEditFormHelp(AlertMessage):
    """Shared tool portal context presentation edit form help"""

    status = 'info'
    _message = _("You can select the default template which will be applied **by default** to "
                 "all contents inside this shared tool.<br />"
                 "If you select a shared template or choose to inherit from parent "
                 "configuration, you can adjust settings of each portlet but can't change "
                 "page configuration.<br />"
                 "If you choose to use a local template, it's configuration will only be "
                 "reusable in sub-levels which will choose to inherit from it.")

    message_renderer = 'markdown'


@viewlet_config(name='presentation-template.help',
                context=IWfSharedContentPortalContext, layer=IAdminLayer,
                view=PortalContextPresentationEditForm,
                manager=IHelpViewletManager, weight=10)
class SharedContextPortalContextPresentationEditFormHelp(AlertMessage):
    """Shared content portal context presentation edit form help"""

    status = 'info'
    _message = _("You can use the default template defined on the shared tool, which will "
                 "be applied to all contents.<br />"
                 "If you select another shared template or choose to inherit from this "
                 "configuration, you can adjust settings of each portlet but can't change "
                 "page configuration.<br />"
                 "If you choose to use a local template, it's configuration will not be "
                 "usable in other contents, except if you share it.")

    message_renderer = 'markdown'
