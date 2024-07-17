function sendMessage() {
    const userInput = document.getElementById('userInput');
    const message = userInput.value.trim();

    if (message === '') {
        return;
    }

    const messageElement = document.createElement('div');
    messageElement.className = 'chat-message user';
    messageElement.textContent = message;

    const chatMessages = document.getElementById('chatMessages');
    chatMessages.appendChild(messageElement);

    chatMessages.scrollTop = chatMessages.scrollHeight;
    userInput.value = '';
}

function showChat() {
    const chatContainer = document.getElementsByClassName('chat-container')[0];
    const showChatButton = document.getElementById('showChatButton');
    chatContainer.style.display = 'flex';
    showChatButton.style.display = 'none';
}

function closeChat() {
    const chatContainer = document.getElementsByClassName('chat-container')[0];
    const showChatButton = document.getElementById('showChatButton');
    chatContainer.style.display = 'none';
    showChatButton.style.display = 'block';
}


document.getElementById('showChatButton').addEventListener('click', showChat);
document.getElementById('closeChatButton').addEventListener('click', closeChat);
window.sendMessage = sendMessage;

