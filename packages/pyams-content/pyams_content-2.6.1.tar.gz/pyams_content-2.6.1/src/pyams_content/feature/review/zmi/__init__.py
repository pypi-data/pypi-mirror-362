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

"""PyAMS_content.feature.review.zmi module

Management components for content review.
"""

from pyramid.renderers import render
from pyramid.view import view_config
from zope.interface import Interface
from zope.schema import Bool, Text

from pyams_content.feature.review import IReviewComment, IReviewComments, IReviewManager, \
    IReviewTarget
from pyams_content.interfaces import COMMENT_CONTENT_PERMISSION, MANAGE_CONTENT_PERMISSION
from pyams_content.shared.common import IWfSharedContentRoles
from pyams_content.zmi import content_js
from pyams_form.ajax import ajax_form_config
from pyams_form.button import Buttons, handler
from pyams_form.field import Fields
from pyams_form.interfaces.form import IAJAXFormRenderer
from pyams_i18n.interfaces import II18n
from pyams_layer.interfaces import IPyAMSLayer
from pyams_pagelet.pagelet import pagelet_config
from pyams_security.interfaces import ISecurityManager
from pyams_security.schema import PrincipalsSetField
from pyams_security.utility import get_principal
from pyams_skin.schema.button import CloseButton, SubmitButton
from pyams_skin.viewlet.menu import MenuItem
from pyams_template.template import template_config
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config
from pyams_utils.date import format_datetime, get_age
from pyams_utils.factory import get_object_factory
from pyams_utils.fanstatic import get_resource_path
from pyams_utils.registry import get_utility
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.form import AdminModalAddForm
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.profile import IUserProfile
from pyams_zmi.interfaces.viewlet import IContextActionsDropdownMenu, IContentManagementMenu
from pyams_zmi.view import InnerAdminView
from pyams_zmi.zmi.viewlet.menu import NavigationMenuItem


__docformat__ = 'restructuredtext'

from pyams_content import _


@viewlet_config(name='content-review.menu',
                context=IReviewTarget, layer=IAdminLayer,
                manager=IContextActionsDropdownMenu, weight=10,
                permission=MANAGE_CONTENT_PERMISSION)
class ContentReviewMenu(MenuItem):
    """Content review menu"""

    label = _("Ask for content review")
    icon_class = 'fas fa-eye'

    href = 'content-review.html'
    modal_target = True


class IContentReviewFormFields(Interface):
    """Content review interface"""

    reviewers = PrincipalsSetField(title=_("Sought principals"),
                                   description=_("List of principals from which a review is "
                                                 "requested"),
                                   required=True)

    comment = Text(title=_("Comment"),
                   description=_("Comment associated with this request"),
                   required=True)

    notify_all = Bool(title=_("Notify all reviewers"),
                      description=_("If 'yes', selected reviewers will be notified by mail of "
                                    "your request, even if they were already members of the "
                                    "reviewers group. Otherwise, only new reviewers will be "
                                    "notified"),
                      default=True,
                      required=True)


class IContentReviewButtons(Interface):
    """Shared content review form buttons"""

    review = SubmitButton(name='review',
                          title=_("Ask for content review"))

    close = CloseButton(name='close',
                        title=_("Cancel"))


@ajax_form_config(name='content-review.html',
                  context=IReviewTarget, layer=IPyAMSLayer,
                  permission=MANAGE_CONTENT_PERMISSION)
class ContentReviewAskForm(AdminModalAddForm):
    """Content review add form"""

    subtitle = _("Content review")
    legend = _("Content review request")

    fields = Fields(IContentReviewFormFields)
    buttons = Buttons(IContentReviewButtons)

    _edit_permission = MANAGE_CONTENT_PERMISSION

    def update_widgets(self, prefix=None):
        super().update_widgets(prefix)
        comment = self.widgets.get('comment')
        if comment is not None:
            comment.rows = 10

    @handler(buttons['review'])
    def handle_review(self, action):
        """Review button handler"""
        self.handle_add(self, action)

    def create_and_add(self, data):
        data = data.get(self, data)
        manager = IReviewManager(self.context, None)
        if manager is not None:
            return manager.ask_review(request=self.request, **data)


@adapter_config(required=(IReviewTarget, IAdminLayer, ContentReviewAskForm),
                provides=IAJAXFormRenderer)
class ContentReviewAskFormRenderer(ContextRequestViewAdapter):
    """Content review ask form renderer"""

    def render(self, changes):
        """AJAX form renderer"""
        if changes is None:
            return None
        translate = self.request.localizer.translate
        if changes:
            message = translate(_("Request successful, {count} new notifications "
                                  "have been sent.")).format(count=changes)
        else:
            message = translate(_("Request successful, no new notification have been sent."))
        comments = IReviewComments(self.context)
        return {
            'status': 'reload',
            'smallbox': {
                'status': 'success',
                'message': message
            },
            'events': [{
                'event': 'update-comments.ams.content',
                'options': {
                    'count': len(comments)
                }
            }]
        }


#
# Share contents comments
#

@viewlet_config(name='review-comments.menu',
                context=IReviewTarget, layer=IAdminLayer,
                manager=IContentManagementMenu, weight=30,
                permission=COMMENT_CONTENT_PERMISSION)
class ContentReviewCommentsMenu(NavigationMenuItem):
    """Content review comments menu"""

    label = _("Comments")
    icon_class = 'far fa-comments'

    href = '#review-comments.html'

    badge_status = 'info'

    @property
    def object_data(self):
        """Object data getter"""
        return {
            'ams-modules': {
                'content': {
                    'src': get_resource_path(content_js)
                }
            },
            'ams-callback': 'MyAMS.content.review.init'
        }

    def update(self):
        super().update()
        nb_comments = len(IReviewComments(self.context))
        self.badge = str(nb_comments)


@pagelet_config(name='review-comments.html',
                context=IReviewTarget, layer=IPyAMSLayer,
                permission=COMMENT_CONTENT_PERMISSION)
@template_config(template='templates/comments.pt', layer=IAdminLayer)
class ContentReviewCommentsView(InnerAdminView):
    """Content review comments view"""

    title = _("Version comments")

    comments = None
    security = None

    def update(self):
        super().update()
        self.comments = IReviewComments(self.context).values()
        self.security = get_utility(ISecurityManager)

    def get_principal(self, principal_id):
        """Principal getter"""
        return self.security.get_principal(principal_id)

    @staticmethod
    def get_avatar(principal):
        """Principal avatar getter"""
        return IUserProfile(principal).get_avatar()

    @staticmethod
    def get_date(comment):
        """Comment date getter"""
        return format_datetime(comment.creation_date)

    @staticmethod
    def get_age(comment):
        """Comment age getter"""
        return get_age(comment.creation_date)


@view_config(name='add-review-comment.json',
             context=IReviewTarget, request_type=IPyAMSLayer,
             renderer='json', xhr=True,
             permission=COMMENT_CONTENT_PERMISSION)
def add_review_comment(request):
    """Review comment add view"""
    translate = request.localizer.translate
    comment_body = request.params.get('comment')
    if not comment_body:
        return {
            'status': 'error',
            'message': translate(_("Message is mandatory!"))
        }
    # add new comment
    comments = IReviewComments(request.context)
    factory = get_object_factory(IReviewComment)
    comment = factory(owner=request.principal.id,
                      comment=request.params.get('comment'))
    roles = IWfSharedContentRoles(request.context, None)
    if roles is not None:
        comment.is_reviewer_comment = comment.owner in (roles.readers or ())
    comments.add_comment(comment)
    # return comment infos
    profile = IUserProfile(request.principal)
    comment_body = render('templates/comment.pt', request=request, value={
        'comment': comment,
        'comment_date': format_datetime(comment.creation_date),
        'comment_age': get_age(comment.creation_date, request=request),
        'profile': profile
    })
    return {
        'status': 'success',
        'callbacks': [{
            'callback': 'MyAMS.helpers.addElementToParent',
            'options': {
                'element': comment_body,
                'parent': '#review-messages',
                'scrollTo': True,
                'scrollParent': '#review-messages-view'
            },
        }],
        'events': [{
            'event': 'update-comments.ams.content',
            'options': {
                'count': len(comments)
            }
        }]
    }


@view_config(name='get-comments.json',
             context=IReviewTarget, request_type=IPyAMSLayer,
             renderer='json',
             permission=COMMENT_CONTENT_PERMISSION)
def get_review_comments(request):
    """Review comments getter"""
    count = int(request.params.get('count', 0))
    comments = IReviewComments(request.context)
    if len(comments) <= count:
        return {
            'status': 'success',
            'count': count
        }
    result = []
    for index, comment in enumerate(comments.values()):
        if index < count:
            continue
        principal = get_principal(request, principal_id=comment.owner)
        result.append(render('templates/comment.pt', request=request, value={
            'comment': comment,
            'comment_date': format_datetime(comment.creation_date),
            'comment_age': get_age(comment.creation_date, request=request),
            'profile': IUserProfile(principal)
        }))
    return {
        'status': 'success',
        'comments': result,
        'count': len(comments)
    }
