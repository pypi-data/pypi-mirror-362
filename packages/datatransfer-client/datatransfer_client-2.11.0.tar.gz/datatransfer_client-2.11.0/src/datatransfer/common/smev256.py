# coding: utf-8

from __future__ import absolute_import

from spyne_smev.smev256 import Smev256 as _Smev256


class Smev256(_Smev256):
    """Переопределение класса протокол Smev256.
    """

    def __init__(self, *args, **kwargs):
        super(Smev256, self).__init__(*args, **kwargs)

        # Разрешаем парсить большие XML.
        self.parser_kwargs['huge_tree'] = True
