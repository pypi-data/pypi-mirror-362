# -*- coding: utf-8 -*-

from __future__ import absolute_import

from datatransfer.source.common.configuration import get_object


KTE_LABS_SEND_DATA_PERM = "send"

PERM_KTE_LABS = {
    "label": u"Контингент КТЕ Лабс",
    "items": [
        (KTE_LABS_SEND_DATA_PERM, u"Отправка данных в Контингент КТЕ Лабс")
    ]
}


KTE_SUB_PERMISSIONS = {
    'send': KTE_LABS_SEND_DATA_PERM
}
WEB_EDU_KTE_SUB_PERMISSIONS = {}

KTE_PACK_SUB_PERMISSIONS = get_object("kte_pack_permissions")
