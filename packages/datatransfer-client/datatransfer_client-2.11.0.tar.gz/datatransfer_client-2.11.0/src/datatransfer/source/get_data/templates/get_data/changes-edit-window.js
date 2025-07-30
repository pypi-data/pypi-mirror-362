var _grid = Ext.getCmp('{{ component.grid.client_id}}');
var selectionModel = _grid.getSelectionModel();

function applyChanges() {
    if (selectionModel.hasSelection()) {
        Ext.Msg.confirm(
            'Внимание',
            'Вы действительно хотите принять изменения из Контингента ' +
            'по данному учащемуся/учащимся?<br /><br />' +
            'Данное действие невозможно отменить.',
        function (btn){
            if (btn === 'yes'){
                selections = selectionModel.getSelections();
                ids = selections.map(
                    function(selection){
                        return selection.id;
                    }
                );
                params = {
                    'fields': ids.join(','),
                    'change_id': '{{ component.change_id }}'
                }
                Ext.applyIf(params, win.actionContextJson)
                Ext.Ajax.request({
                    url: '{{ component.apply_url}}',
                    method: 'POST',
                    params: params,
                    success: function (response, options) {
                        win.getEl().unmask();

                        var obj = Ext.util.JSON.decode(response.responseText);
                        if (obj.success) {
                            // {# Удаляем примененные поля из грида. #}
                            selections.forEach(function(row) {
                                    _grid.store.remove(row)
                                }
                            )
                            // {# Костыль для обновления внешнего грида #}
                            win.fireEvent('closed_ok');
                        } else if (obj.message) {
                            Ext.Msg.alert('Внимание', obj.message);
                        }
                    }, failure: function (response, options) {
                        console.log('failure');
                        win.getEl().unmask();
                        uiAjaxFailMessage(response, options);
                    }
                })
            }
        }
        );
    } else {
        Ext.Msg.alert(
            "Внимание", "Элемент не выбран",
            function(){
                win.close();
            }
        );
    }
}

function closeChangesWindow(){
    win.close();
}
