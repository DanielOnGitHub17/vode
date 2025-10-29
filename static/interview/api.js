API_URL = "/interview/api/get-response/"

function endInterview() {
    const codeEditor = get("CODE_EDITOR");
    if (codeEditor) {
        codeEditor.style.pointerEvents = "none";
        codeEditor.style.opacity = "0.5";
    }

    // alert("Time is up! Your interview has ended.");
    window.location.href = `/interview/end/${window.interviewId}/`;
    return;


    if (typeof window.sendRecordings === "function") {
        window.sendRecordings();
    } else {
        // Fallback if recorder not loaded
        window.location.href = `/interview/end/${window.interviewId}/`;
    }
}

async function sendTextCode(transcribedText = "", code = "") {
    // later, check code diff to see if any code changed so that you don't send code unnecessarily
    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken")
            },
            body: JSON.stringify({
                audio_transcript: transcribedText,
                code: code,
                interview_id: window.interviewId
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        // Display AI response in chat and play audio
        typeAndSay(data);

        return data;
    } catch (error) {
        console.error("sendTextCode error:", error);
        return null;
    }
}

function sendCode(code) {
    return sendTextCode("", code);
}

function sendText(text, code = "") {
    return sendTextCode(text, code);
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function sendHeartbeat() {
    console.log("sendHeartbeat called");
}

function naturalSpeech(audioBase64) {
    if (!audioBase64 || !window.speaker) {
        console.warn("No audio or speaker not available");
        return;
    }

    // Disable editor and mute speech recognition while audio is playing
    disableEditorAndSpeech();

    // Convert base64 audio to playable format
    const audioBlob = base64ToBlob(audioBase64, "audio/mpeg");
    const audioUrl = URL.createObjectURL(audioBlob);

    window.speaker.src = audioUrl;
    window.speaker.play().catch(err => {
        console.error("Audio play error:", err);
    });

    // Re-enable editor and speech after audio ends
    window.speaker.onended = () => {
        // URL.revokeObjectURL(audioUrl);
        // Want to be careful about revoking
        // Candidate might say, "please repeat what you said" - or something like that
        // We'd want to handle that efficiently
        
        // Wait second before re-enabling
        setTimeout(() => {
            enableEditorAndSpeech();
        }, 500);
    };
}

function backupSpeech(text) {
    if (!text || !window.speechSynthesis) {
        console.warn("No text or speechSynthesis not available");
        return;
    }

    // Disable editor and speech recognition
    disableEditorAndSpeech();

    const utterance = new SpeechSynthesisUtterance(text);
    
    utterance.onend = () => {
        setTimeout(() => {
            enableEditorAndSpeech();
        }, 500);
    };

    utterance.onerror = (err) => {
        console.error("Speech synthesis error:", err);
        enableEditorAndSpeech();
    };

    window.speechSynthesis.speak(utterance);
}

function typeAndSay(data) {
    if (!data || !data.reasoning) {
        console.warn("No reasoning data received");
        return;
    }

    // Add AI message to chat
    const aiMessageElement = sendMessage(data.reasoning, true);

    if (aiMessageElement) {
        // Type animation for reasoning text in chat
        typeText(aiMessageElement, data.reasoning, 30);
    }

    // Play audio response
    if (data.audio && data.audio !== "EMPTY") {
        naturalSpeech(data.audio);
    } else {
        backupSpeech(data.reasoning);
    }
}

function disableEditorAndSpeech() {
    // Disable Monaco editor
    const codeEditor = get("CODE_EDITOR");
    codeEditor.style.pointerEvents = "none";
    codeEditor.style.opacity = "0.5";

    // Show AI speaking overlay
    reclass(get("AI_SPEAKING_OVERLAY"), "active");

    // Stop speech recognition
    if (window.recognition) {
        window.recognition.stop();
        console.log("Speech recognition muted while AI is speaking");
    }
}

function enableEditorAndSpeech() {
    // Re-enable Monaco editor
    const codeEditor = get("CODE_EDITOR");
    codeEditor.style.pointerEvents = "auto";
    codeEditor.style.opacity = "1";

    // Hide AI speaking overlay
    reclass(get("AI_SPEAKING_OVERLAY"), "active", true);

    // Resume speech recognition
    if (window.recognition) {
        window.recognition.start();
        console.log("Speech recognition resumed");
    }
}

function typeText(element, text, delay = 30) {
    if (!element || !text) return;

    element.textContent = "";
    let index = 0;

    const typeInterval = setInterval(() => {
        if (index < text.length) {
            element.textContent += text[index];
            index++;

            // Auto-scroll chat to bottom
            const chatMessages = get("CHAT_MESSAGES");
            if (chatMessages) {
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }
        } else {
            clearInterval(typeInterval);
        }
    }, delay);
}

function base64ToBlob(base64, mimeType) {
    // Remove data URL prefix if present
    const base64Data = base64.includes(",") ? base64.split(",")[1] : base64;

    const byteCharacters = atob(base64Data);
    const byteNumbers = new Array(byteCharacters.length);

    for (let i = 0; i < byteCharacters.length; i++) {
        byteNumbers[i] = byteCharacters.charCodeAt(i);
    }

    const byteArray = new Uint8Array(byteNumbers);
    return new Blob([byteArray], { type: mimeType });
}

