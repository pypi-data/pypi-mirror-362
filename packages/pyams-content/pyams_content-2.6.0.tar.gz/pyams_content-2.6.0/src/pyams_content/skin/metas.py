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

"""PyAMS_content.skin.metas module

This module defines common HTML metas headers.
"""

from zope.dublincore.interfaces import IZopeDublinCore
from zope.interface import Interface

from pyams_content.root import ISiteRootInfos
from pyams_i18n.interfaces import II18n
from pyams_layer.interfaces import IPyAMSUserLayer
from pyams_skin.interfaces.metas import IHTMLContentMetas
from pyams_skin.metas import BaseMeta, HTMLTagMeta, LinkMeta
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config
from pyams_utils.timezone import tztime
from pyams_utils.url import absolute_url, canonical_url

__docformat__ = 'restructuredtext'


@adapter_config(name='title',
                required=(Interface, IPyAMSUserLayer, Interface),
                provides=IHTMLContentMetas)
class TitleMetasAdapter(ContextRequestViewAdapter):
    """Title metas adapter"""

    order = 1

    def get_metas(self):
        site_infos = ISiteRootInfos(self.request.root)
        site_title = II18n(site_infos).query_attribute('title', request=self.request)
        title = II18n(self.context).query_attribute('title', request=self.request)
        yield HTMLTagMeta('title',
                          f'{site_title} -- {title}' if (site_title and title) else (title or site_title or '--'))


@adapter_config(name='canonical',
                required=(Interface, IPyAMSUserLayer, Interface),
                provides=IHTMLContentMetas)
class CanonicalURLMetasAdapter(ContextRequestViewAdapter):
    """Canonical URL metas adapter"""

    order = 2

    def get_metas(self):
        target_url = canonical_url(self.context, self.request).replace('+', '%2B')
        yield BaseMeta(tag='link', rel='canonical', href=target_url)


@adapter_config(name='icon',
                required=(Interface, IPyAMSUserLayer, Interface),
                provides=IHTMLContentMetas)
class IconMetasAdapter(ContextRequestViewAdapter):
    """Icon metas adapter"""

    order = 20

    def get_metas(self):
        config = ISiteRootInfos(self.request.root, None)
        if (config is not None) and (config.icon is not None):
            icon = config.icon
            icon_url = absolute_url(icon, self.request)
            icon_size = icon.get_image_size()[0]
            dc = IZopeDublinCore(icon)
            timestamp = tztime(dc.modified).timestamp()
            for size in (16, 32, 72, 114, 144, 180):
                if icon_size < size:
                    break
                yield LinkMeta('apple-touch-icon',
                               type=icon.content_type,
                               href='{}/++thumb++{}x{}?_={}'.format(icon_url, size, size, timestamp),
                               sizes='{0}x{0}'.format(size))
            for size in (32, 124, 128):
                if icon_size < size:
                    break
                yield LinkMeta('icon',
                               type=icon.content_type,
                               href='{}/++thumb++{}x{}?_={}'.format(icon_url, size, size, timestamp),
                               sizes='{0}x{0}'.format(size))
            yield LinkMeta('shortcut-icon', type=icon.content_type, href=icon_url)
