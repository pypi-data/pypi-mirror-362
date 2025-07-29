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

"""PyAMS_content.feature.glossary.interfaces module

This module defines glossary-related task interface.
"""

from zope.interface import Interface

from pyams_scheduler.interfaces import ITask


__docformat__ = 'restructuredtext'


REQUEST_GLOSSARY_KEY = 'pyams_content.glossary'


class IGlossaryUpdaterTaskInfo(Interface):
    """Glossary updated task base interface"""


class IGlossaryUpdaterTask(ITask, IGlossaryUpdaterTaskInfo):
    """Glossary updater task interface"""
