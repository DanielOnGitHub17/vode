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

// Code actions
get('BTN_RUN').addEventListener('click', () => {
    const code = editor.getValue();
    const output = get('CONSOLE_OUTPUT');
    output.innerHTML = '<small><i class="bi bi-hourglass-split"></i> Running...</small>';
    
    setTimeout(() => {
        output.innerHTML = '<small><i class="bi bi-check-circle"></i> Code executed successfully</small>';
    }, 1000);
});

get('BTN_SUBMIT').addEventListener('click', () => {
    const code = editor.getValue();
    const output = get('CONSOLE_OUTPUT');
    output.innerHTML = '<small><i class="bi bi-upload"></i> Submitting...</small>';
    
    setTimeout(() => {
        output.innerHTML = '<small><i class="bi bi-check-circle-fill"></i> Code submitted successfully!</small>';
        get('CODE_STATUS').textContent = 'Submitted';
    }, 1000);
});

// Chat functionality
get('BTN_SEND_CHAT')?.addEventListener('click', sendMessage);
get('CHAT_INPUT')?.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});

function sendMessage() {
    const input = get('CHAT_INPUT');
    const msg = input.value.trim();
    if (!msg) return;
    
    const msgDiv = make('div', { className: 'chat-message' });
    msgDiv.innerHTML = `<i class="bi bi-person-fill"></i><p>${msg}</p>`;
    add(get('CHAT_MESSAGES'), msgDiv);
    
    input.value = '';
    get('CHAT_MESSAGES').scrollTop = get('CHAT_MESSAGES').scrollHeight;
}

// Initialize everything when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    windowManager = new WindowManager();
    startTimer();
    initMonaco();
});
