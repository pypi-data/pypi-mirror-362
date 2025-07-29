#
# Copyright (c) 2015-2021 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_content.workflow.task module

This module defines scheduler tasks which are used to automatically publish or retire
contents which were published with a future publication date of with a planned retiring date.
"""

import logging
from datetime import datetime, timedelta, timezone

from pyramid.events import subscriber
from transaction.interfaces import ITransactionManager
from zope.interface import implementer
from zope.intid import IIntIds

from pyams_content.workflow.interfaces import IWorkflowManagementTask
from pyams_scheduler.interfaces import ISchedulerProcess, SCHEDULER_NAME
from pyams_scheduler.interfaces.task import IDateTaskScheduling, TASK_STATUS_OK
from pyams_scheduler.process import TaskResettingThread
from pyams_scheduler.task import Task
from pyams_security.interfaces.names import INTERNAL_USER_ID
from pyams_site.interfaces import PYAMS_APPLICATION_SETTINGS_KEY, PYAMS_APPLICATION_DEFAULT_NAME
from pyams_utils.registry import get_pyramid_registry, get_utility
from pyams_utils.timezone import gmtime
from pyams_utils.zodb import ZODBConnection
from pyams_workflow.interfaces import IWorkflow, IWorkflowInfo, IWorkflowState
from pyams_zmq.interfaces import IZMQProcessStartedEvent

__docformat__ = 'restructuredtext'

from pyams_content import _


LOGGER = logging.getLogger('PyAMS (content)')


@implementer(IWorkflowManagementTask)
class ContentPublishingTask(Task):
    """Content publisher task"""

    label = _("Content publisher task")
    icon_class = 'fas fa-share'

    settings_view_name = None
    principal_id = INTERNAL_USER_ID
    
    is_zodb_task = True

    def __init__(self, oid, transition_id):
        super().__init__()
        self.oid = oid
        self.transition_id = transition_id

    def run(self, report, **kwargs):
        intids = get_utility(IIntIds)
        content = intids.queryObject(self.oid)
        if content is None:
            LOGGER.debug(">>> can't find publisher task target with OID {}".format(self.oid))
        else:
            workflow = IWorkflow(content)
            state = IWorkflowState(content)
            if state.state in workflow.visible_states:
                LOGGER.debug(">>> content is already published!")
            else:
                info = IWorkflowInfo(content)
                info.fire_transition(self.transition_id,
                                     check_security=False,
                                     principal=self.principal_id)
                info.fire_automatic()
        # remove task after execution!
        if self.__parent__ is not None:
            del self.__parent__[self.__name__]
        return TASK_STATUS_OK, None


@implementer(IWorkflowManagementTask)
class ContentArchivingTask(Task):
    """Content archiving task"""

    label = _("Content archiver task")
    icon_class = 'fas fa-reply'

    settings_view_name = None
    principal_id = INTERNAL_USER_ID
    
    is_zodb_task = True

    def __init__(self, oid):
        super().__init__()
        self.oid = oid

    def run(self, report, **kwargs):
        intids = get_utility(IIntIds)
        content = intids.queryObject(self.oid)
        if content is None:
            LOGGER.debug(">>> can't find archiving task target with OID {}".format(self.oid))
        else:
            workflow = IWorkflow(content)
            state = IWorkflowState(content)
            if state.state not in workflow.visible_states:
                LOGGER.debug(">>> content is not currently published!")
            else:
                info = IWorkflowInfo(content)
                info.fire_transition_toward(workflow.auto_retired_state,
                                            check_security=False,
                                            principal=self.principal_id)
                info.fire_automatic()
        # remove task after execution!
        if self.__parent__ is not None:
            del self.__parent__[self.__name__]
        return TASK_STATUS_OK, None


@subscriber(IZMQProcessStartedEvent, context_selector=ISchedulerProcess)
def handle_scheduler_start(event):
    """Check for scheduler tasks

    Workflow management tasks are typically automatically deleted after their execution.
    If tasks with a passed execution date are still present in the scheduler, this is generally
    because the scheduler was stopped at task execution time; so tasks which where not run are
    re-scheduled at process startup in the very near future...
    """
    with ZODBConnection() as root:
        registry = get_pyramid_registry()
        application_name = registry.settings.get(PYAMS_APPLICATION_SETTINGS_KEY,
                                                 PYAMS_APPLICATION_DEFAULT_NAME)
        application = root.get(application_name)
        sm = application.getSiteManager()  # pylint: disable=invalid-name
        scheduler = sm.get(SCHEDULER_NAME)
        if scheduler is not None:
            LOGGER.debug("Checking pending scheduler tasks on {!r}".format(scheduler))
            for task in scheduler.values():
                if not IWorkflowManagementTask.providedBy(task):
                    continue
                schedule_info = IDateTaskScheduling(task, None)
                if schedule_info is None:  # no date scheduling
                    continue
                now = datetime.now(timezone.utc)
                if schedule_info.active and (schedule_info.start_date < now):
                    # we add a small amount of time to be sure that scheduler and indexer
                    # processes are started...
                    schedule_info.start_date = now + timedelta(minutes=1)
                    # commit update for reset thread to get updated data!!
                    ITransactionManager(task).commit()
                    # start task resetting thread
                    LOGGER.debug(" - restarting task « {} »".format(task.name))
                    TaskResettingThread(event.object, task).start()
