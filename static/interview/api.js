API_URL = "/interview/api/get-response/"

function endInterview() {
    const codeEditor = get("CODE_EDITOR");
    if (codeEditor) {
        codeEditor.style.pointerEvents = "none";
        codeEditor.style.opacity = "0.5";
    }

    alert("Time is up! Your interview has ended.");

    window.location.href = `/interview/end/${window.interviewId}/`;
}

async function sendTextCode(transcribedText = "", code = "") {
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
                interview_id: interviewId
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        typeAndSay(data);
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

function sendRecordings(screenStream, videoStream, audioStream) {
    console.log("sendRecordings called:", { 
        hasScreen: !!screenStream, 
        hasVideo: !!videoStream, 
        hasAudio: !!audioStream 
    });
}

function sendHeartbeat() {
    console.log("sendHeartbeat called");
}

function submitInterview(finalCode, duration) {
    console.log("submitInterview called:", { 
        finalCode: finalCode.substring(0, 50) + "...", 
        duration 
    });
}

function typeAndSay(data) {
    if (!data || !data.reasoning) return;
    
    const chatMessages = get('CHAT_MESSAGES');
    if (chatMessages) {
        const msgDiv = make('div', { className: 'chat-message ai-message' });
        msgDiv.innerHTML = `<i class="bi bi-robot"></i><p id="ai-typing"></p>`;
        add(chatMessages, msgDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        
        const typingElement = get('ai-typing');
        if (typingElement) {
            // Type animation for reasoning text in chat
            typeText(typingElement, data.reasoning, 30);
        }
    }
    
    // Update AI status text with typing animation
    const aiStatus = get('AI_STATUS');
    if (aiStatus) {
        typeText(aiStatus, data.reasoning, 30);
    }
    
    // Play audio response if available
    if (data.audio && window.speaker) {
        // Convert base64 audio to playable format
        const audioBlob = base64ToBlob(data.audio, 'audio/mpeg');
        const audioUrl = URL.createObjectURL(audioBlob);
        
        window.speaker.src = audioUrl;
        window.speaker.play().catch(err => {
            console.error('Audio play error:', err);
        });
        
        // Clean up URL after playing
        window.speaker.onended = () => {
            URL.revokeObjectURL(audioUrl);
        };
    }
}

function typeText(element, text, delay = 30) {
    if (!element || !text) return;
    
    element.textContent = '';
    let index = 0;
    
    const typeInterval = setInterval(() => {
        if (index < text.length) {
            element.textContent += text[index];
            index++;
            
            // Auto-scroll if in chat
            const chatMessages = get('CHAT_MESSAGES');
            if (chatMessages && element.closest('#CHAT_MESSAGES')) {
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }
        } else {
            clearInterval(typeInterval);
        }
    }, delay);
}

function base64ToBlob(base64, mimeType) {
    // Remove data URL prefix if present
    const base64Data = base64.includes(',') ? base64.split(',')[1] : base64;
    
    const byteCharacters = atob(base64Data);
    const byteNumbers = new Array(byteCharacters.length);
    
    for (let i = 0; i < byteCharacters.length; i++) {
        byteNumbers[i] = byteCharacters.charCodeAt(i);
    }
    
    const byteArray = new Uint8Array(byteNumbers);
    return new Blob([byteArray], { type: mimeType });
}

