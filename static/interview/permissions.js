// Hide page body initially
document.body.style.display = 'none';

// Global storage for media streams
window.entire_screen_feed = null;
window.video_feed = null;
window.audio_feed = null; // Will be extracted from screen share

// Global speech recognition
window.recognition = null;
window.transcribedText = '';
window.speechBuffer = '';
window.isUserSpeaking = false;

// Interview ID
let url = window.location.pathname.split('/');
window.interviewId = parseInt(url[url.length - 2]);

// Audio playback for AI responses
window.speaker = new Audio();


async function requestPermissions() {
    try {
        // Request screen capture with audio - MUST BE ENTIRE SCREEN WITH SYSTEM AUDIO
        window.entire_screen_feed = await navigator.mediaDevices.getDisplayMedia({
            video: {
                displaySurface: 'monitor' // Force entire screen only, not window or browser
            },
            audio: true, // Must include system audio
            preferCurrentTab: false,
            surfaceSwitching: 'exclude', // Prevent switching to window/tab
            selfBrowserSurface: 'exclude' // Exclude browser surfaces
        });

        // Verify that the user selected entire screen (not window or tab)
        const videoTrack = window.entire_screen_feed.getVideoTracks()[0];
        const audioTracks = window.entire_screen_feed.getAudioTracks();
        const settings = videoTrack.getSettings();
        
        // Check if displaySurface is 'monitor' (entire screen)
        if (settings.displaySurface !== 'monitor') {
            // User selected window or tab instead of entire screen
            window.entire_screen_feed.getTracks().forEach(track => track.stop());
            throw new Error('You must share your entire screen, not a window or tab.');
        }

        // Check if system audio is included
        if (audioTracks.length === 0) {
            // No audio track in screen share
            window.entire_screen_feed.getTracks().forEach(track => track.stop());
            throw new Error('You must share system audio along with your screen.');
        }

        // Extract audio from screen share for later use
        window.audio_feed = new MediaStream(audioTracks);

        // Request user camera feed
        window.video_feed = await navigator.mediaDevices.getUserMedia({
            video: true,
            audio: false
        });

        // Update video feed DOM element
        const videoStream = get('VIDEO_STREAM');
        if (videoStream) {
            videoStream.srcObject = window.video_feed;
            get("VIDEO_PLACEHOLDER").style.display = "none";
        }

        // Monitor for screen share stop - if user stops sharing, end interview
        videoTrack.onended = () => {
            alert('Screen sharing has stopped. The interview will now end.');
            window.location.href = "/candidate/";
        };

        // // Initialize speech recognition here
        initializeSpeechRecognition();

        // All permissions granted - show the page
        document.body.style.display = '';
        
        // Request fullscreen on user click
        document.body.onclick = () => {
            // alert("please click your screen");
            // initializeSpeechRecognition();
            document.body.requestFullscreen();
            document.body.onclick = null;
        };
    } catch (error) {
        // Permission denied or error occurred
        console.error('Permission error:', error);
        alert('Permission denied. You MUST:\n1. Share your ENTIRE SCREEN (not a window or tab)\n2. Include SYSTEM AUDIO in screen share\n3. Grant camera access\n\nAll are required to continue with the interview.');
        window.location.href = "/candidate/";
    }
}

function initializeSpeechRecognition() {
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
        console.warn('Speech recognition not supported in this browser');
        return;
    }

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    window.recognition = new SpeechRecognition();
    
    window.recognition.continuous = true;
    window.recognition.interimResults = true;
    window.recognition.lang = 'en-US';

    window.recognition.onstart = () => {
        console.log('Speech recognition started');
        window.isUserSpeaking = true;
    };

    window.recognition.onresult = (event) => {
        let interimTranscript = '';
        let finalTranscript = '';

        for (let i = event.resultIndex; i < event.results.length; i++) {
            const transcript = event.results[i][0].transcript;
            if (event.results[i].isFinal) {
                finalTranscript += transcript + ' ';
            } else {
                interimTranscript += transcript;
            }
        }

        if (finalTranscript) {
            window.speechBuffer += finalTranscript;
            window.transcribedText = window.speechBuffer.trim();
            
            // User is speaking and has transcribed text
            if (window.transcribedText.length > 0) {
                window.isUserSpeaking = true;
                // Callback to watch.js handler if available
                if (typeof handleSpeechWithCode === 'function') {
                    console.log(window.transcribedText);
                    handleSpeechWithCode();
                }
            }
        }
    };

    window.recognition.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
        
        if (event.error === 'no-speech') {
            window.isUserSpeaking = false;
        }
        
        // Don't restart on certain fatal errors
        if (event.error === 'language-not-supported' || 
            event.error === 'not-allowed' || 
            event.error === 'service-not-allowed') {
            console.warn('Speech recognition not available:', event.error);
            return;
        }
    };

    window.recognition.onend = () => {
        // Restart recognition if interview is still active
        if (document.body.style.display !== 'none') {
            try {
                window.recognition.start();
            } catch (e) {
                console.log('Recognition restart delayed');
                setTimeout(() => {
                    try {
                        window.recognition.start();
                    } catch (err) {
                        console.error('Failed to restart recognition:', err);
                    }
                }, 1000);
            }
        }
    };

    // Start speech recognition
    try {
        window.recognition.start();
        console.log('Speech recognition initialized and started');
    } catch (e) {
        console.error('Failed to start speech recognition:', e);
    }
}

// Request permissions on page load
requestPermissions();

