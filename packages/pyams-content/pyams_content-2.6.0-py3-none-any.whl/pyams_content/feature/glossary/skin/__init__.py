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

"""PyAMS_content.feature.glossary.skin module

This module defines glossary renderers and views.
"""

import logging
import pickle

from pyramid.decorator import reify
from pyramid.httpexceptions import HTTPNotFound
from zope.interface import implementer

from pyams_content.component.thesaurus import ITagsManager
from pyams_content.feature.glossary import GLOSSARY_CACHE_KEY, GLOSSARY_CACHE_NAME, \
    GLOSSARY_CACHE_NAMESPACE, GLOSSARY_CACHE_REGION, get_glossary_automaton
from pyams_content.feature.glossary.interfaces import REQUEST_GLOSSARY_KEY
from pyams_content.feature.glossary.skin.interfaces import IThesaurusTermRenderer
from pyams_layer.interfaces import IPyAMSUserLayer
from pyams_pagelet.pagelet import pagelet_config
from pyams_portal.skin.page import PortalContextIndexPage
from pyams_security.interfaces.base import VIEW_PERMISSION
from pyams_skin.interfaces.view import IModalPage
from pyams_template.template import layout_config, template_config
from pyams_utils.adapter import ContextRequestAdapter, adapter_config
from pyams_utils.cache import get_cache
from pyams_utils.interfaces.text import IHTMLRenderer


__docformat__ = 'restructuredtext'


LOGGER = logging.getLogger('PyAMS (content)')


@adapter_config(name='glossary',
                required=(str, IPyAMSUserLayer),
                provides=IHTMLRenderer)
class GlossaryHTMLRenderer(ContextRequestAdapter):
    """Glossary HTML renderer"""

    def render(self, **kwargs):
        """Glossary terms renderer"""
        source = self.context
        # check tags manager configuration
        manager = ITagsManager(self.request.root, None)
        if (manager is None) or not manager.enable_glossary:
            return source
        # get glossary automaton
        glossary_cache = get_cache(GLOSSARY_CACHE_NAME, GLOSSARY_CACHE_REGION,
                                   GLOSSARY_CACHE_NAMESPACE)
        try:
            LOGGER.debug("Loading glossary automaton...")
            automaton = glossary_cache.get_value(GLOSSARY_CACHE_KEY)
        except KeyError:
            LOGGER.debug("Automaton not found, loading new one...")
            automaton = get_glossary_automaton(self.request.root)
        else:
            automaton = pickle.loads(automaton)
        if automaton is None:
            LOGGER.debug("Missing automaton, skipping HTML conversion")
            return source
        LOGGER.debug("Automaton loaded with {} terms!".format(len(automaton)))
        #  iterate over automaton entries
        annotations = self.request.annotations
        found_terms = annotations.get(REQUEST_GLOSSARY_KEY) or set()
        last_found_index = 0
        marker = '<span class="thesaurus-term">{}</span>'
        marker_length = len(marker) - 2
        for position, text in automaton.iter(self.context):
            if (text in found_terms) or (position <= last_found_index):
                continue
            LOGGER.debug("Found term '{}' at position {}".format(text, position))
            count = len(found_terms)
            offset = marker_length * count
            start_offset = position + offset - len(text)
            if source[start_offset] in '<>':
                LOGGER.debug("Already tagged term, skipping...")
                continue
            source = source[0:start_offset + 1] + marker.format(text) + \
                source[position + offset + 1:]
            found_terms.add(text)
            last_found_index = position
        if last_found_index:
            self.request.annotations[REQUEST_GLOSSARY_KEY] = found_terms
        return source


class BaseGlossaryViewMixin:
    """Base glossary mixin view"""

    @reify
    def glossary(self):
        """Glossary getter"""
        tags_manager = ITagsManager(self.request.root, None)
        if tags_manager is None:
            raise HTTPNotFound("Can't find tags manager!")
        glossary = tags_manager.glossary
        if glossary is None:
            raise HTTPNotFound("Can't find glossary!")
        return glossary

    @property
    def title(self):
        """Title getter"""
        return self.glossary.title


@pagelet_config(name='get-glossary.html',
                layer=IPyAMSUserLayer,
                permission=VIEW_PERMISSION)
@template_config(template='templates/glossary.pt',
                 layer=IPyAMSUserLayer)
class GlossaryView(BaseGlossaryViewMixin, PortalContextIndexPage):
    """Glossary view"""

    def update(self):
        super().update()
        self.request.context = self.glossary


@template_config(template='templates/glossary-term.pt',
                 layer=IPyAMSUserLayer)
class BaseGlossaryTermViewMixin(BaseGlossaryViewMixin):
    """Base glossary term view mixin class"""

    @reify
    def term(self):
        """Term getter"""
        label = self.request.params.get('term')
        if not label:
            raise HTTPNotFound("No provided glossary term!")
        term = self.glossary.terms.get(label)
        if term is None:
            raise HTTPNotFound("Can't find provided term in glossary!")
        return term

    @property
    def renderers(self):
        registry = self.request.registry
        for name, renderer in sorted(registry.getAdapters((self.term, self.request, self),
                                                          IThesaurusTermRenderer),
                                     key=lambda x: x[1].weight):
            renderer.update()
            yield renderer

    @property
    def is_modal(self):
        return IModalPage.providedBy(self)


@pagelet_config(name='get-glossary-term-page.html',
                layer=IPyAMSUserLayer,
                permission=VIEW_PERMISSION)
class GlossaryTermPage(BaseGlossaryTermViewMixin, PortalContextIndexPage):
    """Glossary term page view"""

    def update(self):
        super().update()
        self.request.context = self.term


@pagelet_config(name='get-glossary-term.html',
                layer=IPyAMSUserLayer,
                permission=VIEW_PERMISSION)
@layout_config(template='templates/term-layout.pt',
               layer=IPyAMSUserLayer)
@implementer(IModalPage)
class GlossaryTermModalPage(BaseGlossaryTermViewMixin):
    """Glossary term modal page view"""

    modal_class = 'modal-dialog modal-dialog-scrollable modal-xl'
