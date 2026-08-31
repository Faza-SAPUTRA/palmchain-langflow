// UI Interactivity
const chatbotToggle = document.getElementById('chatbot-toggle');
const chatbotWidget = document.getElementById('chatbot-widget');
const chatMessages = document.getElementById('chat-messages');
const chatInput = document.getElementById('chat-input');
const sendBtn = document.getElementById('send-btn');

// Toggle Widget
chatbotToggle.addEventListener('click', () => {
  chatbotWidget.classList.toggle('open');
});

// Create Message Element
function appendMessage(text, sender) {
  const msgDiv = document.createElement('div');
  msgDiv.classList.add('message', `${sender}-message`);
  
  if (sender === 'ai' && typeof marked !== 'undefined') {
    // Konversi Markdown (tabel, bold, link) ke HTML yang cantik
    msgDiv.innerHTML = marked.parse(text);
  } else {
    // Input dari user tetap text biasa demi keamanan
    msgDiv.innerText = text;
  }
  
  chatMessages.appendChild(msgDiv);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Generate a random session ID once per page load
const currentSessionId = "palmchain-session-" + Math.random().toString(36).substr(2, 9);

// Call Langflow API
async function callLangflow(message) {
  const LANGFLOW_API_URL = "http://127.0.0.1:7860/api/v1/run/";
  const FLOW_ID = "8626c632-3b3b-428d-942a-79ee3024a9c2"; 
  const LANGFLOW_API_KEY = "sk-FYWivzZs13514fS0uTuT4xtRu3aEHTT-_E6QLCLf01Q"; 
  
  // Tampilkan indikator mengetik
  const typingDiv = document.createElement('div');
  typingDiv.classList.add('message', 'ai-message', 'typing-indicator');
  typingDiv.innerText = "Berpikir...";
  chatMessages.appendChild(typingDiv);
  chatMessages.scrollTop = chatMessages.scrollHeight;

  try {
    const headers = {
      'Content-Type': 'application/json'
    };
    
    // Tambahkan token
    if (LANGFLOW_API_KEY !== "MASUKKAN_API_KEY_LANGFLOW_DISINI") {
      headers['x-api-key'] = LANGFLOW_API_KEY;
    }

    const response = await fetch(`${LANGFLOW_API_URL}${FLOW_ID}`, {
      method: 'POST',
      headers: headers,
      body: JSON.stringify({
        input_value: message,
        output_type: "chat",
        input_type: "chat",
        session_id: currentSessionId
      })
    });

    chatMessages.removeChild(typingDiv); // Hapus indikator mengetik

    if (response.ok) {
      const data = await response.json();
      // Parsing response Langflow (biasanya ada di dalam session_id/outputs/...)
      // Untuk MVP, kita ambil output teksnya secara default
      let aiResponseText = "Tidak ada respons dari AI.";
      
      if (data.outputs && data.outputs.length > 0) {
        const results = data.outputs[0].outputs[0].results;
        if(results && results.message && results.message.text) {
           aiResponseText = results.message.text;
        }
      }
      
      appendMessage(aiResponseText, 'ai');
    } else {
      appendMessage("Maaf, terjadi kesalahan koneksi ke server Langflow.", 'ai');
    }
  } catch (error) {
    chatMessages.removeChild(typingDiv);
    console.error("Langflow Error:", error);
    appendMessage("Gagal terhubung ke AI Langflow. Pastikan server nyala dan Flow ID benar.", 'ai');
  }
}

// Handle Send
function sendMessage(message) {
  const text = message || chatInput.value.trim();
  if (!text) return;
  
  appendMessage(text, 'user');
  if (!message) chatInput.value = '';
  
  // Call AI
  callLangflow(text);
}

// Event Delegation untuk tombol CTA dari AI
chatMessages.addEventListener('click', function(e) {
  if (e.target && e.target.classList.contains('cta-btn')) {
    e.preventDefault();
    const buttonText = e.target.innerText || e.target.textContent;
    sendMessage(buttonText);
  }
});

sendBtn.addEventListener('click', () => sendMessage());
chatInput.addEventListener('keypress', (e) => {
  if (e.key === 'Enter') sendMessage();
});
