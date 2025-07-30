from plone import api
from plone.dexterity.interfaces import IDexterityContent
from plone.restapi.interfaces import IBlockFieldDeserializationTransformer
from rer.block.iframembed.interfaces.settings import IRerBlockIframembedSettings  # noqa
from zExceptions import BadRequest
from zope.component import adapter
from zope.interface import implementer
from zope.publisher.interfaces.browser import IBrowserRequest
from rer.block.iframembed import _

import lxml.html
import os


class DeserializerBase:
    order = 100
    msg = _(
        "invalid_domain_msg",
        default="Unable to save this url. Its domain is blocked by Site Administrator.",
    )

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def is_allowed_url(self, url):
        disabled = os.environ.get("disable_iframe_domains", "False").lower() in (
            "1",
            "true",
        )
        if disabled:
            return True
        valid_domains = api.portal.get_registry_record(
            "available_domains", interface=IRerBlockIframembedSettings
        )
        if not valid_domains:
            return False
        for domain in valid_domains:
            if url.startswith(domain):
                return True
        return False


class IframeBlockDeserializerBase(DeserializerBase):
    block_type = "iframe"

    def __call__(self, block):
        if not self.is_allowed_url(block.get("iframe_href", "")):
            raise BadRequest(api.portal.translate(self.msg))
        return block


class HTMLBlockDeserializerBase(DeserializerBase):
    block_type = "html"

    def __call__(self, block):
        portal_transforms = api.portal.get_tool(name="portal_transforms")
        html_text = block.get("html", "")

        doc = lxml.html.fromstring(html_text)
        if doc.xpath("//iframe"):
            url_to_embed = doc.xpath("//iframe")[0].attrib.get("src")

            if not url_to_embed:
                msg = "Occorre fornire un url associato all'iframe"
                raise BadRequest(msg)
            if not self.is_allowed_url(url=url_to_embed):
                raise BadRequest(api.portal.translate(self.msg))

        data = portal_transforms.convertTo(
            "text/x-html-safe", html_text, mimetype="text/html"
        )

        block["html"] = data.getData()

        return block


@adapter(IDexterityContent, IBrowserRequest)
@implementer(IBlockFieldDeserializationTransformer)
class HTMLBlockDeserializerContent(HTMLBlockDeserializerBase):
    """Deserializer for content-types"""


@adapter(IDexterityContent, IBrowserRequest)
@implementer(IBlockFieldDeserializationTransformer)
class IframeBlockDeserializerContent(IframeBlockDeserializerBase):
    """Deserializer for content-types"""
