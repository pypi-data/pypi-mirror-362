

/* Открывает окно просмотра физ. лиц, данные для которых были приняты в сессии. */
function viewData() {
    var actionUrl = "{{component.view_window_url}}";
    if (actionUrl) {
        Ext.Ajax.request({
            url: "{{ component.view_window_url }}",
            params: {
                session_id: "{{ component.session_id }}"
            },
            success: function(response, options){
                var viewWin = smart_eval(response.responseText);
                viewWin.show();
            },
            failure: function(response, options){
                uiAjaxFailMessage.apply(win, arguments);
            }
        });
    } else {
        Ext.Msg.show({
            title: "Внимание",
            msg: "Просмотр реестра доступен только для последней удачной " +
                 "сессии.",
            buttons: Ext.Msg.OK
        });
    }
}