# -*- coding: utf-8 -*-
from rer.block.iframembed.interfaces import IRerBlockIframembedSettings
from rer.block.iframembed.interfaces import IRerBlockIframembedSettingsControlpanel
from plone.restapi.controlpanels import RegistryConfigletPanel
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


@adapter(Interface, Interface)
@implementer(IRerBlockIframembedSettingsControlpanel)
class RerBlockIframembedSettingsControlpanel(RegistryConfigletPanel):
    schema = IRerBlockIframembedSettings
    configlet_id = "RerBblockIframembedSettings"
    configlet_category_id = "Products"
    schema_prefix = None
