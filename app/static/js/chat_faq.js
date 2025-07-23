document.getElementById('send-btn').onclick = function() {
    const input = document.getElementById('user-input');
    const message = input.value.trim();
    if (!message) return;

    fetch('/faq/faq-help', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({message: message})
    })
    .then(response => response.json())
    .then(data => {
        const chatHistory = document.getElementById('chat-history');

        const noMessageElem = document.getElementById('no-message');
        if (noMessageElem) {
            noMessageElem.remove();
        }

        chatHistory.innerHTML += `
            <div class="d-flex justify-content-end">
                <div class="alert alert-primary" style="max-width:70%;">${message}</div>
            </div>
        `;
        chatHistory.innerHTML += `
            <div class="d-flex justify-content-start">
                <div class="alert alert-secondary" style="max-width:70%;">${data.answer}</div>
            </div>
        `;

        input.value = '';
        chatHistory.scrollTop = chatHistory.scrollHeight;
    });
};

document.getElementById('reset-btn').onclick = function() {
    fetch('/faq/faq-reset', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'}
    })
    .then(response => response.json())
    .then(data => {
        if(data.status == 'success') {
            document.getElementById('chat-history').innerHTML = '<div id="no-message" class="text-muted">メッセージはまだありません。</div>';
        }
    });
};