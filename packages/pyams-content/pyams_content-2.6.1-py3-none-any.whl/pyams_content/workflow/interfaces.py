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

"""PyAMS_content.workflow.interfaces module

This module defines custom workflow-related interfaces.
"""

from pyams_scheduler.interfaces import ITask
from pyams_workflow.interfaces import IWorkflow


__docformat__ = 'restructuredtext'


class IContentWorkflow(IWorkflow):
    """PyAMS default content workflow marker interface"""


class IBasicWorkflow(IWorkflow):
    """PyAMS basic workflow marker interface"""


class IWorkflowManagementTask(ITask):
    """Workflow management task marker interface

    This interface is used to mark scheduler tasks (see PyAMS_scheduler) which are
    used by some workflows which can provide a "future" publication date, and which
    relies on task scheduler to do the actual publication.
    """
