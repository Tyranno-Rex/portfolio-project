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




"use strict";
const leftArrow = document.querySelector(".left-arrow"),
  rightArrow = document.querySelector(".right-arrow"),
  slider = document.querySelector(".slider");

/**
 * @brief Scroll to the right
 */
// function scrollRight() {
//   if (slider.scrollWidth - slider.clientWidth === slider.scrollLeft) {
//     slider.scrollTo({
//       left: 0,
//       behavior: "smooth"
//     });
//   } else {
//     slider.scrollBy({
//       left: window.innerWidth,
//       behavior: "smooth"
//     });
//   }
// }

// /**
//  * @brief Scroll to the left
//  */
// function scrollLeft() {
//   slider.scrollBy({
//     left: -window.innerWidth,
//     behavior: "smooth"
//   });
// }

// // Auto slider
// let timerId = setInterval(scrollRight, 7000);

// /**
//  * @brief Reset timer for scrolling right
//  */
// function resetTimer() {
//   clearInterval(timerId);
//   timerId = setInterval(scrollRight, 7000);
// }

// // Scroll Events
// slider.addEventListener("click", function (ev) {
//   if (ev.target === leftArrow) {
//     scrollLeft();
//     resetTimer();
//   }
// });

// slider.addEventListener("click", function (ev) {
//   if (ev.target === rightArrow) {
//     scrollRight();
//     resetTimer();
//   }
// });
