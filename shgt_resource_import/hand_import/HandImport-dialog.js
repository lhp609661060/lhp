(function (global){
    /* 依赖jquery-ui */

    var dialogId = 0;
    function getDialogId (){
        dialogId ++;
        return dialogId; 
    }

    function Dialog () {
        var self = this;

        self._dialog = $('<div id="hand-import-window-dialog'+getDialogId()+'"></div>');

        self.open = function (){}
        self.close = function (){}
    }

    global.dialog = function (){}

})(handImport);