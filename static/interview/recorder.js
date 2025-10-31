// Video recording management
let screenRecorder = null;
let candidateRecorder = null;
let screenChunks = [];
let candidateChunks = [];

// Cloudflare upload URL (set this from backend or env)
const CLOUDFLARE_API_KEY = "hi_tehre_this_fake"
const CLOUDFLARE_ACCOUNT_ID = "another_fake" // TODO: Get from backend
const CLOUDFLARE_UPLOAD_URL = `https://api.cloudflare.com/client/v4/accounts/${CLOUDFLARE_ACCOUNT_ID}/stream`

// Listen for streams ready event from permissions.js
document.addEventListener("streamsReady", (event) => {
    console.log("Received streamsReady event, starting recording...");
    const { screenStream, videoStream, audioStream } = event.detail;
    startRecording();
});

function startRecording() {
    // Use EXISTING streams from permissions.js - don't create new ones!
    
    // Create MediaRecorder for screen (already has video + system audio)
    if (window.entire_screen_feed) {
        try {
            screenRecorder = new MediaRecorder(window.entire_screen_feed, {
                mimeType: "video/webm;codecs=vp9",
                videoBitsPerSecond: 1500000 // 1.5 Mbps
            });

            screenRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    screenChunks.push(event.data);
                }
            };

            screenRecorder.start(1000); // Collect data every second
            console.log("Screen recording started with existing stream");
        } catch (error) {
            console.error("Failed to start screen recorder:", error);
        }
    } else {
        console.error("No entire_screen_feed available from permissions");
    }

    // Create MediaRecorder for candidate video (already has camera + shared audio)
    if (window.video_feed && window.audio_feed) {
        try {
            // Combine candidate video with system audio (both already exist from permissions.js)
            const candidateStream = new MediaStream([
                ...window.video_feed.getVideoTracks(),
                ...window.audio_feed.getAudioTracks()
            ]);

            candidateRecorder = new MediaRecorder(candidateStream, {
                mimeType: "video/webm;codecs=vp9",
                videoBitsPerSecond: 800000 // 800 Kbps
            });

            candidateRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    candidateChunks.push(event.data);
                }
            };

            candidateRecorder.start(1000);
            console.log("Candidate recording started with existing stream");
        } catch (error) {
            console.error("Failed to start candidate recorder:", error);
        }
    } else {
        console.error("No video_feed or audio_feed available from permissions");
    }
}

function stopRecording() {
    return new Promise((resolve) => {
        let stoppedCount = 0;
        const totalRecorders = 2;

        const checkComplete = () => {
            stoppedCount++;
            if (stoppedCount === totalRecorders) {
                resolve();
            }
        };

        if (screenRecorder && screenRecorder.state !== "inactive") {
            screenRecorder.onstop = () => {
                console.log("Screen recording stopped");
                checkComplete();
            };
            screenRecorder.stop();
        } else {
            checkComplete();
        }

        if (candidateRecorder && candidateRecorder.state !== "inactive") {
            candidateRecorder.onstop = () => {
                console.log("Candidate recording stopped");
                checkComplete();
            };
            candidateRecorder.stop();
        } else {
            checkComplete();
        }
    });
}

async function uploadToCloudflare(videoBlob, filename) {
    try {
        // Create form data for Cloudflare Stream upload
        const formData = new FormData();
        formData.append("file", videoBlob, `${filename}.webm`);
        
        const response = await fetch(CLOUDFLARE_UPLOAD_URL, {
            method: "POST",
            body: formData,
            headers: {
                "Authorization": `Bearer ${CLOUDFLARE_API_KEY}`
            }
        });

        if (!response.ok) {
            throw new Error(`Upload failed: ${response.status} ${response.statusText}`);
        }

        const data = await response.json();
        console.log(`${filename} upload complete:`, data);
        
        // Cloudflare Stream returns the video URL in result.playback.hls
        const videoUrl = data.result?.playback?.hls || data.result?.preview || null;
        return videoUrl;
    } catch (error) {
        console.error(`Error uploading ${filename}:`, error);
        throw error;
    }
}

async function sendRecordings() {
    console.log("Stopping recordings...");
    await stopRecording();

    console.log("Creating video blobs...");
    const screenBlob = new Blob(screenChunks, { type: "video/webm" });
    const candidateBlob = new Blob(candidateChunks, { type: "video/webm" });

    console.log(`Screen video size: ${(screenBlob.size / 1024 / 1024).toFixed(2)} MB`);
    console.log(`Candidate video size: ${(candidateBlob.size / 1024 / 1024).toFixed(2)} MB`);

    try {
        console.log("Uploading videos to Cloudflare...");
        
        const [screenUrl, candidateUrl] = await Promise.all([
            uploadToCloudflare(screenBlob, "screen_video"),
            uploadToCloudflare(candidateBlob, "candidate_video")
        ]);

        console.log("Upload complete!");
        console.log("Screen URL:", screenUrl);
        console.log("Candidate URL:", candidateUrl);

        // Navigate to end page with video URLs
        window.location.href = `/interview/end/${window.interviewId}/?screen_video=${encodeURIComponent(screenUrl)}&candidate_video=${encodeURIComponent(candidateUrl)}`;
    } catch (error) {
        console.error("Failed to upload videos:", error);
        alert("Failed to upload interview recordings. Please contact support.");
        // Still navigate to end page even if upload fails
        window.location.href = `/interview/end/${window.interviewId}/`;
    }
}

// Export functions for use in other files
window.startRecording = startRecording;
window.stopRecording = stopRecording;
window.sendRecordings = sendRecordings;
