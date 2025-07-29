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

"""PyAMS_content.feature.review module

"""

from datetime import datetime, timezone
from uuid import uuid4

from persistent import Persistent
from pyramid.events import subscriber
from zope.container.contained import Contained
from zope.lifecycleevent import IObjectCreatedEvent
from zope.location.interfaces import ISublocations
from zope.schema.fieldproperty import FieldProperty
from zope.traversing.interfaces import ITraversable

from pyams_content.feature.review.interfaces import CommentAddedEvent, ICommentAddedEvent, \
    IReviewComment, IReviewComments, IReviewManager, IReviewTarget, REVIEW_COMMENTS_ANNOTATION_KEY
from pyams_security.interfaces import ISecurityManager
from pyams_utils.adapter import ContextAdapter, adapter_config, get_annotation_adapter
from pyams_utils.container import BTreeOrderedContainer
from pyams_utils.factory import factory_config
from pyams_utils.registry import get_pyramid_registry, get_utility
from pyams_workflow.interfaces import IObjectClonedEvent

__docformat__ = 'restructuredtext'


@factory_config(IReviewComment)
class ReviewComment(Persistent, Contained):
    """Review comment persistent class"""

    owner = FieldProperty(IReviewComment['owner'])
    reviewers = FieldProperty(IReviewComment['reviewers'])
    comment_type = FieldProperty(IReviewComment['comment_type'])
    comment = FieldProperty(IReviewComment['comment'])
    is_reviewer_comment = FieldProperty(IReviewComment['is_reviewer_comment'])
    creation_date = FieldProperty(IReviewComment['creation_date'])

    def __init__(self, owner, comment, comment_type='comment', reviewers=None):
        self.owner = owner
        self.comment = comment
        self.comment_type = comment_type
        sm = get_utility(ISecurityManager)
        if reviewers:
            self.reviewers = ', '.join((
                principal.title
                for principal in (sm.get_principal(reviewer) for reviewer in reviewers)
            ))
        self.creation_date = datetime.now(timezone.utc)


@factory_config(IReviewComments)
class ReviewCommentsContainer(BTreeOrderedContainer):
    """Review comments container"""

    reviewers = FieldProperty(IReviewComments['reviewers'])

    def clear(self):
        for k in self.keys()[:]:
            del self[k]

    def add_comment(self, comment):
        uuid = str(uuid4())
        self[uuid] = comment
        reviewers = self.reviewers or set()
        reviewers.add(comment.owner)
        self.reviewers = reviewers
        get_pyramid_registry().notify(CommentAddedEvent(self.__parent__, comment))


@adapter_config(required=IReviewTarget,
                provides=IReviewComments)
def review_comments_factory(context):
    """Review comments factory"""
    return get_annotation_adapter(context, REVIEW_COMMENTS_ANNOTATION_KEY, IReviewComments,
                                  name='++review-comments++')


@adapter_config(name='review-comments',
                required=IReviewTarget,
                provides=ITraversable)
class ReviewCommentsNamespace(ContextAdapter):
    """++review-comments++ namespace traverser"""

    def traverse(self, name, furtherpath=None):
        return IReviewComments(self.context)


@adapter_config(name='review-comments',
                required=IReviewTarget,
                provides=ISublocations)
class ReviewCommentsSublocations(ContextAdapter):
    """Review comments sub-location adapter"""

    def sublocations(self):
        """Sub-locations iterator"""
        yield from IReviewComments(self.context).values()


@subscriber(IObjectCreatedEvent, context_selector=IReviewTarget)
@subscriber(IObjectClonedEvent, context_selector=IReviewTarget)
def clone_review_target(event):
    """Clear comments when a review target is cloned"""
    comments = IReviewComments(event.object, None)
    if comments is not None:
        comments.clear()
