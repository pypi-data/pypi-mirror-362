# coding: utf-8


def connect_plugin(settings, plugin_settings=None):
    u"""Данная функция необходима для работы плагина в ЭДО."""
    settings['INSTALLED_APPS'].append(
        __package__ + '.apps.FeedBackAppConfig'
    )
