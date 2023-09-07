let codeMirrorInstance;
let currentCodeBlock;

function openModal() {
    document.getElementById('codeModal').style.display = 'block';
    // Инициализация CodeMirror, если еще не был инициализирован
    if (!codeMirrorInstance) {
        codeMirrorInstance = CodeMirror.fromTextArea(document.getElementById('codeArea'), {
            lineNumbers: true
        });
    }
    codeMirrorInstance.refresh();
}

function closeModal() {
    document.getElementById('codeModal').style.display = 'none';
}

function insertCodeToTinyMCE() {
    const editor = tinymce.activeEditor;
    const selectedLanguage = document.getElementById('languageSelector').value;
    const codeContent = codeMirrorInstance.getValue().trim();
    if (currentCodeBlock) {
        currentCodeBlock.innerHTML = `<code class="language-${selectedLanguage}">${codeContent}</code>`;
    } else {
        editor.insertContent(`<pre class="line-numbers"><code class="language-${selectedLanguage}">${codeContent}</code></pre>`);
    }
    closeModal();
}

tinymce.init({
    selector: '#content',
    language: 'ru',
    plugins: 'code',
    toolbar: 'code insertCode',
    setup: function (editor) {
        editor.ui.registry.addButton('insertCode', {
            text: 'Вставить код',
            onAction: function() {
                currentCodeBlock = null; // Сброс текущего блока кода
                openModal();
            }
        });

        editor.on('dblclick', function (event) {
            if (event.target.tagName === 'CODE') {
                currentCodeBlock = event.target;
                codeMirrorInstance.setValue(currentCodeBlock.textContent || currentCodeBlock.innerText);
                openModal();
            }
        });
    }
});
