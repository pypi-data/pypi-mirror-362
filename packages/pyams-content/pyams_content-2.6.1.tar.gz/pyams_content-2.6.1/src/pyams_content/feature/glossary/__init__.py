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

"""PyAMS_content.feature.glossary main module

This module defines several helper functions which are used to update glossary.
"""

import logging
import pickle

from ahocorasick import Automaton

from pyams_content.component.thesaurus import ITagsManager
from pyams_thesaurus.interfaces.term import STATUS_PUBLISHED
from pyams_thesaurus.interfaces.thesaurus import IThesaurus
from pyams_utils.cache import get_cache
from pyams_utils.registry import query_utility


__docformat__ = 'restructuredtext'


LOGGER = logging.getLogger('PyAMS (content)')

GLOSSARY_CACHE_NAME = 'persistent'
GLOSSARY_CACHE_REGION = 'persistent'
GLOSSARY_CACHE_NAMESPACE = 'PyAMS::glossary'
GLOSSARY_CACHE_KEY = 'automaton'


def get_glossary_automaton(root):
    """Generate and store glossary automaton"""
    # generate automaton
    tags_manager = ITagsManager(root)
    if not tags_manager.enable_glossary:
        return None
    thesaurus = query_utility(IThesaurus, name=tags_manager.glossary_thesaurus_name)
    if thesaurus is None:
        return None
    LOGGER.debug("Building glossary automaton...")
    automaton = Automaton()
    for term in thesaurus.terms.values():
        if term.status == STATUS_PUBLISHED:
            automaton.add_word(term.label, term.label)
    automaton.make_automaton()
    LOGGER.debug("Automaton built with {} terms".format(len(automaton)))
    # store automaton items
    glossary_cache = get_cache(GLOSSARY_CACHE_NAME, GLOSSARY_CACHE_REGION,
                               GLOSSARY_CACHE_NAMESPACE)
    glossary_cache.set_value(GLOSSARY_CACHE_KEY, pickle.dumps(automaton))
    return automaton


def reset_glossary_automaton():
    """Re-initialize glossary automaton"""
    glossary_cache = get_cache(GLOSSARY_CACHE_NAME, GLOSSARY_CACHE_REGION,
                               GLOSSARY_CACHE_NAMESPACE)
    glossary_cache.clear()
