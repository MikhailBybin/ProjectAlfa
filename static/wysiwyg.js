tinymce.init({
    selector: 'textarea',
    external_plugins: {
        codemirror: '/static/tinymice/plugins/codemirror/plugin.js'
    },
    toolbar: 'undo redo | code',
    codemirror: {
        indentOnInit: true,
        path: '/static/tinymice/plugins/codemirror/codemirror-4.8'
    }
});
