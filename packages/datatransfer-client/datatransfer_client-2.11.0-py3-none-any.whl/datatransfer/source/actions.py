# -*- coding: utf-8 -*-

from __future__ import absolute_import

from django.shortcuts import redirect
from m3.actions import OperationResult
from m3_ext.ui.results import ExtUIScriptResult
from objectpack.actions import BasePack, BaseAction

from datatransfer.common.constants import MODE_ALL
from datatransfer.common.constants import MODE_UPDATED
from datatransfer.source.common.configuration import get_object

from . import permissions
from . ui import SelectOrganizationWindow
from .transport.smev.kte.tasks import kte_labs_send_data_task


class SelectOrganizationAction(BaseAction):
    perm_code = 'send'

    def run(self, request, context):
        try:
            org_pack = get_object('kte_organization_select_pack')
        except ValueError:
            org_pack = None

        if org_pack:
            win = SelectOrganizationWindow()
            win.organization_fld.pack = org_pack
            win.form.url = self.parent.send_data_action.absolute_url()
            return ExtUIScriptResult(win)

        return redirect(self.parent.send_data_action.absolute_url())


class SendDataAction(BaseAction):

    perm_code = 'send'

    def context_declaration(self):
        return {
            'organization_id': {'type': 'int_or_none', 'default': None},
            'send_all': {'type': 'boolean', 'default': False},
        }

    def run(self, request, context):

        organization = None if context.send_all else context.organization_id

        kte_labs_send_data_task.apply_async(kwargs={
            'mode': MODE_ALL,
            'organization_id': organization
        })

        return OperationResult(
            message=u'Задача на отправку данных в Контингент '
                    u'КТЕ Лабс успешно поставлена в очередь.'
        )


class SendUpdatedDataAction(BaseAction):

    u"""Экшен отправки измененных данных в КТЕ."""

    perm_code = 'send'

    def run(self, request, context):
        kte_labs_send_data_task.apply_async(kwargs={'mode': MODE_UPDATED})
        return OperationResult(
            message=u'Задача на отправку измененных данных в Контингент '
                    u'КТЕ Лабс успешно поставлена в очередь.'
        )


class ContingentKteLabsPack(BasePack):
    """ Отправляет данные в КТЕ Лабс """

    need_check_permission = True
    sub_permissions = permissions.KTE_PACK_SUB_PERMISSIONS

    def __init__(self):
        super(ContingentKteLabsPack, self).__init__()
        self.send_data_action = SendDataAction()
        self.send_updated_data_action = SendUpdatedDataAction()
        self.select_organization_action = SelectOrganizationAction()
        self.actions.extend([
            self.send_data_action,
            self.send_updated_data_action,
            self.select_organization_action
        ])

    def extend_menu(self, menu):
        return menu.SubMenu(
            u'Администрирование',
            menu.SubMenu(
                u'Интеграция',
                menu.SubMenu(
                    u'Контингент КТЕ Лабс',
                    menu.Item(
                        u'Отправить все данные',
                        self.select_organization_action
                    ),
                    menu.Item(
                        u'Отправить измененные данные',
                        self.send_updated_data_action
                    )
                )
            )
        )
