const socket = io();

const addForm = document.getElementById('add-form');
const itemInput = document.getElementById('item-input');
const shoppingList = document.getElementById('shopping-list');

// Send new item to server
addForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const name = itemInput.value;
    if (name) {
        socket.emit('add_item', { name: name });
        itemInput.value = '';
    }
});

// Helper functions called from HTML buttons
function toggleItem(id) {
    socket.emit('toggle_item', { id: id });
}

function deleteItem(id) {
    socket.emit('delete_item', { id: id });
}

// Receive updated list from Python server and update DOM
socket.on('list_updated', (items) => {
    shoppingList.innerHTML = '';
    
    const reversedItems = [...items].reverse();
    reversedItems.forEach(item => {
        const li = document.createElement('li');
        if (item.done) li.classList.add('completed');
        li.dataset.id = item.id;

        li.innerHTML = `
            <span class="item-name" onclick="toggleItem(${item.id})">${escapeHtml(item.name)}</span>
            <button class="delete-btn" onclick="deleteItem(${item.id})">✕</button>
        `;
        shoppingList.appendChild(li);
    });
});

// Basic security helper to prevent HTML injection in list items
function escapeHtml(text) {
    const div = document.createElement('div');
    div.innerText = text;
    return div.innerHTML;
}