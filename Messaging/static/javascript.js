    // Get the chats element
    const chatElementDiv = document.querySelectorAll(".list-group-item");

    chatElementDiv.forEach(chatElement => {
    // Add a click event listener to the chat element
    chatElement.addEventListener("click", () => {
      // Make an AJAX request to the server to get the chat messages
      fetch(`/messaging/chats/${chatElement.dataset.chatId}/messages/`)
        .then(response => response.json())
        .then(messages => {
          // Render the messages in the chat box
          const chatBox = document.getElementById("chat-field");
          chatBox.innerHTML = "";

          messages.forEach(message => {
            const messageElement = document.createElement("div");

            if (message.sender == user){
                messageElement.innerHTML = `
                     <div class="media w-50 ml-auto mb-3">
                    <div class="media-body">
                    <div class="bg-primary rounded py-2 px-3 mb-2">
                    <p class="text-small mb-0 text-white">${message.content}</p>
                  </div>
                  <p class="small text-muted">${message.timestamp}</p>
                </div>
              </div>
            </div>`
            }else{
                messageElement.innerHTML = `
                <div class="media-body ml-3">'
                 <div class="media w-50 mb-3">
                  <img src="https://bootstrapious.com/i/snippets/sn-chat/avatar.svg" alt="user" width="50" class="rounded-circle">
                  <div class="bg-light rounded py-2 px-3 mb-2">
                    <p class="text-small mb-0 text-muted">, ${message.content}</p>
                  </div>
                  <p class="small text-muted">${message.timestamp}</p>
                </div>
              </div>
            `;

            }

            chatBox.appendChild(messageElement);
          });
        });
    });
})

const socket = new WebSocket('ws://' + window.location.host + '/ws/chat/');

socket.onopen = function() {
    console.log('Websocket connected.');
};

socket.onclose = function() {
    console.log('Websocket disconnected.');
};

const messageInput = document.getElementById('message-input');
const sendBtn = document.getElementById('send-btn');
const messagesDiv = document.getElementById('chat-field');

sendBtn.addEventListener('click', function(event) {
  event.preventDefault();
    const message = messageInput.value.trim();
    if (message) {
        const data = {
            message: message
        };
        socket.send(JSON.stringify(data));
        messageInput.value = '';
    }
});

socket.onmessage = function(event) {
    const message = JSON.parse(event.data);
    const messageDiv = document.createElement('div');
    messageDiv.textContent = message.content;
    messagesDiv.appendChild(messageDiv);
};
