// Connect to the WebSocket server
const socket = io();
const textarea = document.getElementById('note-content');
const saveBtn = document.getElementById('save-btn');

// When the user clicks Save, send the text over the socket
saveBtn.addEventListener('click', () => {
const text = textarea.value;
socket.emit('update_text', { content: text });
});

// Listen for updates broadcasted by the server
socket.on('text_updated', (data) => {
textarea.value = data.content;
});