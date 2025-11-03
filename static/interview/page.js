// Interview Page Setup using funcs.js
let editor;
let timerInterval;
let windowManager;

// Initialize Monaco Editor
function initMonaco() {
    require.config({ paths: { vs: "https://cdn.jsdelivr.net/npm/monaco-editor@0.44.0/min/vs" } });
    require(["vs/editor/editor.main"], function () {
        editor = monaco.editor.create(get("CODE_EDITOR"), {
            value: "// Write your code here\n",
            language: "python",
            theme: "vs-dark",
            automaticLayout: true,
            fontSize: 14,
            minimap: { enabled: false }
        });
    });
}

// Language selector
get("LANGUAGE_SELECT").addEventListener("change", (e) => {
    const langMap = {
        "python": "python",
        "javascript": "javascript",
        "typescript": "typescript",
        "java": "java",
        "cpp": "cpp",
        "csharp": "csharp",
        "go": "go"
    };
    monaco.editor.setModelLanguage(editor.getModel(), langMap[e.target.value]);
});

function sendMessage(messageText = null, isAI = false) {
    console.log("sendMessage called:", { messageText, isAI });
    
    const input = get("CHAT_INPUT");
    const chatMessages = get("CHAT_MESSAGES");
    
    if (!chatMessages) {
        console.error("CHAT_MESSAGES not found");
        return null;
    }
    
    console.log("CHAT_MESSAGES found:", chatMessages);
    
    // Get message text - either from parameter or input field
    const msg = messageText || (input ? input.value.trim() : "");
    if (!msg) {
        console.warn("No message text to send");
        return null;
    }
    
    console.log("Creating message div for:", msg);

    // Create message div
    const msgDiv = make();
    msgDiv.className = "chat-message";
    
    if (isAI) {
        // AI message with robot icon
        msgDiv.innerHTML = `<i class="bi bi-robot"></i><p class="ai-message"></p>`;
    } else {
        // User message with person icon
        msgDiv.innerHTML = `<i class="bi bi-person-fill"></i><p>${msg}</p>`;
    }
    
    console.log("Adding message to chat:", msgDiv);
    add(msgDiv, chatMessages);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    // Clear input if it was used
    if (!messageText && input) {
        input.value = "";
    }
    
    // Return the paragraph element for AI typing animation
    if (isAI) {
        return msgDiv.querySelector("p.ai-message");
    }
    
    return msgDiv;
}

// Make sendMessage globally available
window.sendMessage = sendMessage;

// Initialize everything when DOM is ready
document.addEventListener("DOMContentLoaded", () => {
    windowManager = new WindowManager();
    // Timer is handled by watch.js
    initMonaco();
});
