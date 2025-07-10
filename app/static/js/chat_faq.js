async function sendMessage() {
    const input = document.getElementById("user-input").value;
    const responseArea = document.getElementById("chat-area");

    const res = await fetch("/chat_faq", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: input })
    });

    const data = await res.json();

    responseArea.innerHTML += `
        <div class="${data.sources.includes('FAQ') ? 'help' : 'bot'}">
            ${data.assistant_message}
        </div>
    `;
}
