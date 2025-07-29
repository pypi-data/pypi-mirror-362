#
# Copyright (c) 2015-2024 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_content.feature.qrcode.zmi module

This module defines components which can be used to display QRCodes for
shared contents.
"""

from io import BytesIO

import qrcode
from pyramid.httpexceptions import HTTPNotFound, HTTPPreconditionFailed
from pyramid.interfaces import IView
from pyramid.response import Response
from pyramid.view import view_config
from qrcode.image.pil import PilImage
from qrcode.image.svg import SvgPathImage

from pyams_content.root import ISiteRootInfos
from pyams_content.shared.common import IWfSharedContent
from pyams_form.interfaces.form import IInnerSubForm
from pyams_form.subform import InnerDisplayForm
from pyams_layer.interfaces import IPyAMSLayer
from pyams_pagelet.pagelet import pagelet_config
from pyams_security.interfaces.base import VIEW_SYSTEM_PERMISSION
from pyams_sequence.interfaces import ISequentialIdInfo, ISequentialIdTarget
from pyams_skin.viewlet.actions import ContextAction
from pyams_template.template import template_config
from pyams_utils.adapter import adapter_config
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.form import AdminModalDisplayForm
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.viewlet import IToolbarViewletManager

__docformat__ = 'restructuredtext'

from pyams_content import _


def get_content_url(request, with_oid=False):
    """Get content public URL"""
    sequence = ISequentialIdInfo(request.context, None)
    if sequence is None:
        raise HTTPNotFound()
    infos = ISiteRootInfos(request.root, None)
    if not infos.public_url:
        raise HTTPPreconditionFailed("Public URL must be defined on site root!")
    oid = sequence.get_base_oid().strip()
    url = '{}/+/{}'.format(infos.public_url, oid)
    return (oid, url) if with_oid else url


def get_qrcode_content(request, format='PNG', factory=PilImage):
    """Get QR code content URL"""
    oid, url = get_content_url(request, with_oid=True)
    output = BytesIO()
    qr = qrcode.QRCode()
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(image_factory=factory)
    img.save(output)
    output.seek(0)
    content_type = 'image/svg+xml' if format == 'SVG' else 'image/png'
    response = Response(content_type=content_type)
    if request.params.get('download') is not None:
        response.content_disposition = 'attachment; ' \
                                       'filename="qrcode-{}.{}"'.format(oid, format.lower())
    response.body_file = output
    return response


@view_config(name='qrcode.png',
             context=ISequentialIdTarget, request_type=IPyAMSLayer,
             permission=VIEW_SYSTEM_PERMISSION)
@view_config(name='qrcode.png',
             context=IWfSharedContent, request_type=IPyAMSLayer,
             permission=VIEW_SYSTEM_PERMISSION)
def qrcode_png(request):
    """Content QR code in PNG format"""
    return get_qrcode_content(request, format='PNG', factory=PilImage)


@view_config(name='qrcode.svg',
             context=ISequentialIdTarget, request_type=IPyAMSLayer,
             permission=VIEW_SYSTEM_PERMISSION)
@view_config(name='qrcode.svg',
             context=IWfSharedContent, request_type=IPyAMSLayer,
             permission=VIEW_SYSTEM_PERMISSION)
def qrcode_svg(request):
    """Content QR code in SVG format"""
    return get_qrcode_content(request, format='SVG', factory=SvgPathImage)


#
# QRCodes display view
#

@viewlet_config(name='qrcodes.action',
                context=ISequentialIdTarget, layer=IAdminLayer, view=IView,
                manager=IToolbarViewletManager, weight=7,
                permission=VIEW_SYSTEM_PERMISSION)
@viewlet_config(name='qrcodes.action',
                context=IWfSharedContent, layer=IAdminLayer, view=IView,
                manager=IToolbarViewletManager, weight=7,
                permission=VIEW_SYSTEM_PERMISSION)
class QRCodeAction(ContextAction):
    """QRCode action"""

    css_class = 'btn-sm mx-1'
    icon_class = 'fas fa-qrcode'
    hint = _("QR code")

    href = 'qrcodes.html'
    modal_target = True


@pagelet_config(name='qrcodes.html',
                context=ISequentialIdTarget, layer=IPyAMSLayer,
                permission=VIEW_SYSTEM_PERMISSION)
@pagelet_config(name='qrcodes.html',
                context=IWfSharedContent, layer=IPyAMSLayer,
                permission=VIEW_SYSTEM_PERMISSION)
class QRCodesDisplayForm(AdminModalDisplayForm):
    """QRCodes display form"""

    subtitle = _("Content QR codes")


@adapter_config(name='qrcodes-images',
                context=(ISequentialIdTarget, IAdminLayer, QRCodesDisplayForm),
                provides=IInnerSubForm)
@adapter_config(name='qrcodes-images',
                context=(IWfSharedContent, IAdminLayer, QRCodesDisplayForm),
                provides=IInnerSubForm)
@template_config(template='templates/qrcodes.pt', layer=IAdminLayer)
class QRCodesImagesDisplayForm(InnerDisplayForm):
    """QR codes images display form"""

    @property
    def content_url(self):
        """Content public URL getter"""
        return get_content_url(self.request)
