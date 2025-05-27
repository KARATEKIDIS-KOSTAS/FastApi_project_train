html = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Real-Time Chat</title>
  <style>
    body {
      margin: 0;
      font-family: "Segoe UI", sans-serif;
      background-color: #121212;
      color: #fff;
      display: flex;
      flex-direction: column;
      height: 100vh;
    }

    header {
      background: #1f1f1f;
      padding: 1rem;
      text-align: center;
      font-size: 1.5rem;
      font-weight: bold;
      color: #00ffcc;
      box-shadow: 0 2px 10px rgba(0, 0, 0, 0.4);
    }

    #chat {
      flex: 1;
      overflow-y: auto;
      padding: 1rem;
      display: flex;
      flex-direction: column;
      gap: 0.5rem;
    }

    .message {
      padding: 0.75rem 1rem;
      border-radius: 15px;
      max-width: 70%;
      word-wrap: break-word;
      animation: fadeIn 0.3s ease-in;
    }

    .you {
      align-self: flex-end;
      background-color: #00b894;
      color: white;
    }

    .other {
      align-self: flex-start;
      background-color: #2d3436;
      color: white;
    }

    form {
      display: flex;
      padding: 1rem;
      background: #1f1f1f;
    }

    input[type="text"] {
      flex: 1;
      padding: 0.75rem;
      border-radius: 10px;
      border: none;
      outline: none;
      font-size: 1rem;
      margin-right: 0.5rem;
    }

    button {
      padding: 0.75rem 1.5rem;
      border: none;
      border-radius: 10px;
      background-color: #00cec9;
      color: white;
      font-weight: bold;
      cursor: pointer;
      transition: background-color 0.3s;
    }

    button:hover {
      background-color: #00b894;
    }

    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(10px); }
      to { opacity: 1; transform: translateY(0); }
    }
  </style>
</head>
<body>
  <header>💬 Live Chat</header>
  <div id="chat"></div>

  <form onsubmit="sendMessage(event)">
    <input type="text" id="messageText" placeholder="Type a message..." autocomplete="off" required />
    <button>Send</button>
  </form>

  <script>
    let username = null;

    // Prompt for a nickname before connecting
    while (!username) {
      username = prompt("Enter your nickname:");
    }

    const ws = new WebSocket("ws://localhost:8000/chat/message");
    const chat = document.getElementById("chat");
    const input = document.getElementById("messageText");

    ws.onopen = () => {
      // Send the nickname to the server once the connection is open
      ws.send(JSON.stringify({ type: "join", user: username }));
    };

    ws.onmessage = (event) => {
      const data = event.data;
      const message = document.createElement("div");
      message.classList.add("message", "other");
      message.textContent = data;
      chat.appendChild(message);
      chat.scrollTop = chat.scrollHeight;
    };

    function sendMessage(event) {
      event.preventDefault();
      const text = input.value.trim();
      if (text !== "") {
        // Send message to server along with username
        ws.send(JSON.stringify({ type: "chat", user: username, message: text }));

        const message = document.createElement("div");
        message.classList.add("message", "you");
        message.textContent = `You: ${text}`;
        chat.appendChild(message);
        chat.scrollTop = chat.scrollHeight;

        input.value = "";
      }
    }
  </script>

</body>
</html>
"""
''' <script>
    const ws = new WebSocket("ws://localhost:8000/chat/message");
    const chat = document.getElementById("chat");
    const input = document.getElementById("messageText");

    ws.onmessage = (event) => {
      // When receiving a message, display it as "other"
      const message = document.createElement("div");
      message.classList.add("message", "other");
      message.textContent = event.data;
      chat.appendChild(message);
      chat.scrollTop = chat.scrollHeight;
    };

    function sendMessage(event) {
      event.preventDefault();
      const text = input.value.trim();
      if (text !== "") {
        ws.send(text);

        // Show your own message with a different style
        const message = document.createElement("div");
        message.classList.add("message", "you");
        message.textContent = text;
        chat.appendChild(message);
        chat.scrollTop = chat.scrollHeight;

        input.value = "";
      }
    }
  </script>'''