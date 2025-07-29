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

"""PyAMS_shared.site.link module

"""

from persistent import Persistent
from zope.container.contained import Contained
from zope.interface import Interface, implementer
from zope.schema.fieldproperty import FieldProperty

from pyams_content.component.illustration import ILinkIllustrationTarget
from pyams_content.component.links import ExternalLink, InternalLink
from pyams_content.feature.navigation.interfaces import IDynamicMenu
from pyams_content.interfaces import MANAGE_CONTENT_PERMISSION
from pyams_content.shared.site.interfaces import IExternalSiteLink, IInternalSiteLink, \
    ISiteElementNavigation, ISiteLink
from pyams_i18n.interfaces import II18n
from pyams_layer.interfaces import IPyAMSLayer
from pyams_security.interfaces import IViewContextPermissionChecker
from pyams_sequence.reference import InternalReferenceMixin, get_reference_target
from pyams_utils.adapter import ContextAdapter, ContextRequestAdapter, adapter_config
from pyams_utils.factory import factory_config
from pyams_utils.interfaces import MISSING_INFO
from pyams_utils.zodb import volatile_property
from pyams_workflow.interfaces import IWorkflow, IWorkflowPublicationInfo, IWorkflowState, \
    IWorkflowVersion, IWorkflowVersions
from pyams_zmi.interfaces import IObjectLabel
from pyams_zmi.utils import get_object_label

__docformat__ = 'restructuredtext'

from pyams_content import _


@implementer(ISiteLink, ILinkIllustrationTarget)
class SiteLink(Persistent, Contained):
    """Site link persistent class"""

    navigation_title = FieldProperty(ISiteLink['navigation_title'])
    show_header = FieldProperty(ISiteLink['show_header'])
    navigation_header = FieldProperty(ISiteLink['navigation_header'])
    visible = FieldProperty(ISiteLink['visible'])

    @staticmethod
    def is_deletable():
        """Link deletion checker"""
        return True


@adapter_config(required=ISiteLink,
                provides=IViewContextPermissionChecker)
class SiteLinkPermissionCheck(ContextAdapter):
    """Site link permission checker"""

    edit_permission = MANAGE_CONTENT_PERMISSION


#
# Internal content link
#

@factory_config(IInternalSiteLink)
class InternalSiteLink(InternalReferenceMixin, SiteLink):
    """Internal site link persistent class

    An 'internal content link' is a link to another content, which may be stored anywhere
    (same site, another site or in any shared tool).
    """

    _reference = FieldProperty(IInternalSiteLink['reference'])
    force_canonical_url = FieldProperty(IInternalSiteLink['force_canonical_url'])

    content_name = _("Internal link")

    @volatile_property
    def target(self):
        """Link target getter"""
        target = get_reference_target(self.reference)
        if IWorkflowVersion.providedBy(target):
            workflow = IWorkflow(target, None)
            if workflow is not None:
                versions = IWorkflowVersions(target).get_versions(workflow.visible_states,
                                                                  sort=True)
                if not versions:
                    versions = IWorkflowVersions(target).get_last_versions()
                if versions:
                    target = versions[-1]
        return target


@adapter_config(required=IInternalSiteLink,
                provides=IDynamicMenu)
def internal_site_link_dynamic_menu(context):
    """Internal site link dynamic menu factory"""
    target = context.get_target()
    if target is not None:
        result = InternalLink()
        result.title = context.navigation_title.copy() if context.navigation_title else {}
        result.reference = context.reference
        result.force_canonical_url = context.force_canonical_url
        return result
    return None


@adapter_config(required=(IInternalSiteLink, IPyAMSLayer),
                provides=ISiteElementNavigation)
class InternalSiteLinkNavigationAdapter(ContextRequestAdapter):
    """Internal site link navigation adapter"""

    @property
    def visible(self):
        """Navigation link visibility getter"""
        if not self.context.visible:
            return False
        target = self.context.target
        return (target is not None) and IWorkflowPublicationInfo(target).is_visible(self.request)


@adapter_config(required=(IInternalSiteLink, IPyAMSLayer, Interface),
                provides=IObjectLabel)
def internal_site_link_label(context, request, view):
    """Internal site link label"""
    label = II18n(context).query_attribute('navigation_title', request=request)
    if not label:
        target = context.get_target()
        if target is not None:
            label = get_object_label(target, request, view)
    return label or MISSING_INFO


@adapter_config(required=IInternalSiteLink,
                provides=IWorkflow)
def internal_site_link_workflow_info(context):
    """Internal site link workflow info"""
    target = context.get_target()
    if target is not None:
        return IWorkflow(target, None)
    return None


@adapter_config(required=IInternalSiteLink,
                provides=IWorkflowState)
def internal_content_link_state_info(context):
    """Internal content link workflow state info"""
    target = context.get_target()
    if target is not None:
        return IWorkflowState(target, None)
    return None


@adapter_config(required=IInternalSiteLink,
                provides=IWorkflowPublicationInfo)
def internal_site_link_publication_info(context):
    """Internal site link publication info"""
    target = context.get_target()
    if target is not None:
        return IWorkflowPublicationInfo(target, None)
    return None


#
# External content link
#

@factory_config(IExternalSiteLink)
class ExternalSiteLink(SiteLink):
    """External site link persistent class"""

    url = FieldProperty(IExternalSiteLink['url'])

    content_name = _("External link")


@adapter_config(required=IExternalSiteLink,
                provides=IDynamicMenu)
def external_site_link_dynamic_menu_factory(context):
    """External content link dynamic menu factory"""
    result = ExternalLink()
    result.title = context.navigation_title.copy() if context.navigation_title else {}
    result.url = context.url
    return result


@adapter_config(required=(IExternalSiteLink, IPyAMSLayer),
                provides=ISiteElementNavigation)
class ExternalSiteLinkNavigationAdapter(ContextRequestAdapter):
    """External site link navigation adapter"""

    @property
    def visible(self):
        """Navigation link visibility getter"""
        return self.context.visible


@adapter_config(required=(IExternalSiteLink, IPyAMSLayer, Interface),
                provides=IObjectLabel)
def external_site_link_label(context, request, view):
    """External site link label"""
    label = II18n(context).query_attribute('navigation_title', request=request)
    return label or context.url
