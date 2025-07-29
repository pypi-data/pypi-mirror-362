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

"""PyAMS_content.shared.common.skin.metas module

This module defines meta-headers which are common to all shared contents.
"""

from zope.dublincore.interfaces import IZopeDublinCore
from zope.interface import Interface

from pyams_content.component.illustration import IIllustration, IIllustrationTarget, ILinkIllustration
from pyams_content.component.thesaurus import ITagsInfo
from pyams_content.root import ISiteRootInfos
from pyams_content.shared.common import IWfSharedContent
from pyams_file.interfaces.thumbnail import IThumbnails
from pyams_i18n.interfaces import II18n, II18nManager, INegotiator
from pyams_layer.interfaces import IPyAMSUserLayer
from pyams_skin.interfaces.metas import IHTMLContentMetas
from pyams_skin.metas import ContentMeta, PropertyMeta, SchemaMeta
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config
from pyams_utils.registry import get_utility
from pyams_utils.timezone import tztime
from pyams_utils.traversing import get_parent
from pyams_utils.url import absolute_url, canonical_url
from pyams_workflow.interfaces import IWorkflowPublicationInfo

__docformat__ = 'restructuredtext'


@adapter_config(name='opengraph',
                required=(IWfSharedContent, IPyAMSUserLayer, Interface),
                provides=IHTMLContentMetas)
class SharedContentOpengraphMetasAdapter(ContextRequestViewAdapter):
    """Shared content opengraph metas adapter"""

    weight = 15

    def get_metas(self):
        context = self.context
        request = self.request
        i18n = II18n(context)
        negotiator = get_utility(INegotiator)
        lang = negotiator.server_language

        description = i18n.query_attribute('description', lang=lang, request=request) or \
            i18n.query_attribute('header', lang=lang, request=request)

        # main properties
        yield PropertyMeta('og:type', 'article')
        yield PropertyMeta('og:title',
                           i18n.query_attribute('title', lang=lang, request=request))
        if description:
            yield PropertyMeta('og:description', description)

        # URL and site name
        yield PropertyMeta('og:url', canonical_url(context, request))
        site_infos = ISiteRootInfos(request.root)
        yield PropertyMeta('og:site_name',
                           II18n(site_infos).query_attribute('title', lang=lang, request=request))

        # workflow information
        dc = IZopeDublinCore(context, None)
        if (dc is not None) and dc.modified:
            yield PropertyMeta('article:modified_time', tztime(dc.modified).isoformat())
        pub_info = IWorkflowPublicationInfo(context, None)
        if pub_info is not None:
            if pub_info.first_publication_date:
                yield PropertyMeta('article:published_time',
                                   tztime(pub_info.first_publication_date).isoformat())
            if pub_info.publication_expiration_date:
                yield PropertyMeta('article:expiration_time',
                                   tztime(pub_info.publication_expiration_date).isoformat())

        # tags
        tags = ITagsInfo(context, None)
        if tags is not None:
            for tag in tags.tags or ():
                yield PropertyMeta('article:tag', tag.label)

        # illustration properties
        illustration = None
        card = None
        card_url = None
        alt = None
        target = context
        while target is not None:
            illustration = ILinkIllustration(target, None)
            if (illustration is None) or (not illustration.has_data()):
                illustration = IIllustration(target, None)
            if (illustration is not None) and illustration.has_data():
                break
            target = get_parent(target, IIllustrationTarget, allow_context=False)
        if (target is not None) and (illustration is not None):
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

        yield ContentMeta('twitter:title',
                          i18n.query_attribute('title', lang=lang, request=request))
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
        yield SchemaMeta('name', i18n.query_attribute('title', lang=lang, request=request))
        if description:
            yield SchemaMeta('description', description)
        if card is not None:
            yield SchemaMeta('image', card_url)
