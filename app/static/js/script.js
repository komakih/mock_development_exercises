function scrollToBottom() {
    const chatContainer = document.getElementById('chat-container');
    if (chatContainer) {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
}

// ページ読み込み時に自動でスクロールを実行
document.addEventListener('DOMContentLoaded', scrollToBottom);
