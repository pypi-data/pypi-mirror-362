var organizationFld = Ext.getCmp('{{ component.organization_fld.client_id }}'),
    sendAll = Ext.getCmp('{{ component.send_all.client_id }}'),
    cancelBtn = Ext.getCmp('{{ component.cancel_btn.client_id }}');

sendAll.on('check', onChBoxChange);

function onChBoxChange(cmp, checked) {
    organizationFld.clearValue();
    organizationFld.setReadOnly(checked);
    organizationFld.allowBlank = checked;
    organizationFld.validate();
};

cancelBtn.handler = function() {
    win.close(true);
};
