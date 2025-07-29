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

"""PyAMS_content.root.skin.metas module

This module defines site root metas headers.
"""

from zope.interface import Interface

from pyams_content.component.illustration import IIllustration
from pyams_content.root import ISiteRootInfos
from pyams_file.interfaces.thumbnail import IThumbnails
from pyams_i18n.interfaces import II18n, II18nManager, INegotiator
from pyams_layer.interfaces import IPyAMSUserLayer
from pyams_site.interfaces import ISiteRoot
from pyams_skin.interfaces.metas import IHTMLContentMetas
from pyams_skin.metas import ContentMeta, HTMLTagMeta, PropertyMeta, SchemaMeta
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config
from pyams_utils.registry import get_utility
from pyams_utils.url import absolute_url, canonical_url

__docformat__ = 'restructuredtext'


@adapter_config(name='title',
                required=(ISiteRoot, IPyAMSUserLayer, Interface),
                provides=IHTMLContentMetas)
class SiteRootTitleMetasAdapter(ContextRequestViewAdapter):
    """Site root title metas adapter"""

    order = 1

    def get_metas(self):
        site_infos = ISiteRootInfos(self.context)
        i18n = II18n(site_infos)
        title = i18n.query_attribute('title', request=self.request)
        if title:
            yield HTMLTagMeta('title', title)
        description = i18n.query_attribute('description', request=self.request)
        if description:
            yield ContentMeta('description', description)


@adapter_config(name='opengraph',
                required=(ISiteRoot, IPyAMSUserLayer, Interface),
                provides=IHTMLContentMetas)
class SiteRootOpengraphMetasAdapter(ContextRequestViewAdapter):
    """Site root opengraph metas adapter"""

    weight = 15

    def get_metas(self):
        context = self.context
        request = self.request
        negotiator = get_utility(INegotiator)
        lang = negotiator.server_language

        # main properties
        yield PropertyMeta('og:type', 'website')

        site_infos = ISiteRootInfos(context)
        i18n = II18n(site_infos)
        title = i18n.query_attribute('title', lang=lang, request=request)
        yield PropertyMeta('og:title', title)
        description = i18n.query_attribute('description', lang=lang, request=request)
        if description:
            yield PropertyMeta('og:description', description)

        # URL and site name
        yield PropertyMeta('og:url', canonical_url(context, request))
        yield PropertyMeta('og:site_name', title)


        # illustration properties
        illustration = None
        card = None
        card_url = None
        alt = None
        illustration = IIllustration(context, None)
        if illustration is not None:
            data = II18n(illustration).query_attribute('data', lang=lang, request=request)
            if data:
                card = IThumbnails(data).get_thumbnail('card:w800')
                card_url = absolute_url(data, request, '++thumb++card:w800')
                yield PropertyMeta('og:image', card_url)
                if request.scheme == 'https':
                    yield PropertyMeta('og:image:secure_url', card_url)
                else:
                    yield PropertyMeta('og:image:url', card_url)
                yield PropertyMeta('og:image:type', card.content_type)
                image_size = card.image_size
                yield PropertyMeta('og:image:width', image_size[0])
                yield PropertyMeta('og:image:height', image_size[1])
                alt = II18n(illustration).query_attribute('alt_title', lang=lang, request=request)
                if alt:
                    yield PropertyMeta('og:image:alt', alt)

        # locales properties
        yield PropertyMeta('og:locale', lang)
        manager = II18nManager(context, None)
        if manager is not None:
            for other_lang in manager.languages or ():
                if other_lang != lang:
                    yield PropertyMeta('og:locale:alternate', other_lang)

        yield ContentMeta('twitter:title', title)
        if description:
            yield ContentMeta('twitter:description', description)
        if card is not None:
            yield ContentMeta('twitter:card', 'summary_large_image')
            yield ContentMeta('twitter:image', card_url)
            if alt:
                yield ContentMeta('twitter:image:alt', alt)
        else:
            yield ContentMeta('twitter:card', 'summary')

        # Schema.org properties
        yield SchemaMeta('name', title)
        if description:
            yield SchemaMeta('description', description)
        if card is not None:
            yield SchemaMeta('image', card_url)
