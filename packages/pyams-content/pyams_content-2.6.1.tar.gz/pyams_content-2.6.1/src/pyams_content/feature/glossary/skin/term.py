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

"""PyAMS_content.feature.glossary.skin.term module

This module provides custom glossary terms renderers.
"""

__docformat__ = 'restructuredtext'

from zope.interface import Interface

from pyams_content.component.illustration import IIllustration
from pyams_content.feature.glossary.skin import IThesaurusTermRenderer
from pyams_i18n.interfaces import II18n
from pyams_layer.interfaces import IPyAMSUserLayer
from pyams_template.template import template_config
from pyams_thesaurus.extension.html import IThesaurusTermHTMLInfo
from pyams_thesaurus.interfaces.term import IThesaurusTerm
from pyams_utils.adapter import adapter_config
from pyams_viewlet.viewlet import ViewContentProvider


@adapter_config(name='header',
                required=(IThesaurusTerm, IPyAMSUserLayer, Interface),
                provides=IThesaurusTermRenderer)
@template_config(template='templates/term-header.pt',
                 layer=IPyAMSUserLayer)
class ThesaurusTermHeaderRenderer(ViewContentProvider):
    """Thesaurus term header renderer"""

    weight = 5


@adapter_config(name='illustration',
                required=(IThesaurusTerm, IPyAMSUserLayer, Interface),
                provides=IThesaurusTermRenderer)
@template_config(template='templates/term-illustration.pt',
                 layer=IPyAMSUserLayer)
class ThesaurusTermIllustrationRenderer(ViewContentProvider):
    """Thesaurus term illustration renderer"""

    weight = 10

    illustration = None

    def update(self):
        super().update()
        self.illustration = IIllustration(self.context, None)

    def render(self, template_name=''):
        if not (self.illustration and self.illustration.data):
            return ''
        return super().render(template_name)


@adapter_config(name='body',
                required=(IThesaurusTerm, IPyAMSUserLayer, Interface),
                provides=IThesaurusTermRenderer)
@template_config(template='templates/term-body.pt',
                 layer=IPyAMSUserLayer)
class ThesaurusTermBodyRenderer(ViewContentProvider):
    """Thesaurus term body renderer"""

    weight = 20

    body = None

    def update(self):
        super().update()
        info = IThesaurusTermHTMLInfo(self.context, None)
        if info is not None:
            self.body = II18n(info).query_attribute('description', request=self.request)


@adapter_config(name='associations',
                required=(IThesaurusTerm, IPyAMSUserLayer, Interface),
                provides=IThesaurusTermRenderer)
@template_config(template='templates/term-associations.pt',
                 layer=IPyAMSUserLayer)
class ThesaurusTermAssociationsRenderer(ViewContentProvider):
    """Thesaurus term associations renderer"""

    weight = 50


@adapter_config(name='footer',
                required=(IThesaurusTerm, IPyAMSUserLayer, Interface),
                provides=IThesaurusTermRenderer)
@template_config(template='templates/term-footer.pt',
                 layer=IPyAMSUserLayer)
class ThesaurusTermFooterRenderer(ViewContentProvider):
    """Thesaurus term footer renderer"""

    weight = 90
