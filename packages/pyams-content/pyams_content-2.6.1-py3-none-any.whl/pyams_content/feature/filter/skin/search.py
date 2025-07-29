# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

__docformat__ = 'restructuredtext'

from pyams_content.feature.search import ISearchFolder
from pyams_content.feature.search.interfaces import ISearchFormRequestParams
from pyams_layer.interfaces import IPyAMSUserLayer
from pyams_utils.adapter import ContextRequestAdapter, adapter_config


class BaseFormRequestParams(ContextRequestAdapter):
    """Base form request parameters adapter"""

    param_name = None
    
    def get_params(self):
        for value in self.request.params.getall(self.param_name):
            yield {
                'name': self.param_name,
                'value': value
            }


@adapter_config(name='content_type',
                required=(ISearchFolder, IPyAMSUserLayer),
                provides=ISearchFormRequestParams)
class SearchFormContentTypeRequestParams(BaseFormRequestParams):
    """Search form content-type request parameters adapter"""
    
    param_nam = 'content_type'


@adapter_config(name='data_type',
                required=(ISearchFolder, IPyAMSUserLayer),
                provides=ISearchFormRequestParams)
class SearchFormDataTypeRequestParams(BaseFormRequestParams):
    """Search form data-type request parameters adapter"""
    
    param_name = 'data_type'


@adapter_config(name='facet_label',
                required=(ISearchFolder, IPyAMSUserLayer),
                provides=ISearchFormRequestParams)
class SearchFormFacetLabelRequestParams(BaseFormRequestParams):
    """Search form facet label request parameters adapter"""

    param_name = 'facet_label'


@adapter_config(name='facet_type_label',
                required=(ISearchFolder, IPyAMSUserLayer),
                provides=ISearchFormRequestParams)
class SearchFormFacetTypeLabelRequestParams(BaseFormRequestParams):
    """Search form facet type label request parameters adapter"""

    param_name = 'facet_type_label'


@adapter_config(name='title',
                required=(ISearchFolder, IPyAMSUserLayer),
                provides=ISearchFormRequestParams)
class SearchFormTitleRequestParams(BaseFormRequestParams):
    """Search form title request parameters adapter"""
    
    param_name = 'title'
    
    
@adapter_config(name='tags',
                required=(ISearchFolder, IPyAMSUserLayer),
                provides=ISearchFormRequestParams)
class SearchFormTagsRequestParams(BaseFormRequestParams):
    """Search form tags request parameters adapter"""
    
    param_name = 'tag'


@adapter_config(name='themes',
                required=(ISearchFolder, IPyAMSUserLayer),
                provides=ISearchFormRequestParams)
class SearchFormThemesRequestParams(BaseFormRequestParams):
    """Search form themes request parameters adapter"""
    
    param_name = 'theme'


@adapter_config(name='collections',
                required=(ISearchFolder, IPyAMSUserLayer),
                provides=ISearchFormRequestParams)
class SearchFormCollectionsRequestParams(BaseFormRequestParams):
    """Search form collections request parameters adapter"""
    
    param_name = 'collection'
