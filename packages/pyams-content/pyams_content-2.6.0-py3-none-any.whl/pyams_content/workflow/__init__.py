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

"""PyAMS_content.workflow main module

This module defines main PyAMS content workflow.
"""

from datetime import datetime, timedelta, timezone

from zope.copy import copy
from zope.interface import implementer
from zope.intid import IIntIds
from zope.location import locate
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from pyams_content.interfaces import CREATE_VERSION_PERMISSION, MANAGER_ROLE, \
    MANAGE_CONTENT_PERMISSION, MANAGE_SITE_ROOT_PERMISSION, OWNER_ROLE, PILOT_ROLE, \
    PUBLISH_CONTENT_PERMISSION, READER_ROLE, WEBMASTER_ROLE
from pyams_content.shared.common.interfaces import DEFAULT_CONTENT_WORKFLOW, IContributorRestrictions, \
    IManagerRestrictions, IWfSharedContentRoles
from pyams_content.workflow.interfaces import IContentWorkflow
from pyams_content.workflow.task import ContentArchivingTask, ContentPublishingTask
from pyams_scheduler.interfaces import IScheduler
from pyams_scheduler.interfaces.task import IDateTaskScheduling, SCHEDULER_TASK_DATE_MODE
from pyams_security.interfaces import IRoleProtectedObject
from pyams_security.interfaces.names import INTERNAL_USER_ID
from pyams_sequence.interfaces import ISequentialIdInfo
from pyams_utils.adapter import ContextAdapter, adapter_config
from pyams_utils.date import format_datetime
from pyams_utils.registry import get_current_registry, get_utility, query_utility, utility_config
from pyams_utils.request import check_request
from pyams_utils.timezone import gmtime
from pyams_workflow.interfaces import AUTOMATIC_TRANSITION, IWorkflow, IWorkflowInfo, \
    IWorkflowPublicationInfo, IWorkflowState, IWorkflowStateLabel, IWorkflowVersions, \
    ObjectClonedEvent, SYSTEM_TRANSITION
from pyams_workflow.workflow import Transition, Workflow

__docformat__ = 'restructuredtext'

from pyams_content import _


#
# Workflow states
#

DRAFT = 'draft'
PROPOSED = 'proposed'
CANCELED = 'canceled'
REFUSED = 'refused'
PRE_PUBLISHED = 'pre-published'
PUBLISHED = 'published'
RETIRING = 'retiring'
RETIRED = 'retired'
ARCHIVING = 'archiving'
ARCHIVED = 'archived'
DELETED = 'deleted'

STATES_IDS = (
    DRAFT,
    PROPOSED,
    CANCELED,
    REFUSED,
    PRE_PUBLISHED,
    PUBLISHED,
    RETIRING,
    RETIRED,
    ARCHIVING,
    ARCHIVED,
    DELETED
)

STATES_LABELS = (
    _("Draft"),
    _("Proposed"),
    _("Canceled"),
    _("Refused"),
    _("Published (waiting)"),
    _("Published"),
    _("Retiring"),
    _("Retired"),
    _("Archiving"),
    _("Archived"),
    _("Deleted")
)

STATES_VOCABULARY = SimpleVocabulary([
    SimpleTerm(STATES_IDS[i], title=t)
    for i, t in enumerate(STATES_LABELS)
])

STATES_HEADERS = {
    DRAFT: _("draft created"),
    PROPOSED: _("publication requested"),
    PRE_PUBLISHED: _("published (waiting)"),
    PUBLISHED: _("published"),
    RETIRING: _("retiring requested"),
    RETIRED: _("retired"),
    ARCHIVING: _("archiving requested"),
    ARCHIVED: _("archived")
}


UPDATE_STATES = (DRAFT, )
'''Default state available to contributors in update mode'''

READONLY_STATES = (RETIRED, ARCHIVING, ARCHIVED, DELETED)
'''Retired and archived contents can't be modified'''

PROTECTED_STATES = (PRE_PUBLISHED, PUBLISHED, RETIRING)
'''Protected states are available to webmasters in update mode'''

MANAGER_STATES = (PROPOSED, )
'''Only managers can update proposed contents (if their restrictions apply)'''

PUBLISHED_STATES = (PRE_PUBLISHED, PUBLISHED, RETIRING)
'''Contents in published states are pre-published, published or waiting for retiring'''

VISIBLE_STATES = (PUBLISHED, RETIRING)
'''Contents in visible states are visible in front-office'''

WAITING_STATES = (PROPOSED, RETIRING, ARCHIVING)
'''Contents in waiting states are waiting for a manager action'''

RETIRED_STATES = (RETIRED, ARCHIVING)

ARCHIVED_STATES = (ARCHIVED, )


#
# Workflow conditions
#

def is_internal_user_id(wf, context):
    """Check if current request principal is internal user ID"""
    request = check_request()
    return request.principal.id == INTERNAL_USER_ID


def can_propose_content(wf, context):
    """Check if a content can be proposed"""
    # can't propose content if another proposed version already exists
    versions = IWorkflowVersions(context)
    if versions.has_version(PROPOSED):
        return False
    request = check_request()
    # grant access to webmaster
    if request.has_permission(MANAGE_SITE_ROOT_PERMISSION, context=context):
        return True
    # grant access to owner, creator and local contributors
    roles = IWfSharedContentRoles(context)
    principal_id = request.principal.id
    if principal_id in {context.creator} | roles.owner | roles.contributors:
        return True
    # grant access to allowed contributors
    restrictions = IContributorRestrictions(context)
    if restrictions and restrictions.can_access(context,
                                                permission=MANAGE_CONTENT_PERMISSION,
                                                request=request):
        return True
    # grant access to local content managers
    if principal_id in roles.managers:
        return True
    # grant access to shared tool managers if restrictions apply
    restrictions = IManagerRestrictions(context)
    return restrictions and restrictions.can_access(context,
                                                    permission=MANAGE_CONTENT_PERMISSION,
                                                    request=request)


def can_backdraft_content(wf, context):
    """Check if content can return to DRAFT state"""
    return IWorkflowPublicationInfo(context).publication_date is None


def can_retire_content(wf, context):
    """Check if already published content can return to RETIRED state"""
    return IWorkflowPublicationInfo(context).publication_date is not None


def can_create_new_version(wf, context):
    """Check if we can create a new version"""
    # can't create new version when previous draft already exists
    versions = IWorkflowVersions(context)
    if (versions.has_version(DRAFT) or
            versions.has_version(PROPOSED) or
            versions.has_version(CANCELED) or
            versions.has_version(REFUSED) or
            versions.has_version(PRE_PUBLISHED)):
        return False
    request = check_request()
    # grant access to webmaster
    if request.has_permission(MANAGE_SITE_ROOT_PERMISSION, context):
        return True
    # grant access to owner, creator and local contributors and managers
    roles = IWfSharedContentRoles(context)
    principal_id = request.principal.id
    if principal_id in {context.creator} | roles.owner | roles.contributors | roles.managers:
        return True
    # grant access to allowed contributors
    restrictions = IContributorRestrictions(context)
    if restrictions and restrictions.can_access(context,
                                                permission=MANAGE_CONTENT_PERMISSION,
                                                request=request):
        return True
    # grant access to shared tool managers if restrictions apply
    restrictions = IManagerRestrictions(context)
    return restrictions and restrictions.can_access(context,
                                                    permission=CREATE_VERSION_PERMISSION,
                                                    request=request)


def can_delete_version(wf, context):
    """Check if we can delete a draft version"""
    request = check_request()
    # grant access to webmaster
    if request.has_permission(MANAGE_SITE_ROOT_PERMISSION, context):
        return True
    # grant access to owner, creator and local contributors and managers
    roles = IWfSharedContentRoles(context)
    principal_id = request.principal.id
    if principal_id in {context.creator} | roles.owner | roles.contributors | roles.managers:
        return True
    # grant access to allowed contributors
    restrictions = IContributorRestrictions(context)
    if restrictions and restrictions.can_access(context,
                                                permission=MANAGE_CONTENT_PERMISSION,
                                                request=request):
        return True
    # grant access to shared tool managers if restrictions apply
    restrictions = IManagerRestrictions(context)
    return restrictions and restrictions.can_access(context,
                                                    permission=MANAGE_CONTENT_PERMISSION,
                                                    request=request)


def can_manage_content(wf, context):
    """Check if a manager can handle content"""
    request = check_request()
    # grant access to webmaster
    if request.has_permission(MANAGE_SITE_ROOT_PERMISSION, context):
        return True
    # local content managers can manage content
    roles = IWfSharedContentRoles(context)
    principal_id = request.principal.id
    if principal_id in roles.managers:
        return True
    # shared tool managers can manage content if restrictions apply
    restrictions = IManagerRestrictions(context)
    return restrictions and restrictions.can_access(context,
                                                    permission=PUBLISH_CONTENT_PERMISSION,
                                                    request=request)


def can_cancel_operation(wf, context):
    """Check if we can cancel a request"""
    request = check_request()
    # grant access to webmaster
    if request.has_permission(MANAGE_SITE_ROOT_PERMISSION, context):
        return True
    principal_id = request.principal.id
    # workflow actor can cancel it's own request
    if principal_id == IWorkflowState(context).state_principal:
        return True
    # owner, creator, contributors and managers can cancel workflow request
    roles = IWfSharedContentRoles(context)
    if principal_id in {context.creator} | roles.owner | roles.contributors | roles.managers:
        return True
    # grant access to allowed contributors
    restrictions = IContributorRestrictions(context)
    if restrictions and restrictions.can_access(context,
                                                permission=MANAGE_CONTENT_PERMISSION,
                                                request=request):
        return True
    # shared tool managers can cancel workflow request if restrictions apply
    restrictions = IManagerRestrictions(context)
    return restrictions and restrictions.can_access(context,
                                                    permission=MANAGE_CONTENT_PERMISSION,
                                                    request=request)


#
# Workflow actions
#

def remove_scheduler_task(context):
    """Remove any scheduler task for this context"""
    scheduler = query_utility(IScheduler)
    if scheduler is not None:
        intids = get_utility(IIntIds)
        context_id = intids.queryId(context)
        task_id = 'workflow::{}'.format(context_id)
        if task_id in scheduler:
            del scheduler[task_id]


def reset_publication_action(wf, context):
    """Refuse version publication"""
    IWorkflowPublicationInfo(context).reset(complete=True)


def prepublish_action(wf, context):
    """Publish content with a future effective publication date

    We create a dedicated publication task which will effectively publish the content
    """
    scheduler = query_utility(IScheduler)
    if scheduler is not None:
        intids = get_utility(IIntIds)
        context_id = intids.queryId(context)
        task_id = f'workflow::{context_id}'
        if task_id in scheduler:
            del scheduler[task_id]
        task = ContentPublishingTask(context_id,
                                     prepublished_to_published.transition_id)
        task.name = f'Planned publication for {ISequentialIdInfo(context).public_oid}'
        task.schedule_mode = SCHEDULER_TASK_DATE_MODE
        pub_info = IWorkflowPublicationInfo(context)
        schedule_info = IDateTaskScheduling(task)
        schedule_info.active = True
        schedule_info.start_date = pub_info.publication_effective_date
        scheduler[task_id] = task


def cancel_prepublish_action(wf, context):
    """Cancel pre-publication"""
    remove_scheduler_task(context)


def publish_action(wf, context):
    """Publish version"""
    request = check_request()
    translate = request.localizer.translate
    now = datetime.now(timezone.utc)
    publication_info = IWorkflowPublicationInfo(context)
    publication_info.publication_date = now
    publication_info.publisher = request.principal.id
    publication_info.apply_first_publication_date()
    version_id = IWorkflowState(context).version_id
    for version in IWorkflowVersions(context).get_versions((PRE_PUBLISHED, PUBLISHED, RETIRING,
                                                            RETIRED, ARCHIVING)):
        if version is not context:
            IWorkflowInfo(version).fire_transition_toward(
                ARCHIVED,
                comment=translate(_("Published version {0}")).format(version_id))
    # check expiration date and create auto-archiving task if needed
    # we compare expiration date with current date to handle the case where content is
    # published automatically at application startup, and we add a small amount of time
    # to be sure that scheduler and indexer processes are started
    if publication_info.publication_expiration_date:
        scheduler = query_utility(IScheduler)
        if scheduler is not None:
            intids = get_utility(IIntIds)
            context_id = intids.queryId(context)
            task_id = 'workflow::{}'.format(context_id)
            if task_id in scheduler:
                del scheduler[task_id]
            task = ContentArchivingTask(context_id)
            task.name = 'Planned archiving for {}'.format(ISequentialIdInfo(context).public_oid)
            task.schedule_mode = SCHEDULER_TASK_DATE_MODE
            pub_info = IWorkflowPublicationInfo(context)
            schedule_info = IDateTaskScheduling(task)
            schedule_info.active = True
            schedule_info.start_date = max(now + timedelta(seconds=10),
                                           pub_info.publication_expiration_date)
            scheduler[task_id] = task


def unpublish_action(wf, context):
    """Remove automatic scheduler task when content is unpublished"""
    remove_scheduler_task(context)


def archive_action(wf, context):
    """Remove readers when a content is archived, and delete any scheduler task"""
    # remove readers
    roles = IWfSharedContentRoles(context, None)
    if roles is not None:
        IRoleProtectedObject(context).revoke_role(READER_ROLE, roles.readers)
    # remove any scheduler task
    remove_scheduler_task(context)


def clone_action(wf, context):
    """Create new version"""
    result = copy(context)
    locate(result, context.__parent__)
    registry = get_current_registry()
    registry.notify(ObjectClonedEvent(result, context))
    return result


def delete_action(wf, context):
    """Delete draft version, and parent if single version"""
    versions = IWorkflowVersions(context)
    versions.remove_version(IWorkflowState(context).version_id)


#
# Workflow transitions
#

init = Transition(transition_id='init',
                  title=_("Initialize"),
                  source=None,
                  destination=DRAFT,
                  history_label=_("Draft creation"))

draft_to_proposed = Transition(transition_id='draft_to_proposed',
                               title=_("Propose publication"),
                               source=DRAFT,
                               destination=PROPOSED,
                               permission=MANAGE_CONTENT_PERMISSION,
                               condition=can_propose_content,
                               menu_icon_class='far fa-fw fa-eye',
                               view_name='wf-propose.html',
                               history_label=_("Publication request"),
                               next_step=_("content managers authorized to take charge of your "
                                           "content are going to be notified of your request."),
                               notify_roles={WEBMASTER_ROLE, PILOT_ROLE, MANAGER_ROLE,
                                             OWNER_ROLE},
                               notify_title=_("Publication request"),
                               notify_message=_("{principal} submitted a publication request "
                                                "for content « {title} »"),
                               order=1)

draft_to_prepublished = Transition(transition_id='draft_to_prepublished',
                                   title=_("Pre-publish content"),
                                   source=DRAFT,
                                   destination=PRE_PUBLISHED,
                                   trigger=SYSTEM_TRANSITION,
                                   action=prepublish_action,
                                   history_label=_("Content pre-published"),
                                   notify_roles={'*'},
                                   notify_title=_("Content publication"),
                                   notify_message=_("{principal} pre-published the content "
                                                    "« {title} »"))

draft_to_published = Transition(transition_id='draft_to_published',
                                title=_("Publish content"),
                                source=DRAFT,
                                destination=PUBLISHED,
                                permission=PUBLISH_CONTENT_PERMISSION,
                                condition=can_manage_content,
                                action=publish_action,
                                prepared_transition=draft_to_prepublished,
                                menu_icon_class='fas fa-fw fa-thumbs-up',
                                view_name='wf-publish.html',
                                show_operator_warning=True,
                                history_label=_("Content published"),
                                notify_roles={'*'},
                                notify_title=_("Content publication"),
                                notify_message=_("{principal} published the content "
                                                 "« {title} »"),
                                order=4)

retired_to_proposed = Transition(transition_id='retired_to_proposed',
                                 title=_("Propose publication"),
                                 source=RETIRED,
                                 destination=PROPOSED,
                                 permission=MANAGE_CONTENT_PERMISSION,
                                 condition=can_propose_content,
                                 menu_icon_class='far fa-fw fa-eye',
                                 view_name='wf-propose.html',
                                 history_label=_("Publication request"),
                                 next_step=_("content managers authorized to take charge of your "
                                             "content are going to be notified of your request."),
                                 notify_roles={WEBMASTER_ROLE, PILOT_ROLE, MANAGER_ROLE,
                                               OWNER_ROLE},
                                 notify_title=_("Publication request"),
                                 notify_message=_("{principal} submitted a publication request "
                                                  "for content « {title} »"),
                                 order=1)

proposed_to_canceled = Transition(transition_id='proposed_to_canceled',
                                  title=_("Cancel publication request"),
                                  source=PROPOSED,
                                  destination=CANCELED,
                                  permission=MANAGE_CONTENT_PERMISSION,
                                  condition=can_cancel_operation,
                                  action=reset_publication_action,
                                  menu_icon_class='fas fa-fw fa-reply',
                                  view_name='wf-cancel-propose.html',
                                  history_label=_("Publication request canceled"),
                                  notify_roles={WEBMASTER_ROLE, PILOT_ROLE, MANAGER_ROLE,
                                                OWNER_ROLE},
                                  notify_title=_("Publication request"),
                                  notify_message=_("{principal} cancelled the publication "
                                                   "request for content « {title} »"),
                                  order=2)

canceled_to_draft = Transition(transition_id='canceled_to_draft',
                               title=_("Reset canceled publication to draft"),
                               source=CANCELED,
                               destination=DRAFT,
                               trigger=AUTOMATIC_TRANSITION,
                               history_label=_("State reset to 'draft' (automatic)"),
                               condition=can_backdraft_content)

canceled_to_retired = Transition(transition_id='canceled_to_retired',
                                 title=_("Reset canceled publication to retired"),
                                 source=CANCELED,
                                 destination=RETIRED,
                                 trigger=AUTOMATIC_TRANSITION,
                                 history_label=_("State reset to 'retired' (automatic)"),
                                 condition=can_retire_content)

proposed_to_refused = Transition(transition_id='proposed_to_refused',
                                 title=_("Refuse publication"),
                                 source=PROPOSED,
                                 destination=REFUSED,
                                 permission=PUBLISH_CONTENT_PERMISSION,
                                 condition=can_manage_content,
                                 action=reset_publication_action,
                                 menu_icon_class='fas fa-fw fa-thumbs-down',
                                 view_name='wf-refuse.html',
                                 history_label=_("Publication refused"),
                                 notify_roles={OWNER_ROLE},
                                 notify_title=_("Publication request"),
                                 notify_message=_("{principal} refused the publication request "
                                                  "for content « {title} »"),
                                 order=3)

refused_to_draft = Transition(transition_id='refused_to_draft',
                              title=_("Reset refused publication to draft"),
                              source=REFUSED,
                              destination=DRAFT,
                              trigger=AUTOMATIC_TRANSITION,
                              history_label=_("State reset to 'draft' (automatic)"),
                              condition=can_backdraft_content)

refused_to_retired = Transition(transition_id='refused_to_retired',
                                title=_("Reset refused publication to retired"),
                                source=REFUSED,
                                destination=RETIRED,
                                trigger=AUTOMATIC_TRANSITION,
                                history_label=_("State reset to 'refused' (automatic)"),
                                condition=can_retire_content)

proposed_to_prepublished = Transition(transition_id='proposed_to_prepublished',
                                      title=_("Pre-publish content"),
                                      source=PROPOSED,
                                      destination=PRE_PUBLISHED,
                                      trigger=SYSTEM_TRANSITION,
                                      action=prepublish_action,
                                      history_label=_("Content pre-published"),
                                      notify_roles={'*'},
                                      notify_title=_("Content publication"),
                                      notify_message=_("{principal} pre-published the content "
                                                       "« {title} »"))

prepublished_to_published = Transition(transition_id='prepublished_to_published',
                                       title=_("Publish content"),
                                       source=PRE_PUBLISHED,
                                       destination=PUBLISHED,
                                       trigger=SYSTEM_TRANSITION,
                                       action=publish_action,
                                       history_label=_("Content published"))

prepublished_to_proposed = Transition(transition_id='prepublished_to_proposed',
                                      title=_("Cancel publication"),
                                      source=PRE_PUBLISHED,
                                      destination=PROPOSED,
                                      permission=MANAGE_CONTENT_PERMISSION,
                                      condition=can_manage_content,
                                      action=cancel_prepublish_action,
                                      menu_icon_class='fas fa-fw fa-reply',
                                      view_name='wf-cancel-publish.html',
                                      history_label=_("Publication canceled"),
                                      notify_roles={WEBMASTER_ROLE, PILOT_ROLE, MANAGER_ROLE,
                                                    OWNER_ROLE},
                                      notify_title=_("Content publication"),
                                      notify_message=_("{principal} cancelled the publication "
                                                       "for content « {title} »"),
                                      order=1)

proposed_to_published = Transition(transition_id='proposed_to_published',
                                   title=_("Publish content"),
                                   source=PROPOSED,
                                   destination=PUBLISHED,
                                   permission=PUBLISH_CONTENT_PERMISSION,
                                   condition=can_manage_content,
                                   action=publish_action,
                                   prepared_transition=proposed_to_prepublished,
                                   menu_icon_class='fas fa-fw fa-thumbs-up',
                                   view_name='wf-publish.html',
                                   show_operator_warning=True,
                                   history_label=_("Content published"),
                                   notify_roles={'*'},
                                   notify_title=_("Content publication"),
                                   notify_message=_("{principal} published the content "
                                                    "« {title} »"),
                                   order=4)

published_to_retiring = Transition(transition_id='published_to_retiring',
                                   title=_("Request retiring"),
                                   source=PUBLISHED,
                                   destination=RETIRING,
                                   permission=MANAGE_CONTENT_PERMISSION,
                                   menu_icon_class='far fa-fw fa-pause-circle',
                                   view_name='wf-retiring.html',
                                   history_label=_("Retire request"),
                                   next_step=_("content managers authorized to take charge of "
                                               "your content are going to be notified of your "
                                               "request."),
                                   notify_roles={WEBMASTER_ROLE, PILOT_ROLE, MANAGER_ROLE,
                                                 OWNER_ROLE},
                                   notify_title=_("Content removal"),
                                   notify_message=_("{principal} submitted a retire request "
                                                    "for content « {title} »"),
                                   order=7)

published_to_retired = Transition(transition_id='published_to_retired',
                                  title=_("Retired content"),
                                  source=PUBLISHED,
                                  destination=RETIRED,
                                  permission=PUBLISH_CONTENT_PERMISSION,
                                  condition=can_manage_content,
                                  action=unpublish_action,
                                  menu_icon_class='far fa-fw fa-stop-circle',
                                  view_name='wf-retire.html',
                                  show_operator_warning=True,
                                  history_label=_("Content retired"),
                                  notify_roles={WEBMASTER_ROLE, PILOT_ROLE, MANAGER_ROLE,
                                                OWNER_ROLE},
                                  notify_title=_("Content removal"),
                                  notify_message=_("{principal} retired content « {title} »"),
                                  order=9)

published_to_retired_by_task = Transition(transition_id='published_to_retired_by_task',
                                          title=_("Retired content"),
                                          source=PUBLISHED,
                                          destination=RETIRED,
                                          trigger=SYSTEM_TRANSITION,
                                          condition=is_internal_user_id,
                                          history_label=_("Content retired after passed expiration date"))

retiring_to_published = Transition(transition_id='retiring_to_published',
                                   title=_("Cancel retiring request"),
                                   source=RETIRING,
                                   destination=PUBLISHED,
                                   permission=MANAGE_CONTENT_PERMISSION,
                                   condition=can_cancel_operation,
                                   menu_icon_class='fas fa-fw fa-reply',
                                   view_name='wf-cancel-retiring.html',
                                   history_label=_("Retire request canceled"),
                                   notify_roles={WEBMASTER_ROLE, PILOT_ROLE, MANAGER_ROLE,
                                                 OWNER_ROLE},
                                   notify_title=_("Content removal"),
                                   notify_message=_("{principal} cancelled the retiring request "
                                                    "for content « {title} »"),
                                   order=8)

retiring_to_retired = Transition(transition_id='retiring_to_retired',
                                 title=_("Retire content"),
                                 source=RETIRING,
                                 destination=RETIRED,
                                 permission=PUBLISH_CONTENT_PERMISSION,
                                 condition=can_manage_content,
                                 action=unpublish_action,
                                 menu_icon_class='far fa-fw fa-stop-circle',
                                 view_name='wf-retire.html',
                                 show_operator_warning=True,
                                 history_label=_("Content retired"),
                                 notify_roles={WEBMASTER_ROLE, PILOT_ROLE, MANAGER_ROLE,
                                               OWNER_ROLE},
                                 notify_title=_("Content removal"),
                                 notify_message=_("{principal} retired content « {title} »"),
                                 order=9)

retired_to_prepublished = Transition(transition_id='retired_to_prepublished',
                                     title=_("Pre-publish retired content"),
                                     source=RETIRED,
                                     destination=PRE_PUBLISHED,
                                     trigger=SYSTEM_TRANSITION,
                                     action=prepublish_action,
                                     history_label=_("Content pre-published"),
                                     notify_roles={'*'},
                                     notify_title=_("Content publication"),
                                     notify_message=_("{principal} pre-published the content "
                                                      "« {title} »"))

retired_to_published = Transition(transition_id='retired_to_published',
                                  title=_("Publish retired content"),
                                  source=RETIRED,
                                  destination=PUBLISHED,
                                  permission=PUBLISH_CONTENT_PERMISSION,
                                  condition=can_manage_content,
                                  action=publish_action,
                                  prepared_transition=retired_to_prepublished,
                                  menu_icon_class='fas fa-fw fa-thumbs-up',
                                  view_name='wf-publish.html',
                                  show_operator_warning=True,
                                  history_label=_("Content published"),
                                  notify_roles={'*'},
                                  notify_title=_("Content publication"),
                                  notify_message=_("{principal} published the content "
                                                   "« {title} »"),
                                  order=4)

retired_to_archiving = Transition(transition_id='retired_to_archiving',
                                  title=_("Request archive"),
                                  source=RETIRED,
                                  destination=ARCHIVING,
                                  permission=MANAGE_CONTENT_PERMISSION,
                                  menu_icon_class='fas fa-fw fa-eye',
                                  view_name='wf-archiving.html',
                                  history_label=_("Archive request"),
                                  next_step=_("content managers authorized to take charge of "
                                              "your content are going to be notified of your "
                                              "request."),
                                  notify_roles={WEBMASTER_ROLE, PILOT_ROLE, MANAGER_ROLE,
                                                OWNER_ROLE},
                                  notify_title=_("Content archiving"),
                                  notify_message=_("{principal} submitted an archive request "
                                                   "for content « {title} »"),
                                  order=10)

retired_to_archived = Transition(transition_id='retired_to_archived',
                                 title=_("Archive content"),
                                 source=RETIRED,
                                 destination=ARCHIVED,
                                 permission=PUBLISH_CONTENT_PERMISSION,
                                 condition=can_manage_content,
                                 action=archive_action,
                                 menu_icon_class='fas fa-fw fa-archive',
                                 view_name='wf-archive.html',
                                 show_operator_warning=True,
                                 history_label=_("Content archived"),
                                 notify_roles={WEBMASTER_ROLE, PILOT_ROLE, MANAGER_ROLE,
                                               OWNER_ROLE},
                                 notify_title=_("Content archiving"),
                                 notify_message=_("{principal} archived content « {title} »"),
                                 order=12)

archiving_to_retired = Transition(transition_id='archiving_to_retired',
                                  title=_("Cancel archiving request"),
                                  source=ARCHIVING,
                                  destination=RETIRED,
                                  permission=MANAGE_CONTENT_PERMISSION,
                                  condition=can_cancel_operation,
                                  menu_icon_class='fas fa-fw fa-reply',
                                  view_name='wf-cancel-archiving.html',
                                  history_label=_("Archive request canceled"),
                                  notify_roles={WEBMASTER_ROLE, PILOT_ROLE, MANAGER_ROLE,
                                                OWNER_ROLE},
                                  notify_title=_("Content archiving"),
                                  notify_message=_("{principal} cancelled the archive request "
                                                   "for content « {title} »"),
                                  order=11)

archiving_to_archived = Transition(transition_id='archiving_to_archived',
                                   title=_("Archive content"),
                                   source=ARCHIVING,
                                   destination=ARCHIVED,
                                   permission=PUBLISH_CONTENT_PERMISSION,
                                   condition=can_manage_content,
                                   action=archive_action,
                                   menu_icon_class='fas fa-fw fa-archive',
                                   view_name='wf-archive.html',
                                   show_operator_warning=True,
                                   history_label=_("Content archived"),
                                   notify_roles={WEBMASTER_ROLE, PILOT_ROLE, MANAGER_ROLE,
                                                 OWNER_ROLE},
                                   notify_title=_("Content archiving"),
                                   notify_message=_("{principal} archived content « {title} »"),
                                   order=12)

published_to_archived_by_version = Transition(transition_id='published_to_archived',
                                              title=_("Archive published content"),
                                              source=PUBLISHED,
                                              destination=ARCHIVED,
                                              trigger=SYSTEM_TRANSITION,
                                              history_label=_("Content archived after version publication"),
                                              action=archive_action)

retiring_to_archived_by_version = Transition(transition_id='retiring_to_archived',
                                             title=_("Archive retiring content"),
                                             source=RETIRING,
                                             destination=ARCHIVED,
                                             trigger=SYSTEM_TRANSITION,
                                             history_label=_("Content archived after version publication"),
                                             action=archive_action)

published_to_draft = Transition(transition_id='published_to_draft',
                                title=_("Create new version"),
                                source=PUBLISHED,
                                destination=DRAFT,
                                permission=CREATE_VERSION_PERMISSION,
                                condition=can_create_new_version,
                                action=clone_action,
                                menu_icon_class='far fa-fw fa-file',
                                menu_divider=True,
                                view_name='wf-clone.html',
                                history_label=_("New version created"),
                                order=13)

retiring_to_draft = Transition(transition_id='retiring_to_draft',
                               title=_("Create new version"),
                               source=RETIRING,
                               destination=DRAFT,
                               permission=CREATE_VERSION_PERMISSION,
                               condition=can_create_new_version,
                               action=clone_action,
                               menu_icon_class='far fa-fw fa-file',
                               menu_divider=True,
                               view_name='wf-clone.html',
                               history_label=_("New version created"),
                               order=14)

retired_to_draft = Transition(transition_id='retired_to_draft',
                              title=_("Create new version"),
                              source=RETIRED,
                              destination=DRAFT,
                              permission=CREATE_VERSION_PERMISSION,
                              condition=can_create_new_version,
                              action=clone_action,
                              menu_icon_class='far fa-fw fa-file',
                              menu_divider=True,
                              view_name='wf-clone.html',
                              history_label=_("New version created"),
                              order=15)

archiving_to_draft = Transition(transition_id='archiving_to_draft',
                                title=_("Create new version"),
                                source=ARCHIVING,
                                destination=DRAFT,
                                permission=CREATE_VERSION_PERMISSION,
                                condition=can_create_new_version,
                                action=clone_action,
                                menu_icon_class='far fa-fw fa-file',
                                menu_divider=True,
                                view_name='wf-clone.html',
                                history_label=_("New version created"),
                                order=16)

archived_to_draft = Transition(transition_id='archived_to_draft',
                               title=_("Create new version"),
                               source=ARCHIVED,
                               destination=DRAFT,
                               permission=CREATE_VERSION_PERMISSION,
                               condition=can_create_new_version,
                               action=clone_action,
                               menu_icon_class='far fa-fw fa-file',
                               menu_divider=True,
                               view_name='wf-clone.html',
                               history_label=_("New version created"),
                               order=17)

delete = Transition(transition_id='delete',
                    title=_("Delete version"),
                    source=DRAFT,
                    destination=DELETED,
                    permission=MANAGE_CONTENT_PERMISSION,
                    condition=can_delete_version,
                    action=delete_action,
                    menu_icon_class='fas fa-fw fa-trash',
                    menu_divider=True,
                    view_name='wf-delete.html',
                    history_label=_("Version deleted"),
                    order=99)

wf_transitions = [
    init,
    draft_to_proposed,
    draft_to_prepublished,
    draft_to_published,
    retired_to_proposed,
    proposed_to_canceled,
    canceled_to_draft,
    canceled_to_retired,
    proposed_to_refused,
    refused_to_draft,
    refused_to_retired,
    proposed_to_prepublished,
    prepublished_to_published,
    prepublished_to_proposed,
    proposed_to_published,
    published_to_retiring,
    published_to_retired,
    published_to_retired_by_task,
    retiring_to_published,
    retiring_to_retired,
    retired_to_archiving,
    archiving_to_retired,
    retired_to_prepublished,
    retired_to_published,
    retired_to_archived,
    archiving_to_archived,
    published_to_archived_by_version,
    retiring_to_archived_by_version,
    published_to_draft,
    retiring_to_draft,
    retired_to_draft,
    archiving_to_draft,
    archived_to_draft,
    delete
]


@implementer(IContentWorkflow)
class ContentWorkflow(Workflow):
    """PyAMS default content workflow"""

    label = _("PyAMS content workflow")


@adapter_config(required=IContentWorkflow,
                provides=IWorkflowStateLabel)
class WorkflowStateLabelAdapter(ContextAdapter):
    """Generic state label adapter"""

    @staticmethod
    def get_label(content, request=None, format=True):
        """Workflow state label getter"""
        if request is None:
            request = check_request()
        translate = request.localizer.translate
        state = IWorkflowState(content)
        header = STATES_HEADERS.get(state.state)
        if header is not None:
            state_label = translate(header)
            if format:
                state_label = translate(_('{state} {date}')).format(
                    state=state_label,
                    date=format_datetime(state.state_date))
        else:
            state_label = translate(_("Unknown state"))
        return state_label


@adapter_config(name=DRAFT,
                required=IContentWorkflow,
                provides=IWorkflowStateLabel)
class DraftWorkflowStateLabelAdapter(ContextAdapter):
    """Draft state label adapter"""

    @staticmethod
    def get_label(content, request=None, format=True):
        """Workflow state label getter"""
        if request is None:
            request = check_request()
        translate = request.localizer.translate
        state = IWorkflowState(content)
        if len(state.history) <= 2:
            header = STATES_HEADERS.get(state.state)
            if header is not None:
                if state.version_id == 1:
                    state_label = translate(header)
                else:
                    state_label = translate(_("new version created"))
            else:
                state_label = translate(_("Unknown state"))
        else:
            history_item = state.history[-1]
            if history_item.source_state == CANCELED:
                state_label = translate(_('publication request cancelled'))
            else:
                state_label = translate(_('publication refused'))
        if format:
            state_label = translate(_('{state} {date}')).format(
                state=state_label,
                date=format_datetime(state.state_date))
        return state_label


wf = ContentWorkflow(wf_transitions,
                     states=STATES_VOCABULARY,
                     initial_state=DRAFT,
                     update_states=UPDATE_STATES,
                     readonly_states=READONLY_STATES,
                     protected_states=PROTECTED_STATES,
                     manager_states=MANAGER_STATES,
                     published_states=PUBLISHED_STATES,
                     visible_states=VISIBLE_STATES,
                     waiting_states=WAITING_STATES,
                     retired_states=RETIRED_STATES,
                     archived_states=ARCHIVED_STATES,
                     auto_retired_state=RETIRED)


@utility_config(name=DEFAULT_CONTENT_WORKFLOW, provides=IWorkflow)
class WorkflowUtility:
    """PyAMS default workflow utility"""

    def __new__(cls):
        return wf
