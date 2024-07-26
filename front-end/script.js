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

function showIndicator() {
    const indicatorContent = document.getElementsByClassName('repo-indicator-container')[0];
    const indicatorButton = document.getElementById('showIndicatorButton');
    const indicatorCloseButton = document.getElementById('repo-indicator-close');

    indicatorCloseButton.style.display = 'block';
    indicatorContent.style.display = 'block';
    indicatorButton.style.display = 'none';
}

function closeIndicator() {
    const indicatorContent = document.getElementsByClassName('repo-indicator-container')[0];
    const indicatorButton = document.getElementById('showIndicatorButton');
    const indicatorCloseButton = document.getElementById('repo-indicator-close');

    indicatorCloseButton.style.display = 'none';
    indicatorContent.style.display = 'none';
    indicatorButton.style.display = 'block';
}


document.getElementById('repo-indicator-close').addEventListener('click', closeIndicator);
document.getElementById('showChatButton').addEventListener('click', showChat);
document.getElementById('closeChatButton').addEventListener('click', closeChat);
document.getElementById('showIndicatorButton').addEventListener('click', showIndicator);

window.sendMessage = sendMessage;
