// Hide page body initially
document.body.style.display = 'none';

// Global storage for media streams
window.entire_screen_feed = null;
window.video_feed = null;
window.audio_feed = null;

async function requestPermissions() {
    try {
        // Request screen capture with audio
        window.entire_screen_feed = await navigator.mediaDevices.getDisplayMedia({
            video: true,
            audio: true
        });

        // Request user camera feed
        window.video_feed = await navigator.mediaDevices.getUserMedia({
            video: true,
            audio: false
        });

        // Request user audio feed
        window.audio_feed = await navigator.mediaDevices.getUserMedia({
            audio: true,
            video: false
        });

        // All permissions granted - show the page
        document.body.style.display = '';
        
    } catch (error) {
        // Permission denied or error occurred
        alert('Permission denied. You must grant screen sharing and camera/microphone access to continue with the interview.');
        window.location.href = '/candidate/';
    }
}

// Request permissions on page load
requestPermissions();
