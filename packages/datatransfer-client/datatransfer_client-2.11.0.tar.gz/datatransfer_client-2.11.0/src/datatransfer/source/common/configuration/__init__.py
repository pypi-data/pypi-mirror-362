# coding: utf-8


from __future__ import absolute_import


class ProductConfiguration(object):

    u"""Класс конфигурации."""

    known_attrs = (
        'log_model',
        'client_class',
        'task_class',
        'kte_extractor_mapping_rules',
        'dt_extractor_mapping_rules',
        'get_data_mapping_rules',
        'get_privilege_mapping_rules',
        'person_models',
        'document_models',
        'userprofile_models',
        'project_models_class',
        'feedback_pack_permissions',
        'kte_pack_permissions',
        'kte_organization_select_pack',
        'current_unit_function',
        'get_data_extensions',
        'get_data_config',
        'smev_mnemonics',
        'smev_name',
        'smev_pem',
        'smev_private_key_password',
        'enroll_get_data_mapping_rules',
    )

    active = False

    def __getattr__(self, name):
        # fixme: убрать "active" после отказа от yadic
        if name != 'active' and name not in self.__dict__:
            raise AttributeError("Parameter {} is not set".format(name))
        return super(ProductConfiguration, self).__getattribute__(name)

    def __setattr__(self, name, value):
        assert name in self.known_attrs, (
            'Parameter {} is not registered'.format(name)
        )
        # fixme: убрать "active" после отказа от yadic
        super(ProductConfiguration, self).__setattr__('active', True)
        super(ProductConfiguration, self).__setattr__(name, value)


product_configuration = ProductConfiguration()


# todo: удалить после переноса конфигурации в проекты (deprecated)
# ----------------------------------------------------------------------------
# Изменен способ кастомизации datatransfer-client
# Теперь необходимо объявлять пути к объектам РИС в самой РИС
# в виде обычного словаря.
from django.conf import settings

if hasattr(settings, 'SYSTEM_NAME'):
    from yadic import Container
    from datatransfer.source.common.configuration.configuration import (
        ioc_config
    )

    container = Container(ioc_config)
# ----------------------------------------------------------------------------


def get_object(name):
    u"""Возвращает требуемый объект, используя конфигурацию РИС.

    :param string name: Имя объекта из РИС.
    :return: Объект из РИС.
    """
    if product_configuration.active:
        try:
            return getattr(product_configuration, name)
        except AttributeError:
            # если именно этот параметр отсутствует в product_configuration, то fallback на следующий вариант
            pass
    if hasattr(settings, 'SYSTEM_NAME'):
        return container.get(name, settings.SYSTEM_NAME)
    raise AssertionError("Datatransfer-client is not configured")
