document.addEventListener('DOMContentLoaded', function() {

    let codeBlocks = document.querySelectorAll('pre > code');

    codeBlocks.forEach(function(block, index) {
        let btn = document.createElement('button');
        btn.className = 'btn-copy';
        btn.innerHTML = '<i class="fa-regular fa-clipboard"></i> Copy code';
        btn.setAttribute('data-clipboard-target', '#codeblock-' + index);
        block.setAttribute('id', 'codeblock-' + index);
        block.parentNode.insertBefore(btn, block);
    });

    let clipboard = new ClipboardJS('.btn-copy');

    clipboard.on('success', function(e) {
        let btn = e.trigger;
        btn.innerHTML = '<i class="fas fa-check"></i> Copied!';

        // Снять выделение
        e.clearSelection();

        // Сброс кнопки через 2 секунды
        setTimeout(function() {
            btn.innerHTML = '<i class="fa-regular fa-clipboard"></i> Copy code';
        }, 2000);
    });
});
