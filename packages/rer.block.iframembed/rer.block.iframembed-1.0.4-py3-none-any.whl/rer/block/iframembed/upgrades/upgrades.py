# -*- coding: utf-8 -*-
import logging


logger = logging.getLogger(__name__)

DEFAULT_PROFILE = "profile-rer.block.iframembed:default"

# standard upgrades #


def update_profile(context, profile, run_dependencies=True):
    context.runImportStepFromProfile(DEFAULT_PROFILE, profile, run_dependencies)


def update_actions(context):
    update_profile(context, "actions")


def update_types(context):
    update_profile(context, "typeinfo")


def update_rolemap(context):
    update_profile(context, "rolemap")


def update_registry(context):
    update_profile(context, "plone.app.registry", run_dependencies=False)


def update_catalog(context):
    update_profile(context, "catalog")


def update_controlpanel(context):
    update_profile(context, "controlpanel")
