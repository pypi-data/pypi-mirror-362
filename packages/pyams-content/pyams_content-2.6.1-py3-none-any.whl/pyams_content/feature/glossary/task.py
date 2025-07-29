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

"""PyAMS_content.feature.glossary.task module

This module defines a custom scheduler task which can be used to handle
glossary automaton update.

This task has to be planned like all normal tasks.
"""

import sys
import traceback

from pyramid.events import subscriber
from zope.lifecycleevent import IObjectAddedEvent, IObjectModifiedEvent, IObjectRemovedEvent

from pyams_content.component.thesaurus import ITagsManager
from pyams_content.feature.glossary import get_glossary_automaton
from pyams_content.feature.glossary.interfaces import IGlossaryUpdaterTask
from pyams_scheduler.interfaces import IScheduler
from pyams_scheduler.interfaces.task import TASK_STATUS_FAIL, TASK_STATUS_OK
from pyams_scheduler.task import Task
from pyams_site.interfaces import ISiteRoot
from pyams_thesaurus.interfaces.term import IThesaurusTerm
from pyams_utils.factory import factory_config
from pyams_utils.finder import find_objects_providing
from pyams_utils.registry import get_utility
from pyams_utils.request import check_request
from pyams_utils.traversing import get_parent


__docformat__ = 'restructuredtext'

from pyams_content import _


@factory_config(IGlossaryUpdaterTask)
class GlossaryUpdaterTask(Task):
    """Glossary updater task"""

    label = _("Glossary updater task")
    icon_class = 'fas fa-book'
    
    is_zodb_task = True

    def run(self, report, **kwargs):  # pylint: disable=unused-argument
        """Run glossary automaton update"""
        try:
            report.writeln('Glossary automaton update', prefix='### ')
            root = get_parent(self, ISiteRoot)
            automaton = get_glossary_automaton(root)
            report.writeln(f'Automaton size: **{len(automaton)} terms**', suffix='\n')
            return TASK_STATUS_OK, automaton
        except Exception:  # pylint: disable=bare-except
            report.writeln('**An SQL error occurred**', suffix='\n')
            report.write_exception(*sys.exc_info())
            return TASK_STATUS_FAIL, None


@subscriber(IObjectAddedEvent, context_selector=IThesaurusTerm)
@subscriber(IObjectModifiedEvent, context_selector=IThesaurusTerm)
@subscriber(IObjectRemovedEvent, context_selector=IThesaurusTerm)
def handle_updated_thesaurus_term(event):
    """Reset glossary automaton on term update"""
    request = check_request()
    tags_manager = ITagsManager(request.root)
    if not tags_manager.enable_glossary:
        return
    scheduler = get_utility(IScheduler)
    for task in find_objects_providing(scheduler, IGlossaryUpdaterTask):
        task.launch()
        break
