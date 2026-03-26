// script.js

// WhatsApp Integration
const whatsappNumber = "+5491234567890";

// Function to open the chatbot
function abrirChatbot() {
    document.getElementById("chatbotContainer").style.display = "block";
}

// Function to close the chatbot
function cerrarChatbot() {
    document.getElementById("chatbotContainer").style.display = "none";
}

// Function to send message
function enviarMensaje(message) {
    agregarMensajeUsuario(message);
    processUserMessage(message);
}

// Function to add a message from the bot
function agregarMensajeBot(message) {
    const chatBox = document.getElementById("chatBox");
    const messageElement = document.createElement("div");
    messageElement.className = "bot-message";
    messageElement.innerHTML = message;
    chatBox.appendChild(messageElement);
}

// Function to add a message from the user
function agregarMensajeUsuario(message) {
    const chatBox = document.getElementById("chatBox");
    const messageElement = document.createElement("div");
    messageElement.className = "user-message";
    messageElement.innerHTML = message;
    chatBox.appendChild(messageElement);
}

// Function to process user messages and provide responses
function processUserMessage(message) {
    const responses = {
        "product1": "Here is information about Product 1.",
        "product2": "Here is information about Product 2."
    };

    const response = responses[message.toLowerCase()] || "Sorry, I couldn't find that product.";
    agregarMensajeBot(response);
}

// Keyboard event handling
document.addEventListener("keydown", function (event) {
    if (event.key === "Enter") {
        const inputField = document.getElementById("userInput");
        enviarMensaje(inputField.value);
        inputField.value = '';
    }
});

// Mobile menu toggle functionality
function toggleMobileMenu() {
    const menu = document.getElementById("mobileMenu");
    menu.classList.toggle("active");
}

// Smooth scroll navigation
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Responsive chatbot container
const chatbotContainer = document.createElement('div');
chatbotContainer.id = "chatbotContainer";
chatbotContainer.style.position = "fixed";
chatbotContainer.style.bottom = "0";
chatbotContainer.style.right = "0";
chatbotContainer.style.width = "300px";
chatbotContainer.style.display = "none";
document.body.appendChild(chatbotContainer);