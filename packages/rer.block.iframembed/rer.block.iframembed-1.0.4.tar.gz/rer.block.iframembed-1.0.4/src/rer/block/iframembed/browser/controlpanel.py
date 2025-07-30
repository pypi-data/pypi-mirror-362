# -*- coding: utf-8 -*-
from plone.app.registry.browser import controlpanel
from rer.block.iframembed.interfaces import IRerBlockIframembedSettings
from rer.block.iframembed import _


class IRerBlockIframembedForm(controlpanel.RegistryEditForm):

    schema = IRerBlockIframembedSettings
    label = _("rer_block_iframembed_settings_label", default=u"Iframe domain settings")


class RerBlockIframembedSettings(controlpanel.ControlPanelFormWrapper):
    form = IRerBlockIframembedForm
