# coding: utf-8
from __future__ import absolute_import
from __future__ import print_function

from django.conf import settings
from django.core.management import BaseCommand

from wsfactory.config import Settings


class Command(BaseCommand):

    def handle(self, *args, **options):

        path = getattr(settings, "WSFACTORY_CONFIG_FILE", None)
        if not path:
            print("Config file path does not provided")
        else:
            print("Reloading configuration file %s ..." % path)
            Settings.load(path)
            print("OK!")
