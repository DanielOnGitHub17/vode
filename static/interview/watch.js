// TIMER_BADGE
/*
Timer Watch:
- TIMER_BADGE contains the time duration in its text content
- data-started-time contains when the interview started
- Add 30 seconds grace period to the duration
- When total time expires, call endInterview() to end the interview
*/

const TIMER_BADGE = get("TIMER_BADGE");

// Parse the duration and start time
function initializeTimer() {
    const timeLimitMinutes = parseInt(TIMER_BADGE.textContent.trim()); // e.g., "60" or "45"
    const startedTime = TIMER_BADGE.getAttribute("data-started-time"); // ISO timestamp when interview started

    // Calculate when the interview should stop
    const timeStartMs = new Date(startedTime).getTime();
    const timeLimitMs = timeLimitMinutes * 60 * 1000; // Convert minutes to milliseconds
    const gracePeriodMs = 30 * 1000; // 30 seconds grace period
    const timeStop = timeStartMs + timeLimitMs + gracePeriodMs;

    // Start the countdown with absolute stop timestamp
    startCountdown(timeStop);
}

function startCountdown(timeStop) {
    const interval = setInterval(() => {
        const now = Date.now();
        const timeRemainingMs = timeStop - now;
        const timeRemainingSeconds = Math.floor(timeRemainingMs / 1000);

        if (timeRemainingSeconds <= 0) {
            // Time's up!
            clearInterval(interval);
            TIMER_BADGE.textContent = "00:00";
            TIMER_BADGE.classList.remove("bg-primary");
            TIMER_BADGE.classList.add("bg-danger");

            // End interview
            endInterview();
        } else {
            // Update timer display
            const hours = Math.floor(timeRemainingSeconds / 3600);
            const minutes = Math.floor((timeRemainingSeconds % 3600) / 60);
            const seconds = timeRemainingSeconds % 60;

            let displayTime;
            if (hours > 0) {
                displayTime = `${String(hours).padStart(2, "0")}:${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;
            } else {
                displayTime = `${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;
            }

            TIMER_BADGE.textContent = displayTime;

            // Change color when less than 5 minutes remaining
            if (timeRemainingSeconds <= 300 && timeRemainingSeconds > 0) {
                TIMER_BADGE.classList.remove("bg-primary");
                TIMER_BADGE.classList.add("bg-warning");
            }
        }
    }, 1000); // Update every second
}


// ============================================
// USER ACTIVITY MONITORING
// ============================================

// Configuration
const COUNT_TO_CHECK = 200; // Keystroke threshold (50 default) for silent typing
const CODE_SEND_INTERVAL = 30000; // Send code if actively typing (every 30 seconds default)
const DEBOUNCE_DELAY = 10000; // Wait (default 2 seconds) after last keystroke

// State tracking
let keystrokeCount = 0;
let lastCodeContent = "";
let lastChatMessage = "";

// Use global speech recognition variables from permissions.js
// window.recognition
// window.transcribedText
// window.speechBuffer
// window.isUserSpeaking

// ============================================
// MONACO EDITOR MONITORING
// ============================================

let codeSendTimer = null;
let debounceTimer = null;

function watchMonacoEditor() {
    // Wait for Monaco editor to be initialized
    const checkEditor = setInterval(() => {
        if (typeof editor !== "undefined" && editor) {
            clearInterval(checkEditor);
            setupEditorListeners();
        }
    }, 500);
}

function setupEditorListeners() {
    // Listen to content changes in Monaco editor
    editor.onDidChangeModelContent((event) => {
        keystrokeCount++;

        // Clear existing debounce timer
        if (debounceTimer) {
            clearTimeout(debounceTimer);
        }

        // If user has typed COUNT_TO_CHECK times without speaking
        if (keystrokeCount >= COUNT_TO_CHECK && !window.isUserSpeaking) {
            handleSilentTyping();
            keystrokeCount = 0; // Reset counter
        }

        // Set debounce timer for inactive typing
        debounceTimer = setTimeout(() => {
            handleTypingPause();
        }, DEBOUNCE_DELAY);

        // Periodic code sending while actively typing
        if (!codeSendTimer) {
            codeSendTimer = setInterval(() => {
                const currentCode = editor.getValue();
                if (currentCode !== lastCodeContent && currentCode.trim().length > 0) {
                    sendCode(currentCode);
                    lastCodeContent = currentCode;
                }
            }, CODE_SEND_INTERVAL);
        }
    });

    // Track cursor position changes (user reading/reviewing code)
    editor.onDidChangeCursorPosition((event) => {
        // User is navigating code - could be reviewing
        // This helps us understand user behavior
    });

    // Track selection changes (user highlighting code)
    editor.onDidChangeCursorSelection((event) => {
        // User is selecting code - might be about to explain or modify
    });
}

// ============================================
// CHAT MONITORING
// ============================================

function watchChatBox() {
    console.log("Watching")
    const chatInput = get("CHAT_INPUT");
    const sendButton = get("BTN_SEND_CHAT");

    // Monitor chat input
    chatInput.addEventListener("keypress", (e) => {
        if (e.key === "Enter") {
            console.log("hit enter");
            handleChatMessage();
        }
    });

    // Monitor send button
    sendButton.addEventListener("click", () => {
        console.log("hit button");
        handleChatMessage();
        console.log("finised hit button");
    });
}

function handleChatMessage() {
    console.log("handleChatMessage called");

    const chatInput = get("CHAT_INPUT");
    const message = chatInput.value.trim();

    console.log("Message from input:", message);

    if (message) {
        // Show user message in chat immediately
        console.log("Calling sendMessage with:", message);

        if (typeof window.sendMessage === "function") {
            window.sendMessage(message, false);
        } else {
            console.error("sendMessage function not found!");
        }

        lastChatMessage = message;

        // Send chat message with current code context to API
        const currentCode = editor ? editor.getValue() : "";
        sendText(message, currentCode);

        // Clear input
        chatInput.value = "";
    } else {
        console.warn("No message to send");
    }
}

// ============================================
// DECISION LOGIC FOR API CALLS
// ============================================

function handleSpeechWithCode() {
    // User is speaking while coding
    const currentCode = editor ? editor.getValue() : "";

    if (currentCode.trim().length > 0 && window.transcribedText.length > 0) {
        // Send both transcribed text and code
        sendTextCode(window.transcribedText, currentCode);

        // Clear speech buffer after sending
        window.speechBuffer = "";
        window.transcribedText = "";
    }
}

function handleSilentTyping() {
    // User has typed COUNT_TO_CHECK times without speaking
    // They are focused on coding without verbal explanation
    const currentCode = editor ? editor.getValue() : "";

    if (currentCode !== lastCodeContent && currentCode.trim().length > 0) {
        sendCode(currentCode);
        lastCodeContent = currentCode;
    }
}

function handleTypingPause() {
    // User has paused typing (debounced)
    // Send current code state
    const currentCode = editor ? editor.getValue() : "";

    if (currentCode !== lastCodeContent && currentCode.trim().length > 0) {
        sendCode(currentCode);
        lastCodeContent = currentCode;
    }

    // Reset keystroke counter on pause
    keystrokeCount = 0;
}

function cleanupMonitoring() {
    // Stop speech recognition
    if (window.recognition) {
        window.recognition.stop();
    }

    // Clear timers
    if (codeSendTimer) {
        clearInterval(codeSendTimer);
    }
    if (debounceTimer) {
        clearTimeout(debounceTimer);
    }

    console.log("Monitoring cleanup complete");
}

// Override endInterview to include cleanup
const originalEndInterview = window.endInterview;
window.endInterview = function () {
    cleanupMonitoring();
    if (originalEndInterview) {
        originalEndInterview();
    }
};

// Initialize timer when page loads

onload = () => {
    if (TIMER_BADGE) {
        initializeTimer();
    } else {
        console.error("TIMER_BADGE element not found");
    }

    // Initialize all monitoring systems
    // Speech recognition is initialized in permissions.js
    watchMonacoEditor();
    watchChatBox();

    console.log("Interview monitoring systems initialized");
}