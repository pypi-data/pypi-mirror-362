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

"""PyAMS_content.workflow.notify module

This module defines components which are used to send notifications to managers on
selected workflow events.
"""

from pyramid.events import subscriber
from pyramid.location import lineage

from pyams_content.interfaces import MANAGER_ROLE, MANAGE_CONTENT_PERMISSION
from pyams_content.shared.common.interfaces import IManagerRestrictions, \
    IManagerWorkflowRestrictions
from pyams_i18n.interfaces import II18n
from pyams_security.interfaces import IProtectedObject
from pyams_utils.adapter import ContextAdapter, adapter_config
from pyams_utils.request import query_request
from pyams_utils.url import absolute_url
from pyams_workflow.interfaces import IWorkflowTransitionEvent


__docformat__ = 'restructuredtext'


try:
    from pyams_chat.message import ChatMessage
    from pyams_chat.interfaces import IChatMessage, IChatMessageHandler
except ImportError:
    pass
else:

    @subscriber(IWorkflowTransitionEvent)
    def handle_workflow_transition(event):
        """Handle workflow transition event"""
        request = query_request()
        if request is None:
            return
        transition = event.transition
        if not (transition.user_data.get('notify_roles') and
                transition.user_data.get('notify_message')):
            return
        content = event.object
        translate = request.localizer.translate
        title = II18n(content).query_attribute('title', request=request)
        message = ChatMessage(request=request,
                              context=content,
                              action='notify',
                              category='content.workflow',
                              source=request.principal,
                              title=translate(transition.user_data.get('notify_title',
                                                                       transition.title)),
                              message=translate(transition.user_data.get('notify_message',
                                                                         '')).format(
                                  principal=request.principal.title,
                                  title=title),
                              url=absolute_url(content, request, 'admin'),
                              comment=event.comment,
                              transition=transition)
        message.send()


    @adapter_config(name='content.workflow',
                    required=IChatMessage,
                    provides=IChatMessageHandler)
    class ContentWorkflowTransitionChatHandler(ContextAdapter):
        """Content workflow transition chat message handler"""

        def get_target(self):
            """Chat message targets getter"""
            notify_roles = self.context.user_data['transition'].user_data.get('notify_roles', ())
            if '*' in notify_roles:
                return {}
            request = query_request()
            notification_source = self.context.context
            principals = set()
            for context in lineage(notification_source):
                protection = IProtectedObject(context, None)
                if protection is None:
                    continue
                for role_id in notify_roles:
                    if role_id == MANAGER_ROLE:
                        restrictions = IManagerRestrictions(context, None)
                        if restrictions is None:
                            continue
                        for principal in protection.get_principals(role_id):
                            principal_restrictions = restrictions.get_restrictions(principal)
                            if principal_restrictions:
                                workflow_restrictions = \
                                    IManagerWorkflowRestrictions(principal_restrictions, None)
                                if workflow_restrictions.can_access(notification_source,
                                                                    MANAGE_CONTENT_PERMISSION,
                                                                    request=request):
                                    principals.add(principal)
                    else:
                        principals |= protection.get_principals(role_id)
            source_id = self.context.source['id']
            if source_id in principals:
                principals.remove(source_id)
            return {
                'principals': tuple(principals)
            }
