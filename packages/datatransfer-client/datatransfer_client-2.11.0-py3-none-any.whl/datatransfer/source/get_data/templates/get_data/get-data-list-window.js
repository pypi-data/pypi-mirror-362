
var loadGrid = Ext.getCmp("{{ component.grid.client_id }}"),
    fromDateField = Ext.getCmp("{{ component.from_date.client_id }}"),
    toDateField = Ext.getCmp("{{ component.to_date.client_id }}");


fromDateField.on("change", DateChangeHandler);
fromDateField.on("select", DateChangeHandler);
toDateField.on("change", DateChangeHandler);
toDateField.on("select", DateChangeHandler);

loadGrid.on("rowdblclick", viewWindow);


function DateChangeHandler(field, nValue, oValue){

    if (nValue !== oValue){
        loadGrid.getStore().baseParams[field.name] = nValue;
        loadGrid.getStore().load();
    }
}


/* {# Открывает окно просмотра протокола для сессии #} */
function viewWindow(){

    if (!loadGrid.getSelectionModel().getSelected()){
        Ext.Msg.show({
            title: "Внимание",
            msg: "Элемент не выбран",
            buttons: Ext.Msg.OK
        });
        return;
    } else if (loadGrid.getSelectionModel().getCount() > 1) {
        Ext.Msg.show({
            title: "Внимание",
            msg: "Необходимо выбрать один элемент",
            buttons: Ext.Msg.OK
        });
        return;
    }

    var mask = new Ext.LoadMask(win.body);
    mask.show();

    Ext.Ajax.request({
        url: "{{ component.view_window_url }}",
        params: {
            session_id: loadGrid.getSelectionModel().getSelected().id
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
