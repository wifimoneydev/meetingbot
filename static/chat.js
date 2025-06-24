// static/chat.js
document.getElementById('user-input').addEventListener('keypress', async function (e) {
    if (e.key === 'Enter' && this.value.trim()) {
      const userMessage = this.value.trim();
      addMessage('user', userMessage);
      this.value = '';
      try {
        const res = await fetch('/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message: userMessage })
        });
        const data = await res.json();
        addMessage('bot', data.response);
      } catch (error) {
        addMessage('bot', 'Error: Something went wrong.');
      }
    }
  });
  
  function addMessage(sender, text) {
    const msg = document.createElement('div');
    msg.className = sender === 'user' ? 'user-msg' : 'bot-msg';
    msg.innerText = (sender === 'user' ? 'You: ' : 'Bot: ') + text;
    document.getElementById('messages').appendChild(msg);
    document.getElementById('messages').scrollTop = document.getElementById('messages').scrollHeight;
  }
  