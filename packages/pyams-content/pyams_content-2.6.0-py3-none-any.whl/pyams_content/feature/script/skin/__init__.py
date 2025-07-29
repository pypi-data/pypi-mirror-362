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

from zope.interface import Interface

from pyams_content.feature.script import IScriptContainer
from pyams_content.feature.script.interfaces import IScriptContainerSettings
from pyams_layer.interfaces import IPyAMSUserLayer
from pyams_viewlet.viewlet import ViewContentProvider, contentprovider_config

__docformat__ = 'restructuredtext'


@contentprovider_config(name='pyams.top_scripts',
                        layer=IPyAMSUserLayer, view=Interface)
class TopScriptsContentProvider(ViewContentProvider):
    """Top scripts content provider"""

    def render(self, template_name=''):
        container = IScriptContainer(self.request.root, None)
        if container is None:
            return ''
        settings = IScriptContainerSettings(self.request.root)
        return '\n'.join((
            script.body.format(**settings.items)
            for script in container.get_top_scripts()
        ))


@contentprovider_config(name='pyams.bottom_scripts',
                        layer=IPyAMSUserLayer, view=Interface)
class BottomScriptsContentProvider(ViewContentProvider):
    """Bottom scripts content provider"""

    def render(self, template_name=''):
        container = IScriptContainer(self.request.root, None)
        if container is None:
            return ''
        settings = IScriptContainerSettings(self.request.root)
        return '\n'.join((
            script.body.format(**settings.items)
            for script in container.get_bottom_scripts()
        ))
