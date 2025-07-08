document.getElementById('chatForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const messageInput = document.getElementById('message');
    const message = messageInput.value;
    const thread_id = document.getElementById('thread_id').value || '';

    const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({message, thread_id})
    });

    const data = await response.json();
    document.getElementById('thread_id').value = data.thread_id;
    displayMessage('user', message);
    displayMessage('assistant', data.assistant_message);

    messageInput.value = '';
});

function displayMessage(role, content) {
    const chatBox = document.getElementById('chatBox');
    const msgElem = document.createElement('div');
    msgElem.className = role;
    msgElem.textContent = content;
    chatBox.appendChild(msgElem);
}
