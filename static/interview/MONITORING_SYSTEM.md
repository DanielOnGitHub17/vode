# Interview Monitoring System

## Overview
The interview monitoring system tracks all user activity during a technical interview, including code changes, speech transcription, and chat messages. This data is sent to the backend for AI analysis and interview evaluation.

## Components

### 1. watch.js - Main Monitoring System

#### Timer Management
- Reads interview duration from `TIMER_BADGE` element
- Adds 30-second grace period
- Displays countdown timer
- Changes color at 5 minutes remaining (warning)
- Triggers `endInterview()` when time expires

#### Speech Recognition
- Uses Web Speech API (`SpeechRecognition` or `webkitSpeechRecognition`)
- Continuous recognition with interim results
- Automatically restarts if stopped
- Buffers transcribed text
- Sets `isUserSpeaking` flag

#### Monaco Editor Monitoring
- **Keystroke Counting**: Tracks number of keystrokes
- **Silent Typing Detection**: After 50 keystrokes without speech, sends code
- **Debounced Sending**: Sends code 2 seconds after user stops typing
- **Periodic Updates**: Sends code every 10 seconds during active typing
- **Cursor Tracking**: Monitors cursor position and selection changes

#### Chat Monitoring
- Listens for Enter key and Send button clicks
- Sends chat messages with code context
- Prevents duplicate message sending

## Configuration Constants

```javascript
const COUNT_TO_CHECK = 50;        // Keystroke threshold for silent typing
const CODE_SEND_INTERVAL = 10000; // Send code every 10 seconds (10000ms)
const DEBOUNCE_DELAY = 2000;      // Wait 2 seconds after last keystroke
```

## Decision Logic

### When to Call `sendTextCode(transcribedText, code)`
- User is speaking AND typing/coding
- Both speech transcription and code are available
- **Purpose**: Capture candidate explaining their code verbally

### When to Call `sendCode(code)`
- User has typed 50 times without speaking (silent typing)
- User has paused typing for 2 seconds (debounced)
- Periodic interval (every 10 seconds) during active typing
- **Purpose**: Track code progress without verbal explanation

### When to Call `sendText(text, code)`
- User sends a chat message
- Includes current code as context
- **Purpose**: Track written questions/communication

## API Functions (api.js)

### Core Functions

#### `sendTextCode(transcribedText, code)`
Sends speech transcription with code when user is explaining verbally.

**Parameters:**
- `transcribedText` (string): Speech-to-text output
- `code` (string): Current code in editor

**Backend Endpoint:** `POST /api/interview/activity/`
```json
{
  "type": "speech_and_code",
  "transcribed_text": "I'm using a hash map to store...",
  "code": "def twoSum(nums, target):\n...",
  "timestamp": 1698765432000
}
```

#### `sendCode(code)`
Sends code when user is typing silently.

**Parameters:**
- `code` (string): Current code in editor

**Backend Endpoint:** `POST /api/interview/activity/`
```json
{
  "type": "code_only",
  "code": "def twoSum(nums, target):\n...",
  "timestamp": 1698765432000
}
```

#### `sendText(text, code)`
Sends chat message with code context.

**Parameters:**
- `text` (string): Chat message
- `code` (string): Current code (optional context)

**Backend Endpoint:** `POST /api/interview/activity/`
```json
{
  "type": "chat_message",
  "text": "Can I use a hash map here?",
  "code": "def twoSum(nums, target):\n...",
  "timestamp": 1698765432000
}
```

#### `sendRecordings(screenStream, videoStream, audioStream)`
Uploads screen, camera, and audio recordings at interview end.

**Parameters:**
- `screenStream` (MediaStream): Screen capture
- `videoStream` (MediaStream): Camera feed
- `audioStream` (MediaStream): Microphone audio

**Backend Endpoint:** `POST /api/interview/recordings/`

#### `sendHeartbeat()`
Periodic heartbeat to track active interview session.

**Backend Endpoint:** `POST /api/interview/heartbeat/`
```json
{
  "timestamp": 1698765432000,
  "status": "active"
}
```

#### `submitInterview(finalCode, duration)`
Final submission when interview completes.

**Parameters:**
- `finalCode` (string): Final code submission
- `duration` (number): Total duration in seconds

**Backend Endpoint:** `POST /api/interview/submit/`
```json
{
  "final_code": "def twoSum(nums, target):\n...",
  "duration": 2730,
  "timestamp": 1698765432000
}
```

## State Variables

```javascript
let keystrokeCount = 0;      // Tracks keystrokes since last reset
let lastCodeContent = '';    // Prevents duplicate code sends
let lastChatMessage = '';    // Prevents duplicate chat messages
let isUserSpeaking = false;  // Whether speech is detected
let codeSendTimer = null;    // Interval for periodic code sending
let debounceTimer = null;    // Timeout for debounced typing pause
let recognition = null;      // SpeechRecognition instance
let transcribedText = '';    // Current transcription
let speechBuffer = '';       // Accumulated speech text
```

## Event Flow

### Scenario 1: User Speaks While Coding
1. Speech recognition detects speech → `recognition.onresult`
2. `isUserSpeaking = true`
3. `transcribedText` is updated
4. User types in editor → `editor.onDidChangeModelContent`
5. `handleSpeechWithCode()` called
6. `sendTextCode(transcribedText, code)` sends data to backend

### Scenario 2: Silent Typing (50+ keystrokes)
1. User types without speaking
2. `keystrokeCount` increments on each keystroke
3. When `keystrokeCount >= 50` AND `!isUserSpeaking`
4. `handleSilentTyping()` called
5. `sendCode(code)` sends code to backend
6. `keystrokeCount` resets to 0

### Scenario 3: Typing Pause
1. User stops typing
2. `debounceTimer` starts (2 seconds)
3. If no more keystrokes in 2 seconds
4. `handleTypingPause()` called
5. `sendCode(code)` sends code to backend

### Scenario 4: Chat Message
1. User types in chat input
2. Presses Enter or clicks Send button
3. `handleChatMessage()` called
4. `sendText(message, code)` sends with code context

### Scenario 5: Timer Expires
1. Countdown reaches 00:00
2. `endInterview()` called
3. `cleanupMonitoring()` stops all listeners
4. Code editor disabled
5. Redirect to `/interview/end/{id}/`

## Cleanup

### `cleanupMonitoring()`
Called when interview ends to stop all monitoring:
- Stops speech recognition
- Clears `codeSendTimer` interval
- Clears `debounceTimer` timeout
- Prevents memory leaks

### Override Pattern
```javascript
const originalEndInterview = window.endInterview;
window.endInterview = function() {
    cleanupMonitoring();
    if (originalEndInterview) {
        originalEndInterview();
    }
};
```

## Browser Compatibility

### Speech Recognition
- ✅ Chrome/Edge: `webkitSpeechRecognition`
- ✅ Chrome/Edge (newer): `SpeechRecognition`
- ❌ Firefox: Not supported (fallback: no speech tracking)
- ❌ Safari: Limited support

### Media Capture
- ✅ All modern browsers with HTTPS or localhost
- Requires user permission for camera/microphone/screen

## Security Considerations

1. **HTTPS Required**: Media capture and speech recognition require secure context
2. **User Permissions**: Must request and receive permission for camera/mic/screen
3. **Data Privacy**: All transcriptions and code sent to backend should be encrypted
4. **Session Validation**: Backend must verify interview session is valid

## Future Enhancements

- [ ] Add silence detection to pause speech recognition
- [ ] Implement local recording with MediaRecorder API
- [ ] Add code diff tracking (only send changes, not full code)
- [ ] Compress data before sending
- [ ] Add offline queue for failed API calls
- [ ] Visual feedback for when data is being sent
- [ ] Add "test microphone" feature before interview starts
- [ ] Track test case executions and results
