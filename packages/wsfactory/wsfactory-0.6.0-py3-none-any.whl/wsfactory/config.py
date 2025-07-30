# coding: utf-8
from __future__ import (
    absolute_import,
)

import hashlib
import logging
import os
from functools import (
    partial,
    wraps,
)

from django.views.decorators.csrf import (
    csrf_exempt,
)
from lxml import (
    etree,
)

from . import (
    _helpers,
)


logger = logging.getLogger(__name__)


VALUE_TYPES = {
    'unicode': str,
    'string': str,
    'int': int,
    'float': float,
    'text': str,
    'password': str,
    'bool': lambda x: x in ('True', 'true', True),
}


def parse_params(params, filter_nullable=False):
    return dict(
        (param.attrib['key'], VALUE_TYPES.get(param.attrib['valueType'])(param.text) if param.text else None)
        for param in params
        if param.text or not filter_nullable
    )


class ImproperlyConfigured(Exception):
    pass


class Settings(object):
    __instance = None

    NAMESPACE = 'http://bars-open.ru/schema/wsfactory'
    DEFAULT_TNS = 'http://bars-open.ru/inf'
    CACHE_KEY = 'wsfactory_config_file_hash'
    SCHEMA = _helpers.load_schema(os.path.join(os.path.dirname(__file__), 'schema', 'wsfactory.xsd'))

    def __new__(cls, *more):
        if not cls.__instance:
            obj = cls.__instance = super(Settings, cls).__new__(cls, *more)

            obj._app_cache = {}
            obj._configured = False
            obj._config_path = None
            obj._hash = None
            obj._api_handler = None
            obj._app_cls = None
            obj._django_cls = None
            obj._document = None

        return cls.__instance

    @classmethod
    def reload(cls):
        if not cls.configured():
            raise ImproperlyConfigured('Not configured yet!')
        config_path = cls.config_path()
        cls.__instance = None
        cls.load(config_path)

    @classmethod
    def validate(cls, xml):
        schema = _helpers.load_schema(os.path.join(os.path.dirname(__file__), 'schema', 'wsfactory.xsd'))
        if not schema.validate(etree.fromstring(etree.tostring(xml))):
            raise ImproperlyConfigured(
                "Config file didn't pass schema validation: %s\n" % '\n'.join(err.message for err in schema.error_log)
            )

    @classmethod
    def load(cls, config_path):
        logger.debug('Load configuration file %s' % config_path)
        cls.__instance = None
        config = cls()
        config._config_path = config_path

        # Читаем настройки

        if not os.path.exists(config_path):
            raise ImproperlyConfigured('Configuration file `%s` does not exist!' % config_path)

        document_tree = _helpers.load_xml(config_path)
        cls.validate(document_tree)

        config._document = document_tree.getroot()

        # Посчитаем хеш-сумму файла конфигурации, и запишем её в кэш django
        with open(config_path, 'rb') as fd:
            config._hash = hashlib.md5(fd.read()).hexdigest()

        cache = _helpers.get_cache('wsfactory')
        cache.set(cls.CACHE_KEY, config._hash)
        config._configured = True

        logger.debug('Configuration file %s successfully loaded' % config_path)

    @classmethod
    def dump(cls, config_path):
        if not cls.configured():
            raise ImproperlyConfigured('Configuration does not loaded yet')
        self = cls()
        cls.validate(self._document)

        logger.debug('Dump configuration file %s' % config_path)
        if not os.access(os.path.exists(config_path) and config_path or os.path.dirname(config_path), os.W_OK):
            raise ImproperlyConfigured('Permission denied `%s`' % config_path)
        # Записываем результат в файл
        with open(config_path, 'w') as fd:
            fd.write(etree.tostring(self._document, pretty_print=True, encoding='utf8'))

        logger.debug('Configuration file %s successfully dumped' % config_path)

    def _create_protocol(self, code, params, security=None):
        proto_el = self._document.Protocols.find('*[@code="{0}"]'.format(code))
        proto_params = parse_params(proto_el.getchildren())
        proto_params.update(params)
        if security:
            security_el = self._document.SecurityProfile.find('*[@code="{0}"]'.format(security))
            security_params = parse_params(security_el.findall('.//{{{0}}}Param'.format(self.NAMESPACE)))
            security_cls = _helpers.load(
                self._document.SecurityProfile.Modules.xpath(
                    '*[@code="{0}"]/@path'.format(security_el.attrib['module'])
                )[0]
            )
            proto_params['wsse_security'] = security_cls(**security_params)
        proto_cls = _helpers.load(proto_el.attrib['module'])
        return proto_cls(**proto_params)

    def _create_app(self, app_name):
        app_el = self._document.Applications.find('*[@name="{0}"]'.format(app_name))
        service_name = app_el.attrib['service']
        service_el = self._document.Services.find('*[@code="{0}"]'.format(service_name))
        api = {}
        service_meta = {}
        for api_id in service_el.xpath('*/@id'):
            method_ = self._document.ApiRegistry.xpath('*[@id="{0}"]'.format(api_id))[0]
            api.update({method_.get('code'): _helpers.reload(method_.get('module'))})

            service_meta.update(
                {
                    method_.get('code'): {
                        'method_verbose_name': method_.get('name'),
                        'protocol': app_el.InProtocol.get('code'),
                    },
                }
            )

        api.update({'METHOD_VERBOSE_NAMES': service_meta})

        service = type(str(service_name), (self.ServiceBase,), dict(api))

        in_protocol, out_protocol = self._create_app_protocols(app_el)

        max_content_length = app_el.get('max_content_length', None)
        if max_content_length:
            max_content_length = int(max_content_length)
        app = _helpers.create_application(
            self.Application,
            self.WsgiApplication,
            app_name,
            app_el.get('tns', self.DEFAULT_TNS),
            service,
            in_protocol,
            out_protocol,
            max_content_length,
        )
        self._app_cache[app_name] = app
        return app

    def _create_app_protocols(self, app_el):
        in_proto_params = dict(list(app_el.InProtocol.items()))
        in_proto_params['params'] = parse_params(app_el.InProtocol.getchildren(), True)
        out_proto_params = dict(list(app_el.OutProtocol.items()))
        out_proto_params['params'] = parse_params(app_el.OutProtocol.getchildren(), True)

        return (self._create_protocol(**in_proto_params), self._create_protocol(**out_proto_params))

    @_helpers.cached_to('__ApplicationClass')
    def __get_app_class(self):
        app_cls_path = self._document.attrib['ApplicationClass']

        from spyne.application import (
            Application,
        )

        app_cls = _helpers.load(app_cls_path)
        if not issubclass(app_cls, Application):
            raise ImproperlyConfigured('{0} is not subclass of spyne Application'.format(app_cls.__name__))
        return app_cls

    Application = property(__get_app_class)

    @_helpers.cached_to('__WsgiClass')
    def __get_wsgi_class(self):
        wsgi_cls_path = self._document.attrib['WsgiClass']
        from spyne.server.django import (
            DjangoApplication,
        )

        wsgi_app_cls = _helpers.load(wsgi_cls_path)
        if not issubclass(wsgi_app_cls, DjangoApplication):
            raise ImproperlyConfigured('{0} is not subclass of spyne DjangoApplication'.format(wsgi_app_cls.__name__))
        return wsgi_app_cls

    WsgiApplication = property(__get_wsgi_class)

    @_helpers.cached_to('__ServiceClass')
    def __get_service_class(self):
        service_cls_path = self._document.attrib['ServiceClass']
        from spyne.service import (
            ServiceBase,
        )

        service_cls = _helpers.load(service_cls_path)
        if not issubclass(service_cls, ServiceBase):
            raise ImproperlyConfigured('{0} is not subclass of spyne ServiceBase'.format(service_cls.__name__))
        return service_cls

    ServiceBase = property(__get_service_class)

    @_helpers.cached_to('__ApiHandler')
    def __get_api_handler(self):
        service_handler_path = self._document.attrib['ApiHandler']
        service_handler = _helpers.load(service_handler_path)
        if not callable(service_handler):
            raise ImproperlyConfigured('`{0}` is not callable'.format(service_handler_path))
        return service_handler

    ApiHandler = property(__get_api_handler)

    @classmethod
    def get_service_handler(cls, service_name):
        self = cls()
        if service_name not in self._document.Applications.xpath('*/@name'):
            return None
        if service_name in self._app_cache:
            return self._app_cache.get(service_name)
        else:
            app = self._create_app(service_name)
            self._app_cache[service_name] = app
            return app

    @classmethod
    def configured(cls):
        self = cls()
        return self._configured

    @classmethod
    def config_path(cls):
        return cls()._config_path

    @classmethod
    def hash(cls):
        self = cls()
        return self._hash


def track_config(fn):
    from django.conf import (
        settings,
    )

    @wraps(fn)
    def inner(*args, **kwargs):
        if not Settings.configured():
            config_path = getattr(settings, 'WSFACTORY_CONFIG_FILE')
            logger.info('Not configured yet. Load configuration %s' % config_path)
            Settings.load(config_path)
        cache = _helpers.get_cache('wsfactory')
        if Settings.hash() != cache.get(Settings.CACHE_KEY):
            logger.info('Configuration file was changed. Reloading ...')
            Settings.reload()

        return fn(*args, **kwargs)

    return inner


@track_config
def get_url_patterns():
    if not Settings.configured():
        raise ImproperlyConfigured('WSFactory not configured yet!')

    from django.urls import (
        re_path,
    )

    urls = []
    self = Settings()
    with_url = self._document.Applications.findall('*[@url]')

    for app in with_url:
        view = partial(self.ApiHandler, service=app.attrib['name'])
        urls.append(re_path(app.attrib['url'], csrf_exempt(view)))

    return urls
