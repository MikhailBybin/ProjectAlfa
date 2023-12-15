document.addEventListener('DOMContentLoaded', function() {


     var quill = new Quill('#editor', {
        theme: 'snow',
        modules: {
            toolbar: '#toolbar'
        }
    });

    function convertQuillContentForPrism(content) {
        return content.replace(/<pre class="ql-syntax" spellcheck="false">/g, '<pre class="line-numbers language-python"><code class="language-python">').replace(/<\/pre>/g, '</code></pre>');
    }

    document.querySelector('#articleForm').addEventListener('submit', function(e) {
        var quillContent = quill.root.innerHTML;
        var convertedContent = convertQuillContentForPrism(quillContent);
        document.querySelector('#content').value = convertedContent;
    });
});

