# coding: utf-8
from __future__ import absolute_import

from functools import wraps
from importlib import import_module
from importlib import reload as importlib_reload
from threading import RLock
import os

from lxml import etree
from lxml import objectify
from six.moves import cStringIO as StringIO
import requests


def load(path):
    mod, obj = path.rsplit('.', 1)
    mod = import_module(mod)
    return getattr(mod, obj)


def reload(path):
    mod, obj = path.rsplit('.', 1)
    mod = import_module(mod)
    mod = importlib_reload(mod)
    return getattr(mod, obj)


_lock = RLock()


def lock(fn):

    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            _lock.acquire()
            result = fn(*args, **kwargs)
        finally:
            _lock.release()
        return result

    return wrapper


def load_xml(xml_path):
    """
    Загружает xml в etree.ElementTree
    """
    if os.path.exists(xml_path):
        xml_io = open(xml_path, 'rb')
    else:
        raise ValueError(xml_path)
    xml = objectify.parse(xml_io)
    xml_io.close()
    return xml


def load_schema(schema_path):
    """
    Загружает схему xsd
    """
    if schema_path.startswith('http://') or schema_path.startswith('https://'):
        response = requests.get(schema_path)
        schema_io = StringIO(response.text)
    elif os.path.exists(schema_path):
        schema_io = open(schema_path, 'rb')
    else:
        raise ValueError(schema_path)
    schema = etree.XMLSchema(file=schema_io)
    schema_io.close()
    return schema


def create_application(
        app_cls, wsgi_cls, name, tns, service,
        in_protocol, out_protocol, max_content_length):

    app = app_cls(
        [service], tns,
        name=name,
        in_protocol=in_protocol,
        out_protocol=out_protocol)
    if max_content_length is not None:
        wsgi_app = wsgi_cls(app, max_content_length=max_content_length)
    else:
        wsgi_app = wsgi_cls(app)

    return wsgi_app


def get_cache(backend):
    from django.core.cache import caches
    from django.core.cache import InvalidCacheBackendError
    try:
        cache = caches[backend]
    except InvalidCacheBackendError:
        cache = caches['default']
    return cache


def cached_to(attr):
    def decorator(fn):
        def wrapper(self, *args, **kwargs):
            retval = getattr(self, attr, None)
            if retval is None:
                retval = fn(self, *args, **kwargs)
                _lock = RLock()
                try:
                    _lock.acquire()
                    setattr(self, attr, retval)
                finally:
                    _lock.release()

            return retval
        return wrapper
    return decorator
