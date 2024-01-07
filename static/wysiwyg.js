document.addEventListener('DOMContentLoaded', function() {

    var toolbarOptions = [
      ['bold', 'italic', 'underline', 'strike'],        // toggled buttons
      ['blockquote', 'code-block'],
      ['link', 'image'],

      [{ 'list': 'ordered'}, { 'list': 'bullet' }],
      [{ 'script': 'sub'}, { 'script': 'super' }],      // superscript/subscript
      [{ 'indent': '-1'}, { 'indent': '+1' }],          // outdent/indent
      [{ 'direction': 'rtl' }],                         // text direction

      [{ 'size': ['small', false, 'large', 'huge'] }],  // custom dropdown
      [{ 'header': [1, 2, 3, 4, 5, 6, false] }],

      [{ 'color': [] }, { 'background': [] }],          // dropdown with defaults from theme
      [{ 'font': [] }],
      [{ 'align': [] }],

      ['clean']                                         // remove formatting button
    ];

    // Инициализация Quill
    var quill = new Quill('#editor', {
        theme: 'snow',
        modules: {
            syntax: true,
            toolbar: toolbarOptions,
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

    // document.querySelector('#articleForm').addEventListener('submit', function(e) {
    // e.preventDefault(); // Предотвращение стандартной отправки формы
    //
    // var quillHtml = quill.root.innerHTML; // Получение HTML-контента из Quill
    // var convertedForPrism = convertQuillContentForPrism(quillHtml); // Преобразование для Prism
    // var formattedHtml = convertedForPrism.replace(/\n/g, '<br>'); // Замена переносов строк на <br>
    // console.log(formattedHtml); // Вывод в консоль для проверки
    //
    // document.querySelector('#hiddenTextField').value = formattedHtml; // Установка значения скрытого поля
    //
    // this.submit(); // Отправка формы
    // });

});
