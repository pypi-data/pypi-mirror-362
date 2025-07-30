# -*- coding: utf-8 -*-
from rer.block.iframembed import _
from plone.restapi.controlpanels.interfaces import IControlpanel
from zope.interface import Interface
from zope import schema


class IRerBlockIframembedSettings(Interface):
    """Interface for RerBlockIframembed controlpanel"""

    available_domains = schema.Tuple(
        title=_("available_domains", default="Available domains"),
        description=_(
            "available_domains_help",
            default="Insert a list of available domains. One per line.",
        ),
        missing_value=None,
        value_type=schema.TextLine(),
        required=False,
    )


class IRerBlockIframembedSettingsControlpanel(IControlpanel):
    """ """
