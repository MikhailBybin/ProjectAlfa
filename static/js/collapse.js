const toggleButtons = document.querySelectorAll('.toggleButton');

toggleButtons.forEach((button) => {
    button.addEventListener('click', () => {
        const article = button.nextElementSibling; // Получаем следующий элемент после кнопки
        article.classList.toggle('collapsed');
    });
});




