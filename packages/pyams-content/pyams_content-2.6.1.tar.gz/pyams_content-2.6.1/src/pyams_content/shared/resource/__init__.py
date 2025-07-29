#
# Copyright (c) 2015-2025 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_content.shared.resource module

"""

from persistent import Persistent
from zope.container.contained import Contained
from zope.interface import implementer
from zope.schema.fieldproperty import FieldProperty

from pyams_content.component.illustration import IIllustrationTarget, ILinkIllustrationTarget
from pyams_content.component.paragraph import IParagraphContainerTarget
from pyams_content.component.thesaurus import ICollectionsTarget, ITagsTarget, IThemesTarget
from pyams_content.feature.preview.interfaces import IPreviewTarget
from pyams_content.feature.review import IReviewTarget
from pyams_content.shared.common import ISharedContent, IWfSharedContent, SharedContent, WfSharedContent
from pyams_content.shared.common.types import WfTypedSharedContentMixin
from pyams_content.shared.resource.interfaces import IResource, IResourceInfo, IWfResource, RESOURCE_CONTENT_NAME, \
    RESOURCE_CONTENT_TYPE, RESOURCE_INFORMATION_KEY
from pyams_security.interfaces import IViewContextPermissionChecker
from pyams_utils.adapter import adapter_config, get_annotation_adapter
from pyams_utils.factory import factory_config
from pyams_utils.traversing import get_parent

__docformat__ = 'restructuredtext'


@factory_config(IWfResource)
@factory_config(IWfSharedContent, name=RESOURCE_CONTENT_TYPE)
@implementer(IIllustrationTarget, ILinkIllustrationTarget, IParagraphContainerTarget,
             ITagsTarget, IThemesTarget, ICollectionsTarget, IReviewTarget, IPreviewTarget)
class WfResource(WfSharedContent, WfTypedSharedContentMixin):
    """Base resource content"""

    content_type = RESOURCE_CONTENT_TYPE
    content_name = RESOURCE_CONTENT_NAME
    content_intf = IWfResource
    content_view = True
    
    references = FieldProperty(IWfResource['references'])
    data_type = FieldProperty(IWfResource['data_type'])


@factory_config(IResourceInfo)
class ResourceInfo(Persistent, Contained):
    """Resource info persistent class"""

    original_country = FieldProperty(IResourceInfo['original_country'])
    original_title = FieldProperty(IResourceInfo['original_title'])
    author = FieldProperty(IResourceInfo['author'])
    translator = FieldProperty(IResourceInfo['translator'])
    illustrator = FieldProperty(IResourceInfo['illustrator'])
    drawer = FieldProperty(IResourceInfo['drawer'])
    colourist = FieldProperty(IResourceInfo['colourist'])
    lettering = FieldProperty(IResourceInfo['lettering'])
    producer = FieldProperty(IResourceInfo['producer'])
    director = FieldProperty(IResourceInfo['director'])
    actors = FieldProperty(IResourceInfo['actors'])
    editor = FieldProperty(IResourceInfo['editor'])
    collection = FieldProperty(IResourceInfo['collection'])
    series = FieldProperty(IResourceInfo['series'])
    volume = FieldProperty(IResourceInfo['volume'])
    format = FieldProperty(IResourceInfo['format'])
    nb_pages = FieldProperty(IResourceInfo['nb_pages'])
    duration = FieldProperty(IResourceInfo['duration'])
    age_range = FieldProperty(IResourceInfo['age_range'])
    release_year = FieldProperty(IResourceInfo['release_year'])
    awards = FieldProperty(IResourceInfo['awards'])
    editor_reference = FieldProperty(IResourceInfo['editor_reference'])
    isbn_number = FieldProperty(IResourceInfo['isbn_number'])
    price = FieldProperty(IResourceInfo['price'])
    source_url = FieldProperty(IResourceInfo['source_url'])
    summary = FieldProperty(IResourceInfo['summary'])
    synopsis = FieldProperty(IResourceInfo['synopsis'])
    publisher_words = FieldProperty(IResourceInfo['publisher_words'])


@adapter_config(required=IResourceInfo,
                provides=IViewContextPermissionChecker)
def resource_info_permission_checker(context):
    """Resource permission checker"""
    resource = get_parent(context, IWfResource)
    return IViewContextPermissionChecker(resource)


@adapter_config(required=IWfResource,
                provides=IResourceInfo)
def resource_info(context):
    """Resource information adapter"""
    return get_annotation_adapter(context, RESOURCE_INFORMATION_KEY, IResourceInfo)
    
    
@factory_config(IResource)
@factory_config(ISharedContent, name=RESOURCE_CONTENT_TYPE)
class Resource(SharedContent):
    """Workflow managed resource class"""
    
    content_type = RESOURCE_CONTENT_TYPE
    content_name = RESOURCE_CONTENT_NAME
