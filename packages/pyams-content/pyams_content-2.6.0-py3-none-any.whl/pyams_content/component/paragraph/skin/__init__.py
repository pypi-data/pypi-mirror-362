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

"""PyAMS_content.component.paragraph.skin module

This module defines generic components used to handle paragraphs renderers settings.
"""

from zope.traversing.interfaces import ITraversable

from pyams_content.component.paragraph import IBaseParagraph
from pyams_content.feature.renderer import IRendererSettings
from pyams_utils.adapter import ContextAdapter, adapter_config
from pyams_workflow.content import HiddenContentPublicationInfo
from pyams_workflow.interfaces import IWorkflowPublicationInfo


__docformat__ = 'restructuredtext'


@adapter_config(name='renderer',
                required=IBaseParagraph,
                provides=ITraversable)
class ParagraphRendererSettingsTraverser(ContextAdapter):
    """Paragraph renderer settings traverser"""

    def traverse(self, name, furtherpath=None):
        """Traverse paragraph to renderer settings"""
        return IRendererSettings(self.context)


@adapter_config(required=IBaseParagraph,
                provides=IWorkflowPublicationInfo)
def base_paragraph_publication_info(context):
    """Base paragraph publication info"""
    if not context.visible:
        return HiddenContentPublicationInfo()
    return None
