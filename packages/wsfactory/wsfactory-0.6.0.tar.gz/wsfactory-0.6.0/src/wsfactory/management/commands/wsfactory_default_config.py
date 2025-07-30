# coding: utf-8
from __future__ import absolute_import

import codecs
import os

from django.core.management import BaseCommand
from lxml import etree

from wsfactory.config import Settings
import wsfactory


class Command(BaseCommand):

    args = "< path >"

    def handle(self, path="./", *args, **options):
        config_path = os.path.join(os.path.dirname(
            wsfactory.__file__), "schema", "base_config.xml")
        schema_location = os.path.abspath(os.path.join(os.path.dirname(
            wsfactory.__file__), "schema", "wsfactory.xsd"))
        el = etree.parse(config_path).getroot()
        el.attrib[
            "{http://www.w3.org/2001/XMLSchema-instance}schemaLocation"
        ] = "".join((
            Settings.NAMESPACE,
            " ",
            "file://", schema_location
        ))
        target_file_name = os.path.join(
            os.path.abspath(path), "wsfactory_config.xml")
        with codecs.open(target_file_name, "w", "utf8") as fd:
            fd.write(etree.tounicode(el, pretty_print=True))

        self.stdout.write("OK!\n")
