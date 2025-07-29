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

"""PyAMS_content.feature.review.interfaces module

"""

from zope.annotation import IAttributeAnnotatable
from zope.container.constraints import containers, contains
from zope.interface import Attribute, Interface, implementer
from zope.interface.interfaces import IObjectEvent, ObjectEvent
from zope.location.interfaces import IContained
from zope.schema import Bool, Choice, Datetime, Text, TextLine
from zope.schema.interfaces import IContainer

from pyams_security.schema import PrincipalField, PrincipalsSetField


__docformat__ = 'restructuredtext'

from pyams_content import _


COMMENT_TYPES = {
    'request': _("Review request"),
    'comment': _("Reviewer comment")
}


class ICommentAddedEvent(IObjectEvent):
    """Comment added event interface"""

    comment = Attribute("New comment")


@implementer(ICommentAddedEvent)
class CommentAddedEvent(ObjectEvent):
    """Comment added event"""

    def __init__(self, object, comment):
        super().__init__(object)
        self.comment = comment


class IReviewComment(IContained, IAttributeAnnotatable):
    """Review comment interface"""

    containers('.IReviewComments')

    owner = PrincipalField(title=_("Comment writer"),
                           required=True)

    reviewers = TextLine(title=_("Content reviewers"),
                         required=False)

    comment_type = Choice(title=_("Comment type"),
                          values=COMMENT_TYPES.keys(),
                          required=True,
                          default='comment')

    comment = Text(title=_("Comment body"),
                   required=True)

    is_reviewer_comment = Bool(title=_("Reviewer comment?"),
                               required=True,
                               default=False)

    creation_date = Datetime(title=_("Creation date"),
                             required=False)


REVIEW_COMMENTS_ANNOTATION_KEY = 'pyams_content.review.comments'


class IReviewComments(IContainer):
    """Review comment container interface"""

    contains(IReviewComment)

    reviewers = PrincipalsSetField(title=_("Reviewers list"),
                                   description=_("List of principals which reviewed the comment"),
                                   required=False)

    def clear(self):
        """Remove all comments"""

    def add_comment(self, comment):
        """Add given comment to list"""


class IReviewManager(Interface):
    """Content review interface"""

    def ask_review(self, reviewers, comment, notify=True, request=None):
        """Ask for content review"""


class IReviewTarget(Interface):
    """Review target marker interface

    This interface is used to mark contents which can handle review.
    """
