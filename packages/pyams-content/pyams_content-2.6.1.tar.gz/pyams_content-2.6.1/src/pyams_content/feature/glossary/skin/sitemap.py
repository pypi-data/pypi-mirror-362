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

"""PyAMS_content.feature.glossary.skin.sitemap module

This module defines adapters and views which are used to provide
glossary sitemap.
"""

from pyramid.view import view_config

from pyams_content.component.thesaurus import ITagsManager
from pyams_content.feature.sitemap.interfaces import ISitemapExtension
from pyams_layer.interfaces import IPyAMSUserLayer
from pyams_site.interfaces import ISiteRoot
from pyams_thesaurus.interfaces.thesaurus import IThesaurus
from pyams_utils.adapter import ContextRequestAdapter, adapter_config


__docformat__ = 'restructuredtext'


@adapter_config(name='glossary',
                required=(ISiteRoot, IPyAMSUserLayer),
                provides=ISitemapExtension)
class GlossarySitemapExtension(ContextRequestAdapter):
    """Glossary sitemap extension adapter"""

    @property
    def source(self):
        """Glossary sitemap source"""
        return ITagsManager(self.request.root).glossary


@view_config(name='sitemap.xml',
             context=IThesaurus, request_type=IPyAMSUserLayer,
             renderer='templates/glossary-sitemap.pt')
class GlossarySitemapView:
    """Glossary sitemap view"""

    def __init__(self, request):
        self.request = request

    def __call__(self):
        self.request.response.content_type = 'text/xml'
        return {}
