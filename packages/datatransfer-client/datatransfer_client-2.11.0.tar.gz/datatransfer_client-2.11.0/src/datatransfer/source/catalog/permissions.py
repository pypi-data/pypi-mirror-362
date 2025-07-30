# -*- coding: utf-8 -*-
from __future__ import absolute_import

from datatransfer.source.common.configuration import get_object


VIEW_FEEDBACK_PERM = "feedback_view"

PERM_GROUP_FEEDBACK = {
    "label": u"Выгрузка данных",
    "items": [
        (VIEW_FEEDBACK_PERM, u"Просмотр результатов выгрузки")
    ]
}


TREE_FEEDBACK_GROUP = {
    "label": u"Плагин взаимодействия с ИС",
    "items": [
        PERM_GROUP_FEEDBACK
    ]
}


SCHOOL_SUB_PERMISSIONS = {
    "view": VIEW_FEEDBACK_PERM
}


KINDER_SUB_PERMISSIONS = SCHOOL_SUB_PERMISSIONS
COLLEGE_SUB_PERMISSIONS = SCHOOL_SUB_PERMISSIONS
EXTEDU_SUB_PERMISSIONS = SCHOOL_SUB_PERMISSIONS
GENIUS_SUB_PERMISSIONS = SCHOOL_SUB_PERMISSIONS


PACK_SUB_PERMISSIONS = get_object("feedback_pack_permissions")
