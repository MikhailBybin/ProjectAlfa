tinymce.init({
    selector: 'textarea',
    external_plugins: {
        codemirror: "{{ url_for('static', filename='tinymice/plugins/codemirror/plugin.js') }}"
    },
    toolbar: 'undo redo | code',
    codemirror: {
        indentOnInit: true,
        path: "{{ url_for('static', filename='tinymice/plugins/codemirror/codemirror-4.8/lib/') }}"
    }
});
