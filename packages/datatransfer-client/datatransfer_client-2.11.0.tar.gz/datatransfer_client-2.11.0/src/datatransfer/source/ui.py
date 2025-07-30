# coding: utf-8
from __future__ import absolute_import

from m3_ext.ui.fields.complex import ExtDictSelectField
from m3_ext.ui.fields import ExtCheckBox
from objectpack.ui import BaseEditWindow


class SelectOrganizationWindow(BaseEditWindow):

    u"""Окно выбора организации, по которой будут отправлены данные
    в Контингент."""

    def _init_components(self):
        super(SelectOrganizationWindow, self)._init_components()

        self.title = u'Отправка данных'

        self.organization_fld = ExtDictSelectField(
            label=u'Наименование организации',
            name='organization_id',
            anchor='100%',
            hide_edit_trigger=True,
            read_only=True
        )

        self.send_all = ExtCheckBox(
            name='send_all',
            label=u'По всем организациям',
            checked=True
        )

    def _do_layout(self):
        super(SelectOrganizationWindow, self)._do_layout()
        self.form.items.extend((self.send_all, self.organization_fld))
        self.template_globals = 'select-organization-window.js'
        self.save_btn.text = u'Отправить'
        self.height = 150
