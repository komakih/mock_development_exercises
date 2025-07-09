// 既存コードのフォーム送信イベント（追記済み）
document.getElementById('chatForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const messageInput = document.getElementById('message');
    const message = messageInput.value;
    let thread_id = document.getElementById('thread_id').value || '';

    displayMessage('user', message);
    thread_id = await saveMessage(thread_id, 'user', message);
    document.getElementById('thread_id').value = thread_id;

    const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({message, thread_id})
    });
    const data = await response.json();

    displayMessage('assistant', data.assistant_message);
    await saveMessage(thread_id, 'bot', data.assistant_message);

    messageInput.value = '';
});

// メッセージ表示（既存コード）
function displayMessage(role, content) {
    const chatBox = document.getElementById('chatBox');
    const msgElem = document.createElement('div');
    msgElem.className = role;
    msgElem.textContent = content;
    chatBox.appendChild(msgElem);
}

// 以下、新規追加コード（履歴保存と履歴ロード機能）
async function saveMessage(thread_id, sender, content) {
    const response = await fetch('/save_message', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({thread_id, sender, content})
    });

    const data = await response.json();
    return data.thread_id;
}

async function loadHistory(thread_id) {
    const response = await fetch(`/history/${thread_id}`);
    const data = await response.json();
    const chatBox = document.getElementById('chatBox');
    chatBox.innerHTML = '';
    data.messages.forEach(msg => {
        displayMessage(msg.sender, msg.message);
    });
    document.getElementById('thread_id').value = thread_id;
}
