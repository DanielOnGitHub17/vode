# Screen Sharing & Audio Configuration

## Summary of Changes

### ✅ Enforcement of Entire Screen Sharing
The interview platform now **requires** candidates to:
1. Share their **entire screen** (not a window or tab)
2. Include **system audio** in the screen share
3. Grant **camera access**

Any failure to meet these requirements will prevent the interview from starting.

---

## Permissions Flow

### 1. Initial Request (permissions.js)
```javascript
window.entire_screen_feed = await navigator.mediaDevices.getDisplayMedia({
    video: {
        displaySurface: 'monitor' // Force entire screen
    },
    audio: true, // Must include system audio
    preferCurrentTab: false,
    surfaceSwitching: 'exclude',
    selfBrowserSurface: 'exclude'
});
```

### 2. Verification Checks

#### ✅ Entire Screen Verification
```javascript
const settings = videoTrack.getSettings();
if (settings.displaySurface !== 'monitor') {
    throw new Error('You must share your entire screen, not a window or tab.');
}
```

**Possible values:**
- `'monitor'` - Entire screen ✅ (Required)
- `'window'` - Single window ❌ (Rejected)
- `'browser'` - Browser tab ❌ (Rejected)

#### ✅ System Audio Verification
```javascript
const audioTracks = window.entire_screen_feed.getAudioTracks();
if (audioTracks.length === 0) {
    throw new Error('You must share system audio along with your screen.');
}
```

### 3. Audio Extraction
```javascript
// Extract audio from screen share (includes system audio)
window.audio_feed = new MediaStream(audioTracks);
```

**Why this approach?**
- Screen share can include system audio (all computer sounds)
- Microphone audio is captured separately via speech recognition
- At the end, we can combine video tracks with audio tracks for recording

---

## Global Variables

### Media Streams
```javascript
window.entire_screen_feed  // MediaStream with video + system audio
window.video_feed          // MediaStream with camera video only
window.audio_feed          // MediaStream with system audio (extracted from screen share)
```

### Speech Recognition
```javascript
window.recognition         // SpeechRecognition instance
window.transcribedText     // Current transcribed text
window.speechBuffer        // Accumulated speech buffer
window.isUserSpeaking      // Boolean flag for speaking state
```

---

## Speech Recognition Setup

### Initialization (in permissions.js)
Speech recognition is initialized **once** in `permissions.js` after all permissions are granted:

```javascript
function initializeSpeechRecognition() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    window.recognition = new SpeechRecognition();
    
    window.recognition.continuous = true;
    window.recognition.interimResults = true;
    window.recognition.lang = 'en-US';
    
    // Event handlers...
    window.recognition.start();
}
```

### Auto-restart on End
```javascript
window.recognition.onend = () => {
    if (document.body.style.display !== 'none') {
        try {
            window.recognition.start();
        } catch (e) {
            setTimeout(() => {
                window.recognition.start();
            }, 1000);
        }
    }
};
```

### Callback to watch.js
When speech is detected, it calls `handleSpeechWithCode()` if available:

```javascript
window.recognition.onresult = (event) => {
    // ... process transcription
    if (window.transcribedText.length > 0) {
        window.isUserSpeaking = true;
        if (typeof handleSpeechWithCode === 'function') {
            handleSpeechWithCode();
        }
    }
};
```

---

## Integration with watch.js

### Removed Duplicate Code
- ❌ Removed `initializeSpeechRecognition()` from watch.js
- ❌ Removed local variables: `recognition`, `transcribedText`, `speechBuffer`, `isUserSpeaking`
- ✅ Now uses global `window.*` variables from permissions.js

### Updated References
```javascript
// OLD (local variables)
if (keystrokeCount >= COUNT_TO_CHECK && !isUserSpeaking) { ... }
sendTextCode(transcribedText, currentCode);

// NEW (global variables)
if (keystrokeCount >= COUNT_TO_CHECK && !window.isUserSpeaking) { ... }
sendTextCode(window.transcribedText, currentCode);
```

---

## Screen Share Monitoring

### Stop Detection
If the user stops screen sharing during the interview:

```javascript
videoTrack.onended = () => {
    alert('Screen sharing has stopped. The interview will now end.');
    window.location.href = "/candidate/";
};
```

This prevents candidates from:
- Stopping screen share to cheat
- Accidentally closing the share
- Switching to a different window

---

## Error Handling

### Clear Error Messages
```javascript
alert('Permission denied. You MUST:\n' +
      '1. Share your ENTIRE SCREEN (not a window or tab)\n' +
      '2. Include SYSTEM AUDIO in screen share\n' +
      '3. Grant camera access\n\n' +
      'All are required to continue with the interview.');
```

### Automatic Redirect
On any permission failure → redirect to `/candidate/`

---

## Recording at Interview End

### Combining Streams
At the end of the interview, you can combine the streams:

```javascript
function createFinalRecording() {
    // Video track from screen share
    const screenVideoTrack = window.entire_screen_feed.getVideoTracks()[0];
    
    // Audio track from screen share (system audio)
    const systemAudioTrack = window.audio_feed.getAudioTracks()[0];
    
    // Combine into final recording stream
    const finalStream = new MediaStream([
        screenVideoTrack,
        systemAudioTrack
    ]);
    
    // Use MediaRecorder to create video file
    const recorder = new MediaRecorder(finalStream);
    // ... handle recording
}
```

### Camera Feed
The camera feed (`window.video_feed`) is recorded separately for picture-in-picture or side-by-side display.

---

## Browser Compatibility

### getDisplayMedia Support
| Browser | displaySurface | Audio Sharing |
|---------|---------------|---------------|
| Chrome 107+ | ✅ Supported | ✅ Supported |
| Edge 107+ | ✅ Supported | ✅ Supported |
| Firefox 103+ | ⚠️ Limited | ⚠️ Limited |
| Safari 13+ | ❌ Not supported | ❌ Not supported |

### Speech Recognition Support
| Browser | SpeechRecognition |
|---------|-------------------|
| Chrome | ✅ webkitSpeechRecognition |
| Edge | ✅ webkitSpeechRecognition |
| Firefox | ❌ Not supported |
| Safari | ⚠️ Limited support |

---

## Security Considerations

1. **HTTPS Required**: All media APIs require secure context (HTTPS or localhost)
2. **User Permissions**: Browser prompts user for each permission
3. **Verification**: Server-side must verify recordings are valid
4. **Privacy**: System audio captures all computer sounds (music, notifications, etc.)
5. **Monitoring**: Active screen share monitoring prevents cheating

---

## Testing Checklist

- [ ] Test with entire screen selection (should pass)
- [ ] Test with window selection (should fail)
- [ ] Test with tab selection (should fail)
- [ ] Test without system audio checkbox (should fail)
- [ ] Test stopping screen share mid-interview (should redirect)
- [ ] Test speech recognition activation
- [ ] Test camera feed display
- [ ] Verify all global variables are accessible
- [ ] Verify watch.js receives speech callbacks

---

## Future Enhancements

- [ ] Visual indicator when speech is being transcribed
- [ ] Visual indicator when system audio is active
- [ ] Warn user if system audio level is too low
- [ ] Allow re-requesting permissions if accidentally denied
- [ ] Add "test permissions" button before interview starts
- [ ] Display current screen share status in UI
