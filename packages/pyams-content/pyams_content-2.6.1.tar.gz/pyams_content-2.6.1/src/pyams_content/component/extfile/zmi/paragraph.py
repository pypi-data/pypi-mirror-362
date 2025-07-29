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

"""PyAMS_content.component.extfile.zmi.paragraph module

This module defines components which are used to handle paragraphs
which are also associations containers.
"""

from pyams_content.component.association import IAssociationContainer, IAssociationContainerTarget
from pyams_content.component.extfile import EXTAUDIO_ICON_CLASS, EXTFILE_ICON_CLASS, \
    EXTIMAGE_ICON_CLASS, EXTVIDEO_ICON_CLASS, IExtAudio, IExtFile, IExtImage, IExtVideo
from pyams_content.component.paragraph.zmi.container import ParagraphTitleToolbarItemMixin
from pyams_content.component.paragraph.zmi.interfaces import IParagraphContainerFullTable, \
    IParagraphTitleToolbar
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.interfaces import IAdminLayer


__docformat__ = 'restructuredtext'

from pyams_content import _


@viewlet_config(name='external-files',
                context=IAssociationContainerTarget, layer=IAdminLayer,
                view=IParagraphContainerFullTable, manager=IParagraphTitleToolbar,
                weight=50)
class ExternalFilesTitleToolbarViewlet(ParagraphTitleToolbarItemMixin):
    """External files title toolbar viewlet"""

    icon_class = EXTFILE_ICON_CLASS
    icon_hint = _("Internal files")

    target_intf = IAssociationContainer
    item_intf = IExtFile


@viewlet_config(name='external-images',
                context=IAssociationContainerTarget, layer=IAdminLayer,
                view=IParagraphContainerFullTable, manager=IParagraphTitleToolbar,
                weight=60)
class ExternalImagesTitleToolbarViewlet(ParagraphTitleToolbarItemMixin):
    """External images title toolbar viewlet"""

    icon_class = EXTIMAGE_ICON_CLASS
    icon_hint = _("Internal images")

    target_intf = IAssociationContainer
    item_intf = IExtImage


@viewlet_config(name='external-videos',
                context=IAssociationContainerTarget, layer=IAdminLayer,
                view=IParagraphContainerFullTable, manager=IParagraphTitleToolbar,
                weight=70)
class ExternalVideosTitleToolbarViewlet(ParagraphTitleToolbarItemMixin):
    """External files title toolbar viewlet"""

    icon_class = EXTVIDEO_ICON_CLASS
    icon_hint = _("Internal videos")

    target_intf = IAssociationContainer
    item_intf = IExtVideo


@viewlet_config(name='external-audios',
                context=IAssociationContainerTarget, layer=IAdminLayer,
                view=IParagraphContainerFullTable, manager=IParagraphTitleToolbar,
                weight=80)
class ExternalAudiosTitleToolbarViewlet(ParagraphTitleToolbarItemMixin):
    """External audio files title toolbar viewlet"""

    icon_class = EXTAUDIO_ICON_CLASS
    icon_hint = _("Internal audio files")

    target_intf = IAssociationContainer
    item_intf = IExtAudio
