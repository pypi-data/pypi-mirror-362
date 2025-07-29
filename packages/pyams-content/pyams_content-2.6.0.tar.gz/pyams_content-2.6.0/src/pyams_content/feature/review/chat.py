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

"""PyAMS_content.feature.review.chat module

Chat messages handlers for contents reviews.
"""

from pyramid.events import subscriber

from pyams_content.feature.review import ICommentAddedEvent, IReviewComments
from pyams_content.interfaces import OWNER_ROLE, READER_ROLE
from pyams_i18n.interfaces import II18n
from pyams_security.interfaces import IProtectedObject
from pyams_utils.adapter import ContextAdapter, adapter_config
from pyams_utils.request import query_request
from pyams_utils.url import absolute_url


__docformat__ = 'restructuredtext'

from pyams_content import _


try:
    from pyams_chat.interfaces import IChatMessage, IChatMessageHandler
    from pyams_chat.message import ChatMessage
except ImportError:
    pass
else:

    @subscriber(ICommentAddedEvent)
    def handle_new_comment(event):
        """Handle new review comment"""
        request = query_request()
        if request is None:
            return
        content = event.object
        translate = request.localizer.translate
        message = ChatMessage(request=request,
                              context=content,
                              action='notify',
                              category='content.review',
                              source=event.comment.owner,
                              title=translate(_("Review request")),
                              message=translate(_("A new comment was added on "
                                                  "content « {0} »")).format(
                                  II18n(content).query_attribute('title', request=request)),
                              url=absolute_url(content, request, 'admin#review-comments.html'),
                              comments=IReviewComments(content))
        message.send()


    @adapter_config(name='content.review',
                    required=IChatMessage,
                    provides=IChatMessageHandler)
    class ContentReviewMessageHandler(ContextAdapter):
        """Content review message handler"""

        def get_target(self):
            """Message targets getter"""
            context = self.context.context
            principals = set()
            protection = IProtectedObject(context, None)
            if protection is not None:
                principals |= protection.get_principals(READER_ROLE) | \
                              protection.get_principals(OWNER_ROLE)
            comments = self.context.user_data.get('comments')
            if comments is not None:
                principals |= comments.reviewers
            source_id = self.context.source['id']
            if source_id in principals:
                principals.remove(source_id)
            return {
                'principals': tuple(principals)
            }
