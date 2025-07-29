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

"""PyAMS_content.workflow.zmi.task module

"""

__docformat__ = 'restructuredtext'

from zope.interface import Interface

from pyams_content.workflow import ContentArchivingTask, ContentPublishingTask
from pyams_content.workflow.interfaces import IWorkflowManagementTask
from pyams_utils.adapter import NullAdapter, adapter_config
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.table import ITableElementEditor


@adapter_config(required=(IWorkflowManagementTask, IAdminLayer, Interface),
                provides=ITableElementEditor)
class WorkflowManagementTaskEditor(NullAdapter):
    """Workflow management task editor"""
