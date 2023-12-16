document.addEventListener('DOMContentLoaded', function() {


    // Инициализация Quill
    var quill = new Quill('#editor', {
        theme: 'snow',
        modules: {
            toolbar: '#toolbar',
            imageResize: {}
        }
    });

    // Инициализация обработчиков событий для кнопок выбора языка
    document.querySelectorAll('.language-btn').forEach(button => {
        button.addEventListener('click', function() {
            // Удаляем класс 'active' у всех кнопок
            document.querySelectorAll('.language-btn').forEach(btn => btn.classList.remove('active'));

            // Добавляем класс 'active' только к нажатой кнопке
            this.classList.add('active');
        });
    });

    // Функция для преобразования содержимого Quill для подсветки синтаксиса Prism
    function convertQuillContentForPrism(content) {
        const activeButton = document.querySelector('.language-btn.active');
        const selectedLanguage = activeButton ? activeButton.getAttribute('data-language') : 'language-python';

        return content.replace(/<pre class="ql-syntax" spellcheck="false">/g, `<pre class="line-numbers ${selectedLanguage}"><code class="${selectedLanguage}">`).replace(/<\/pre>/g, '</code></pre>').replace(/\n<\/code><\/pre>/g, '</code></pre>');
    }

    // Обработчик события отправки формы
    document.querySelector('#articleForm').addEventListener('submit', function(e) {
        var quillContent = quill.root.innerHTML;
        var convertedContent = convertQuillContentForPrism(quillContent);
        document.querySelector('#content').value = convertedContent;
    });
});
