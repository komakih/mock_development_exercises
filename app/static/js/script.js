function scrollToBottom() {
    const chatContainer = document.getElementById('chat-container');
    if (chatContainer) {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
    const inputField = document.querySelector('input[name="message"]');
    if (inputField) {
        inputField.value = ''; // ←ここで明示的にフォーム値を空にしておく
    }
}

// ページ読み込み時に自動でスクロールを実行
document.addEventListener('DOMContentLoaded', scrollToBottom);
