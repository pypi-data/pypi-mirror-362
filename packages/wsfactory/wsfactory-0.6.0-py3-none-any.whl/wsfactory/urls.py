# coding: utf-8
from __future__ import (
    absolute_import,
)

from django.urls import (
    re_path,
)

from .config import (
    get_url_patterns,
)
from .views import (
    api_list,
    handle_api_call,
)


urlpatterns = [
    re_path(r'^wsfactory/api$', api_list),
    re_path(r'^wsfactory/api/(?P<service>[\w\-]+)(/\w*)?$', handle_api_call),
] + get_url_patterns()
