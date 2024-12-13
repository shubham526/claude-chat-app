// Initialize conversation array
let conversation = [];

// Function to load conversation from server
async function loadConversation() {
    try {
        const response = await fetch('/api/get-conversation');
        const data = await response.json();
        if (data.conversation && data.conversation.length > 0) {
            conversation = data.conversation;
            // Display existing messages
            conversation.forEach(msg => {
                addMessage(msg.role, msg.content);
            });
        } else {
            // Initialize with default message if no conversation exists
            conversation = [{
                role: "user",
                content: "You are Claude, an AI assistant created by Anthropic. You're helpful, harmless, and honest."
            }];
        }
    } catch (error) {
        console.error('Error loading conversation:', error);
        // Initialize with default message on error
        conversation = [{
            role: "user",
            content: "You are Claude, an AI assistant created by Anthropic. You're helpful, harmless, and honest."
        }];
    }
}

// Utility function to escape HTML characters
function escapeHTML(html) {
    return html
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}

function addMessage(role, content) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role === 'user' ? 'ml-auto bg-blue-100' : 'bg-gray-100'} rounded-lg p-4`;

    // First, split the content into code and non-code parts
    const parts = content.split(/```(\w+)?\n([\s\S]*?)```/);
    let formattedContent = '';

    for (let i = 0; i < parts.length; i++) {
        if (i % 3 === 0) {
            // Regular text content - needs HTML escaping
            formattedContent += escapeHTML(parts[i]);
        } else if (i % 3 === 1) {
            // Language specification (if any)
            continue;
        } else {
            // Code block content - escape HTML for display
            const language = parts[i - 1] || 'plaintext';
            const code = escapeHTML(parts[i]); // Ensure HTML inside code blocks is escaped
            formattedContent += `
                <div class="relative">
                    <button class="copy-code-btn" data-code="${encodeURIComponent(parts[i])}">Copy code</button>
                    <pre><code class="language-${language}">${code}</code></pre>
                </div>
            `;
        }
    }

    messageDiv.innerHTML = `<div class="text-gray-800">${formattedContent}</div>`;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    // Apply syntax highlighting
    setTimeout(() => {
        document.querySelectorAll('pre code').forEach((el) => {
            hljs.highlightElement(el);
        });
    }, 0);
}

function addTypingIndicator() {
    const indicator = document.createElement('div');
    indicator.className = 'typing-indicator bg-gray-100 rounded-lg p-4';
    indicator.innerHTML = '<span></span><span></span><span></span>';
    chatMessages.appendChild(indicator);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    return indicator;
}

// Get DOM elements
const chatMessages = document.getElementById('chat-messages');
const chatForm = document.getElementById('chat-form');
const userInput = document.getElementById('user-input');

chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    let userMessage = userInput.value.trim();
    if (!userMessage) return;

    console.log('Sending message:', userMessage);
    console.log('Current conversation:', conversation);

    // Add user message to the chat for display
    addMessage('user', userMessage);

    // Add user message to the conversation array
    conversation.push({
        role: "user",
        content: userMessage
    });

    userInput.value = ''; // Clear input field

    // Show typing indicator
    const typingIndicator = addTypingIndicator();

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ conversation })
        });

        console.log('Response status:', response.status);
        const data = await response.json();
        console.log('Response data:', data);

        // Remove typing indicator
        typingIndicator.remove();

        if (data.error) {
            console.error('Error from server:', data.error);
            addMessage('assistant', 'Sorry, an error occurred. Please try again.');
        } else {
            // Add assistant's message
            addMessage('assistant', data.content);
            conversation.push({
                role: "assistant",
                content: data.content
            });
        }
    } catch (error) {
        console.error('Error:', error);
        typingIndicator.remove();
        addMessage('assistant', 'Sorry, an error occurred. Please try again.');
    }
});

// Enable textarea submission with Enter (Shift+Enter for new line)
userInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        chatForm.dispatchEvent(new Event('submit'));
    }
});

// Event delegation for copying code
document.addEventListener('click', (e) => {
    if (e.target && e.target.classList.contains('copy-code-btn')) {
        const codeToCopy = decodeURIComponent(e.target.dataset.code);
        navigator.clipboard.writeText(codeToCopy).then(() => {
            e.target.textContent = 'Copied!';
            setTimeout(() => (e.target.textContent = 'Copy code'), 2000);
        });
    }
});

// Load conversation when page loads
document.addEventListener('DOMContentLoaded', loadConversation);
