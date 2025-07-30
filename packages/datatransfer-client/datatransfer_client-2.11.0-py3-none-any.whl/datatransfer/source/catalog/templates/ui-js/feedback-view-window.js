
var statisticGrid = Ext.getCmp("{{ component.statistic_grid.client_id }}"),
    statisticSelectionModel = statisticGrid.getSelectionModel(),
    errorsGrid = Ext.getCmp("{{ component.errors_grid.client_id }}"),
    errorsGridColumnModel = errorsGrid.getColumnModel(),
    processedColumn = errorsGridColumnModel.columns[
        errorsGridColumnModel.findColumnIndex("processed")],
    feedBackIDField = Ext.getCmp("{{ component.feedback_hidden_fld.client_id }}");

statisticSelectionModel.on("selectionchange", function(cmp){

    var errorsStore = errorsGrid.getStore(),
        selectedRecord = cmp.getSelected();

    if (selectedRecord){
        errorsStore.baseParams["feedback_statistic"] = selectedRecord.id;
        errorsStore.load();
    }
});

processedColumn.processEvent = function(name, e, grid, rowIndex, colIndex){
    if (name == 'mousedown') {
        var record = grid.store.getAt(rowIndex);
        record.set(this.dataIndex, !record.data[this.dataIndex]);
        Ext.Ajax.request({
            url: "{{ component.error_save_url }}",
            params: {
                record_id: record.id
            },
            failure(response, options){
                record.reject();
            }
        });
        return false;
    } else {
        return Ext.grid.ActionColumn.superclass.processEvent.apply(this, arguments);
    }
}

function detailErrorWindow(){

    if (!errorsGrid.getSelectionModel().getSelected()){
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
        url: "{{ component.error_detail_window_url }}",
        params: {
            detail_id: errorsGrid.getSelectionModel().getSelected().id
        },
        success: function(response, options){
            mask.hide();
            var detailErrorWin = smart_eval(response.responseText);
            detailErrorWin.show();
        },
        failure: function(response, options){
            uiAjaxFailMessage.apply(win, arguments);
            mask.hide();
        }
    });
}

function printReport(){
    Ext.Ajax.request({
        url: "{{ component.report_action }}",
        params: {
            feedback: feedBackIDField.getValue(),
            feedback_statistic_id: statisticSelectionModel.getSelected()?.id
        },
        success: function(response, options){
            smart_eval(response.responseText);
        },
        failure: function(response, options){
            uiAjaxFailMessage.apply(win, arguments);
        }
    });
}

function loadErrors(){
    Ext.Ajax.request({
        url: "{{ component.upload_action }}",
        params: {
            feedback: feedBackIDField.getValue()
        },
        failure: function(response, options){
            uiAjaxFailMessage.apply(win, arguments);
        }
    });
}