$(document).ready(function() {
    if($('textarea#form-widgets-code').length > 0) {
        var editor = ace.edit("editor");
        textarea = $('textarea#form-widgets-code');
        textarea.hide();
        editor.setValue(textarea.val());
        editor.setTheme("ace/theme/monokai");
        editor.getSession().setMode("ace/mode/python");
        editor.commands.addCommand({
            name: 'save',
            bindKey: {win: 'Ctrl-S',  mac: 'Command-S'},
            exec: function(editor) {
                $("#form-buttons-apply").click();
            },
            readOnly: false
        });
        $('#form').submit(function() {
            textarea.val(editor.getValue());
        })
    }
})