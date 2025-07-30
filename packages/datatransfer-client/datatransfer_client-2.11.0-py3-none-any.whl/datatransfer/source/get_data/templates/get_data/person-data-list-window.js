
/*  {% comment %}
 *
 *  Доработка грида с колонкой чекбоксов, исправляющая сброс
 *  чекбоксов при переходе на другую страницу в гриде.
 *
 *  {% endcomment %}
 */
var _grid = Ext.getCmp('{{ component.grid.client_id}}');
{% include "get_data/multiselect-page-fix.js" %}

applyMultiSelectFix(_grid);

/* {# Принять изменения из Контингента #} */
function apply_changes() {

    var ids = _grid.getCheckedIdsString();

    if (ids) {
        Ext.Msg.show({
            title: 'Внимание',
            msg: 'Далее будут приняты все изменения по выделенным записям.<br>' +
            'Предварительно необходимо просмотреть все предлагаемые изменения ' +
            'по каждому студенту, изменений может быть больше, чем указано в ' +
            'окне предварительного просмотра. <br><br>Принять изменения из Контингента?',
            width: 400,
            buttons: {'ok': 'Принять изменения', 'cancel': 'Отмена'},
            icon : Ext.MessageBox.QUESTION,
            fn: function (btn){
                if (btn === 'ok'){
                    Ext.Ajax.request({
                        url: '{{ component.apply_url}}',
                        method: 'POST',
                        params: {'persons': ids},
                        success: function (response, options) {
                            win.getEl().unmask();
                            var obj = Ext.util.JSON.decode(response.responseText);
                            if (obj.message) {
                                Ext.Msg.alert('Внимание', obj.message);
                            }
                        }, failure: function (response, options) {
                            win.getEl().unmask();
                            uiAjaxFailMessage(response, options);
                        }
                    })
                }
        }
        });
        var dlg = Ext.MessageBox.getDialog();
        // {# Значок для кнопки "Принять изменения". #}
        dlg.buttons[0].setIconClass('icon-accept');
    } else {
        Ext.Msg.alert('Внимание', 'Элемент не выбран');
    }
}


// {# нумерация строк в гриде #}
function numRenderer(value, metData, record, rowIndex, colIndex, store) {
    var start = 0;
    if (store.lastOptions && store.lastOptions.params) {
        start = store.lastOptions.params.start;
    }
    return start + rowIndex + 1;
}
