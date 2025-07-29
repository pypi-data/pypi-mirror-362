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

"""PyAMS_content.component.paragraph.settings module

This module defines persistent classes and adapters which are used to handle
paragraphs factory settings.

These settings are used to define which types of paragraphs are allowed in
each content.
"""

__docformat__ = 'restructuredtext'

from persistent import Persistent
from zope.schema.fieldproperty import FieldProperty

from pyams_content.component.paragraph.interfaces import IParagraphFactorySettings, \
    IParagraphFactorySettingsTarget, PARAGRAPH_FACTORY_SETTINGS_KEY
from pyams_utils.adapter import adapter_config, get_annotation_adapter
from pyams_utils.factory import factory_config


@factory_config(IParagraphFactorySettings)
class ParagraphFactorySettings(Persistent):
    """Paragraph factory settings"""

    allowed_paragraphs = FieldProperty(IParagraphFactorySettings['allowed_paragraphs'])
    auto_created_paragraphs = FieldProperty(IParagraphFactorySettings['auto_created_paragraphs'])


@adapter_config(required=IParagraphFactorySettingsTarget,
                provides=IParagraphFactorySettings)
def paragraph_factory_settings_adapter(context):
    """Paragraph factory settings adapter"""
    return get_annotation_adapter(context, PARAGRAPH_FACTORY_SETTINGS_KEY,
                                  IParagraphFactorySettings)
