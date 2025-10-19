// Interview Page Setup using funcs.js
let editor;
let timerInterval;
let windowManager;

// Initialize Monaco Editor
function initMonaco() {
    require.config({ paths: { vs: 'https://cdn.jsdelivr.net/npm/monaco-editor@0.44.0/min/vs' } });
    require(['vs/editor/editor.main'], function () {
        editor = monaco.editor.create(get('CODE_EDITOR'), {
            value: '// Write your code here\n',
            language: 'python',
            theme: 'vs-dark',
            automaticLayout: true,
            fontSize: 14,
            minimap: { enabled: false }
        });
    });
}

// Timer functionality
function startTimer() {
    let totalSeconds = 45 * 60;
    timerInterval = setInterval(() => {
        totalSeconds--;
        const mins = Math.floor(totalSeconds / 60);
        const secs = totalSeconds % 60;
        get('TIMER_BADGE').textContent = `${mins}:${secs < 10 ? '0' : ''}${secs}`;
        if (totalSeconds <= 0) clearInterval(timerInterval);
    }, 1000);
}

// Language selector
get('LANGUAGE_SELECT').addEventListener('change', (e) => {
    const langMap = {
        'python': 'python',
        'javascript': 'javascript',
        'typescript': 'typescript',
        'java': 'java',
        'cpp': 'cpp',
        'csharp': 'csharp',
        'go': 'go'
    };
    monaco.editor.setModelLanguage(editor.getModel(), langMap[e.target.value]);
});

function sendMessage() {
    const input = get('CHAT_INPUT');
    const chatMessages = get('CHAT_MESSAGES');
    
    if (!input || !chatMessages) return;
    
    const msg = input.value.trim();
    if (!msg) return;
    
    const msgDiv = make('div', { className: 'chat-message' });
    msgDiv.innerHTML = `<i class="bi bi-person-fill"></i><p>${msg}</p>`;
    add(chatMessages, msgDiv);
    
    // chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Initialize everything when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    windowManager = new WindowManager();
    // Timer is handled by watch.js
    initMonaco();
});
