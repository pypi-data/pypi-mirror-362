
var loadGrid = Ext.getCmp("{{ component.grid.client_id }}"),
    fromDateField = Ext.getCmp("{{ component.from_date.client_id }}"),
    toDateField = Ext.getCmp("{{ component.to_date.client_id }}");


fromDateField.on("change", DateChangeHandler);
toDateField.on("change", DateChangeHandler);


function DateChangeHandler(field, nValue, oValue){

    if (nValue !== oValue && field.isValid()){
        loadGrid.getStore().baseParams[field.name] = nValue;
        loadGrid.getStore().load();
    }
}


function viewWindow(){

    if (!loadGrid.getSelectionModel().getSelected()){
        Ext.Msg.show({
            title: "Внимание",
            msg: "Необходимо выбрать одну запись",
            buttons: Ext.Msg.OK
        });
        return;
    }

    var mask = new Ext.LoadMask(win.body);
    mask.show();

    Ext.Ajax.request({
        url: "{{ component.view_window_url }}",
        params: {
            feedback: loadGrid.getSelectionModel().getSelected().id
        },
        success: function(response, options){
            var viewWin = smart_eval(response.responseText);
            viewWin.show();
            mask.hide();
        },
        failure: function(response, options){
            uiAjaxFailMessage.apply(win, arguments);
            mask.hide();
        }
    });
}
