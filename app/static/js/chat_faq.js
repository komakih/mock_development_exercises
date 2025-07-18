document.getElementById("chat-form").addEventListener("submit", async function(e) {
    e.preventDefault();

    const input = document.getElementById("user-input").value;
    const responseArea = document.getElementById("chat-area");

    try {
        const res = await fetch("/faq/faq-help", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: input })
        });

        const data = await res.json();

        // シンプルに回答を表示
        responseArea.innerHTML += `
            <div class="bot">
                ${data.answer}
            </div>
        `;

    } catch (error) {
        console.error('Error:', error);
        responseArea.innerHTML += `<div class="bot text-danger">エラーが発生しました。</div>`;
    }
});
