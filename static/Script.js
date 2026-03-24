// ============================================================
// Digital Forensics Investigation Assistant
// IBM Internship Project — Frontend JavaScript
// ============================================================

const chatMessages = document.getElementById("chat-messages");
const userInput = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");

// Set welcome message time
document.getElementById("welcome-time").textContent = getTime();

// ---- UTILITY FUNCTIONS ----

function getTime() {
  return new Date().toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit",
  });
}

function scrollToBottom() {
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function formatText(text) {
  // Convert basic markdown-like text to HTML
  return text
    .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
    .replace(/\*(.*?)\*/g, "<em>$1</em>")
    .replace(/\n\n/g, "<br><br>")
    .replace(/\n/g, "<br>")
    .replace(/•\s/g, "• ");
}

// ---- ADD USER MESSAGE ----

function addUserMessage(text) {
  const row = document.createElement("div");
  row.className = "message-row user-row";

  const avatar = document.createElement("div");
  avatar.className = "msg-avatar user-avatar";
  avatar.textContent = "You";

  const bubble = document.createElement("div");
  bubble.className = "bubble user-bubble";
  bubble.innerHTML = `${formatText(text)}<span class="msg-time">${getTime()}</span>`;

  row.appendChild(avatar);
  row.appendChild(bubble);
  chatMessages.appendChild(row);
  scrollToBottom();
}

// ---- ADD BOT MESSAGE ----

function addBotMessage(text, type = "normal") {
  const row = document.createElement("div");
  row.className = "message-row bot-row";

  const avatar = document.createElement("div");
  avatar.className = "msg-avatar bot-avatar";
  avatar.textContent = "DF";

  const bubble = document.createElement("div");

  if (type === "out_of_scope") {
    bubble.className = "bubble bot-bubble out-of-scope-bubble";
  } else if (type === "error") {
    bubble.className = "bubble bot-bubble error-bubble";
  } else {
    bubble.className = "bubble bot-bubble";
  }

  bubble.innerHTML = `${formatText(text)}<span class="msg-time">${getTime()}</span>`;

  row.appendChild(avatar);
  row.appendChild(bubble);
  chatMessages.appendChild(row);
  scrollToBottom();
}

// ---- TYPING INDICATOR ----

function showTyping() {
  const row = document.createElement("div");
  row.className = "message-row bot-row";
  row.id = "typing-indicator";

  const avatar = document.createElement("div");
  avatar.className = "msg-avatar bot-avatar";
  avatar.textContent = "DF";

  const bubble = document.createElement("div");
  bubble.className = "bubble bot-bubble typing-bubble";
  bubble.innerHTML = `
    <div class="typing-dots">
      <span></span><span></span><span></span>
    </div>
  `;

  row.appendChild(avatar);
  row.appendChild(bubble);
  chatMessages.appendChild(row);
  scrollToBottom();
}

function hideTyping() {
  const el = document.getElementById("typing-indicator");
  if (el) el.remove();
}

// ---- SEND MESSAGE (calls Python Flask backend) ----

async function sendMessage() {
  const question = userInput.value.trim();
  if (!question) return;

  // Show user message
  addUserMessage(question);
  userInput.value = "";
  userInput.style.height = "auto";
  sendBtn.disabled = true;

  // Show typing indicator
  showTyping();

  try {
    // Send to Python Flask backend (/ask route)
    const response = await fetch("/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: question }),
    });

    const data = await response.json();
    hideTyping();

    if (data.error) {
      addBotMessage("Error: " + data.error, "error");
    } else if (data.out_of_scope) {
      addBotMessage(data.answer, "out_of_scope");
    } else {
      addBotMessage(data.answer, "normal");
    }
  } catch (err) {
    hideTyping();
    addBotMessage(
      "Connection error. Make sure the Python Flask server is running (python app.py).",
      "error",
    );
  }

  sendBtn.disabled = false;
  userInput.focus();
}

// ---- EVENT LISTENERS ----

// Send on button click
sendBtn.addEventListener("click", sendMessage);

// Send on Enter key (Shift+Enter = new line)
userInput.addEventListener("keydown", function (e) {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});

// Auto-resize textarea
userInput.addEventListener("input", function () {
  this.style.height = "auto";
  this.style.height = Math.min(this.scrollHeight, 100) + "px";
});
