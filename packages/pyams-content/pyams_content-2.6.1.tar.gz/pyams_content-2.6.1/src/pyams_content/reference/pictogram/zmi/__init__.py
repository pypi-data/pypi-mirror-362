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

"""PyAMS_*** module

"""

from pyramid.httpexceptions import HTTPNotFound
from pyramid.renderers import render, render_to_response
from pyramid.response import Response
from pyramid.view import view_config
from zope.interface import Interface

from pyams_content.interfaces import MANAGE_REFERENCE_TABLE_PERMISSION
from pyams_content.reference.pictogram import IPictogram, IPictogramTable
from pyams_content.reference.pictogram.zmi.table import PictogramTableContainerTable
from pyams_form.ajax import ajax_form_config
from pyams_form.field import Fields
from pyams_form.interfaces.form import IAJAXFormRenderer
from pyams_i18n.interfaces import II18n
from pyams_layer.interfaces import IPyAMSLayer
from pyams_security.interfaces.base import VIEW_SYSTEM_PERMISSION
from pyams_skin.interfaces.view import IModalEditForm, IModalPage
from pyams_skin.viewlet.actions import ContextAddAction
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config
from pyams_utils.interfaces.form import NO_VALUE_STRING
from pyams_utils.interfaces.intids import IUniqueID
from pyams_utils.registry import get_utility
from pyams_utils.traversing import get_parent
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.form import AdminModalAddForm, AdminModalEditForm
from pyams_zmi.helper.event import get_json_table_row_add_callback, \
    get_json_table_row_refresh_callback
from pyams_zmi.interfaces import IAdminLayer, TITLE_SPAN
from pyams_zmi.interfaces.form import IFormTitle
from pyams_zmi.interfaces.table import ITableElementEditor
from pyams_zmi.interfaces.viewlet import IToolbarViewletManager
from pyams_zmi.table import TableElementEditor
from pyams_zmi.utils import get_object_label

__docformat__ = 'restructuredtext'

from pyams_content import _


@viewlet_config(name='add-pictogram.menu',
                context=IPictogramTable, layer=IAdminLayer, view=PictogramTableContainerTable,
                manager=IToolbarViewletManager, weight=10,
                permission=MANAGE_REFERENCE_TABLE_PERMISSION)
class PictogramAddAction(ContextAddAction):
    """Pictogram add action"""

    label = _("Add pictogram")
    href = 'add-pictogram.html'


@ajax_form_config(name='add-pictogram.html',
                  context=IPictogramTable, layer=IPyAMSLayer,
                  permission=MANAGE_REFERENCE_TABLE_PERMISSION)
class PictogramAddForm(AdminModalAddForm):
    """Pictogram add form"""

    subtitle = _("New pictogram")
    legend = _("New pictogram properties")
    modal_class = 'modal-xl'

    fields = Fields(IPictogram).omit('__parent__', '__name__')
    content_factory = IPictogram

    def add(self, obj):
        oid = IUniqueID(obj).oid
        self.context[oid] = obj


@adapter_config(required=(IPictogramTable, IAdminLayer, IModalPage),
                provides=IFormTitle)
def pictogram_add_form_title(context, request, view):
    """Pictogram add form title"""
    return get_object_label(context, request, view)


@adapter_config(required=(IPictogramTable, IAdminLayer, PictogramAddForm),
                provides=IAJAXFormRenderer)
class PictogramAddFormAJAXRenderer(ContextRequestViewAdapter):
    """Pictogram add form AJAX renderer"""

    def render(self, changes):
        """AJAX form renderer"""
        if not changes:
            return None
        table = get_parent(self.context, IPictogramTable)
        return {
            'callbacks': [
                get_json_table_row_add_callback(table, self.request,
                                                PictogramTableContainerTable, changes)
            ]
        }


@adapter_config(required=(IPictogram, IAdminLayer, Interface),
                provides=ITableElementEditor)
class PictogramElementEditor(TableElementEditor):
    """Pictogram table element editor"""


@ajax_form_config(name='properties.html',
                  context=IPictogram, layer=IPyAMSLayer,
                  permission=VIEW_SYSTEM_PERMISSION)
class PictogramEditForm(AdminModalEditForm):
    """Pictogram properties edit form"""

    @property
    def subtitle(self):
        translate = self.request.localizer.translate
        return translate(_("Pictogram: {}")).format(
            II18n(self.context).query_attribute('title', request=self.request))

    legend = _("Pictogram properties")
    modal_class = 'modal-xl'

    fields = Fields(IPictogram).omit('__parent__', '__name__')


@adapter_config(required=(IPictogram, IAdminLayer, IModalEditForm),
                provides=IFormTitle)
def pictogram_edit_form_title(context, request, form):
    """Pictogram edit form title"""
    table = get_utility(IPictogramTable)
    return TITLE_SPAN.format(get_object_label(table, request, form))


@adapter_config(required=(IPictogram, IAdminLayer, PictogramEditForm),
                provides=IAJAXFormRenderer)
class PictogramEditFormAJAXRenderer(ContextRequestViewAdapter):
    """Pictogram edit form AJAX renderer"""

    def render(self, changes):
        """AJAX result renderer"""
        if not changes:
            return None
        table = get_parent(self.context, IPictogramTable)
        return {
            'callbacks': [
                get_json_table_row_refresh_callback(table, self.request,
                                                    PictogramTableContainerTable, self.context)
            ]
        }


@view_config(name='get-pictogram-header.html',
             context=IPictogramTable, request_type=IPyAMSLayer,
             permission=VIEW_SYSTEM_PERMISSION)
def get_pictogram_header_view(request):
    """View used to get thumbnail and alternate label associated with a given pictogram"""
    translate = request.localizer.translate
    name = request.params.get('value')
    if (not name) or (name == NO_VALUE_STRING):
        return Response(translate(_("Default header: --")))
    pictogram = request.context.get(name)
    if pictogram is None:
        raise HTTPNotFound()
    return render_to_response('templates/pictogram-header.pt', {
        'context': pictogram
    }, request=request)


def get_pictogram_header(pictogram, request=None):
    """Get thumbnail and alternate label associated with a given pictogram"""
    return render('templates/pictogram-header.pt', {
        'context': pictogram
    }, request=request)
