document.addEventListener('DOMContentLoaded', function() {
    var articlePreviews = document.querySelectorAll('.article-preview');
    articlePreviews.forEach(function(preview) {
        var content = preview.textContent;
        if (content.length > 500) {
            preview.textContent = content.substring(0, 500) + '...';
        }
    });
});
