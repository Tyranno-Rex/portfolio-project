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

    // send 버튼을 일시적으로 비활성화
    document.getElementById('sendButton').disabled = true;
    var question_key = localStorage.getItem('chatbotPassword');
    console.log('question_key : ', question_key);
    fetch('https://jeongeunseong.store/openai/api/send_question/', { // local server
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: message, question_key: question_key}),
    })
    .then((response) => response.json())
    .then((data) => {
        const messageElement = document.createElement('div');
        messageElement.className = 'chat-message bot';
        messageElement.textContent = data.answer;
        console.log(data.answer);
        chatMessages.appendChild(messageElement);
    });

    document.getElementById('sendButton').disabled = false;
    chatMessages.scrollTop = chatMessages.scrollHeight;
    userInput.value = '';
}

function showChat() {
    const ModalContent = `'
        <div class="detail-title">Chatbot</div>
        <div class="detail-description">
        This is a chatbot that can help you with your questions. 
        But, I'm a poor Guy, So set a password for Chatbot.
        Please enter the password to chat with me. <br>
        </div>
        <br><br>
        <input type="password" id="password" placeholder="Enter Password">
        <button onclick="checkPassword_Click()">Enter</button>
    `;
    document.getElementById('modal-content').innerHTML = ModalContent;
    myModal.open('#myModal');
}

function savePasswordToLocalStorage() {
    const password = document.getElementById('password').value;
    localStorage.setItem('chatbotPassword', password);
    console.log(localStorage.getItem('chatbotPassword'));
}

function checkPassword_Click() {
    console.log('password : ', document.getElementById('password').value);
    fetch('https://jeongeunseong.store/openai/check/password/', { // local server
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ password: document.getElementById('password').value}),
    })
    .then((response) => response.json())
    .then((data) => {
        if (data.data === 'Password is correct') {
            savePasswordToLocalStorage();
            myModal.close('#myModal');
            const chatContainer = document.getElementsByClassName('chat-container')[0];
            const showChatButton = document.getElementById('showChatButton');
            chatContainer.style.display = 'flex';
            showChatButton.style.display = 'none';
        } else {
            alert('Password is incorrect');
        }
    });   
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
window.checkPassword_Click = checkPassword_Click;