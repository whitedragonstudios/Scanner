// This function will handle cycling news articles
function initNewsCycle(newsArticles) {
    let currentIndex = 0;

    function showNews() {
        const news = newsArticles[currentIndex];
        document.getElementById('news-src').textContent = news.src;
        document.getElementById('news-art').textContent = news.art;
        document.getElementById('news-url').href = news.url;

        // Move to next article, loop back to start
        currentIndex = (currentIndex + 1) % newsArticles.length;
    }

    // Show first article immediately
    showNews();

    // Cycle every 30 seconds
    setInterval(showNews, 30000);
}
