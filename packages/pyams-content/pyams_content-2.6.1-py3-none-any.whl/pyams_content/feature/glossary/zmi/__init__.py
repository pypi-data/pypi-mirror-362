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

"""PyAMS_content.feature.glossary.zmi module

This module defines components used to handle glossary updater task.
"""

from pyams_content.component.thesaurus import ITagsManagerTarget
from pyams_content.component.thesaurus.zmi.manager import TagsManagerGlossaryGroup
from pyams_content.feature.glossary.interfaces import IGlossaryUpdaterTask
from pyams_content.feature.glossary.task import GlossaryUpdaterTask
from pyams_form.ajax import ajax_form_config
from pyams_layer.interfaces import IPyAMSLayer
from pyams_scheduler.interfaces import MANAGE_TASKS_PERMISSION
from pyams_scheduler.interfaces.folder import ITaskContainer
from pyams_scheduler.task.zmi import BaseTaskAddForm, BaseTaskEditForm
from pyams_scheduler.zmi import TaskContainerTable
from pyams_skin.interfaces.viewlet import IHelpViewletManager
from pyams_skin.viewlet.help import AlertMessage
from pyams_skin.viewlet.menu import MenuItem
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.viewlet import IContextAddingsViewletManager


__docformat__ = 'restructuredtext'

from pyams_content import _


@viewlet_config(name='tags-glossary.help',
                context=ITagsManagerTarget, layer=IAdminLayer, view=TagsManagerGlossaryGroup,
                manager=IHelpViewletManager, weight=1)
class TagsGlossaryHeader(AlertMessage):
    """Tags manager glossary help message"""

    status = 'info'

    _message = _("To use glossary features, you must define a glossary updater task "
                 "into tasks scheduler utility!")


@viewlet_config(name='add-glossary-updater-task.menu',
                context=ITaskContainer, layer=IAdminLayer, view=TaskContainerTable,
                manager=IContextAddingsViewletManager, weight=210,
                permission=MANAGE_TASKS_PERMISSION)
class GlossaryUpdaterTaskAddMenu(MenuItem):
    """Glossary updater task add menu"""

    label = _("Add glossary updater task...")
    href = 'add-glossary-updater-task.html'
    modal_target = True


@ajax_form_config(name='add-glossary-updater-task.html',
                  context=ITaskContainer, layer=IPyAMSLayer,
                  permission=MANAGE_TASKS_PERMISSION)
class GlossaryUpdaterTaskAddForm(BaseTaskAddForm):
    """Glossary updater task add form"""

    content_factory = IGlossaryUpdaterTask
    content_label = GlossaryUpdaterTask.label


@ajax_form_config(name='properties.html',
                  context=IGlossaryUpdaterTask, layer=IPyAMSLayer,
                  permission=MANAGE_TASKS_PERMISSION)
class GlossaryUpdaterTaskEditForm(BaseTaskEditForm):
    """Glossary updater task edit form"""
