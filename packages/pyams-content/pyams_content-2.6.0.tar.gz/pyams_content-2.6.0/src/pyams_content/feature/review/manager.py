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

"""PyAMS_content.feature.review.manager module

Review target adapter.
"""

from pyramid.renderers import render

from pyams_content.feature.review import IReviewComments, IReviewManager, IReviewTarget, \
    ReviewComment
from pyams_content.shared.common.interfaces import IWfSharedContentRoles
from pyams_mail.interfaces import IPrincipalMailInfo
from pyams_mail.message import HTMLMessage
from pyams_security.interfaces import ISecurityManager
from pyams_security.interfaces.notification import INotificationSettings
from pyams_security.principal import MissingPrincipal
from pyams_utils.adapter import ContextAdapter, adapter_config
from pyams_utils.registry import get_utility
from pyams_utils.request import check_request


__docformat__ = 'restructuredtext'

from pyams_content import _


@adapter_config(required=IReviewTarget,
                provides=IReviewManager)
class ReviewManagerAdapter(ContextAdapter):
    """Review manager adapter"""

    def ask_review(self, reviewers, comment, notify_all=True, request=None):
        """Ask for content review"""
        roles = IWfSharedContentRoles(self.context, None)
        if roles is None:
            return
        # check request
        if request is None:
            request = check_request()
        translate = request.localizer.translate
        # initialize mailer
        sm = get_utility(ISecurityManager)  # pylint: disable=invalid-name
        settings = INotificationSettings(sm)
        sender_name = request.principal.title \
            if request.principal is not None else settings.sender_name
        sender_address = settings.sender_email
        sender = sm.get_raw_principal(request.principal.id)
        sender_mail_info = IPrincipalMailInfo(sender, None)
        if sender_mail_info is not None:
            for sender_name, sender_address in sender_mail_info.get_addresses():
                break
        if settings.enable_notifications:
            mailer = settings.get_mailer()
        else:
            mailer = None
        # create message
        html_body = render('zmi/templates/mail-notification.pt', request=request, value={
            'settings': settings,
            'comment': comment,
            'sender': sender_name
        })
        # notify reviewers
        notifications = 0
        readers = roles.readers.copy()
        for reviewer in reviewers:
            if settings.enable_notifications and \
                    (mailer is not None) and \
                    (notify_all or (reviewer not in readers)):
                principal = sm.get_raw_principal(reviewer)
                if not isinstance(principal, MissingPrincipal):
                    mail_info = IPrincipalMailInfo(principal, None)
                    if mail_info is not None:
                        for name, address in mail_info.get_addresses():
                            message = HTMLMessage(
                                subject=translate(_("{service_name}A content review is "
                                                    "requested")).format(
                                    service_name=f'[{settings.subject_prefix}] '
                                        if settings.subject_prefix else ''),
                                from_addr=f'{settings.sender_name} <{settings.sender_email}>',
                                reply_to=f'{sender_name} <{sender_address}>',
                                to_addr=f'{name} <{address}>',
                                html=html_body)
                            mailer.send(message)
                            notifications += 1
            readers.add(reviewer)
        roles.readers = readers
        # add comment
        review_comment = ReviewComment(owner=request.principal.id,
                                       comment_type='request',
                                       comment=translate(_("Request comment: "
                                                           "{comment}")).format(comment=comment),
                                       reviewers=reviewers)
        IReviewComments(self.context).add_comment(review_comment)
        # return notifications count
        return notifications
