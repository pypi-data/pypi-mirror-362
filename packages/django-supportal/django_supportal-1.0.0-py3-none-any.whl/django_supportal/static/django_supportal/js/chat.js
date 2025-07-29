// chat websocket client
class ChatClient {
    constructor(websocketUrl, businessId, sessionId) {
        this.websocketUrl = websocketUrl;
        this.businessId = businessId;
        this.sessionId = sessionId;
        this.socket = null;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        this.reconnectInterval = 3000;
        
        this.initializeElements();
        this.connect();
        this.setupEventListeners();
    }
    
    initializeElements() {
        this.messagesContainer = document.getElementById('chat-messages');
        this.messageInput = document.getElementById('message-input');
        this.sendButton = document.getElementById('send-button');
        this.connectionStatus = document.getElementById('connection-status');
    }
    
    connect() {
        try {
            this.socket = new WebSocket(this.websocketUrl);
            this.setupSocketEventListeners();
        } catch (error) {
            console.error('websocket connection failed:', error);
            this.handleConnectionError();
        }
    }
    
    setupSocketEventListeners() {
        this.socket.onopen = () => {
            console.log('websocket connected');
            this.updateConnectionStatus('connected', true);
            this.reconnectAttempts = 0;
            this.enableInput();
        };
        
        this.socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.handleMessage(data);
        };
        
        this.socket.onclose = (event) => {
            console.log('websocket disconnected:', event.code, event.reason);
            this.updateConnectionStatus('disconnected', false);
            this.disableInput();
            this.attemptReconnect();
        };
        
        this.socket.onerror = (error) => {
            console.error('websocket error:', error);
            this.handleConnectionError();
        };
    }
    
    setupEventListeners() {
        this.sendButton.addEventListener('click', () => {
            this.sendMessage();
        });
        
        this.messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendMessage();
            }
        });
    }
    
    sendMessage() {
        const message = this.messageInput.value.trim();
        if (!message || !this.socket || this.socket.readyState !== WebSocket.OPEN) {
            return;
        }
        
        const data = {
            message: message,
            type: 'user'
        };
        
        this.socket.send(JSON.stringify(data));
        this.messageInput.value = '';
        this.disableInput();
    }
    
    handleMessage(data) {
        if (data.error) {
            this.displayMessage(data.error, 'system');
        } else {
            this.displayMessage(data.message, data.sender);
        }
        
        this.enableInput();
    }
    
    displayMessage(message, sender) {
        const messageElement = document.createElement('div');
        messageElement.className = `message ${sender}`;
        
        const messageContent = document.createElement('div');
        messageContent.textContent = message;
        messageElement.appendChild(messageContent);
        
        const messageTime = document.createElement('div');
        messageTime.className = 'message-time';
        messageTime.textContent = new Date().toLocaleTimeString();
        messageElement.appendChild(messageTime);
        
        this.messagesContainer.appendChild(messageElement);
        this.scrollToBottom();
    }
    
    scrollToBottom() {
        this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
    }
    
    updateConnectionStatus(status, connected) {
        this.connectionStatus.textContent = status;
        this.connectionStatus.className = connected ? 'status connected' : 'status';
    }
    
    enableInput() {
        this.messageInput.disabled = false;
        this.sendButton.disabled = false;
        this.messageInput.focus();
    }
    
    disableInput() {
        this.messageInput.disabled = true;
        this.sendButton.disabled = true;
    }
    
    handleConnectionError() {
        this.updateConnectionStatus('error', false);
        this.disableInput();
        this.attemptReconnect();
    }
    
    attemptReconnect() {
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            this.updateConnectionStatus(`reconnecting (${this.reconnectAttempts}/${this.maxReconnectAttempts})`, false);
            
            setTimeout(() => {
                this.connect();
            }, this.reconnectInterval);
        } else {
            this.updateConnectionStatus('connection failed', false);
            this.displayMessage('connection lost. please refresh the page.', 'system');
        }
    }
}

// initialize chat client when page loads
document.addEventListener('DOMContentLoaded', () => {
    new ChatClient(websocketUrl, businessId, sessionId);
});