# Video Recording and Upload Implementation

## Overview
Implemented a complete video recording system that captures both screen share and candidate camera feeds, uploads them to Cloudflare, and stores the URLs in the database.

## Architecture

### 1. Two Separate Video Recordings
- **Screen Video**: Entire screen capture + system audio
  - Source: `window.entire_screen_feed` (from permissions.js)
  - Includes: Screen video + system audio
  - Format: video/webm (VP9 codec)
  - Bitrate: 2.5 Mbps

- **Candidate Video**: Camera feed + system audio
  - Source: `window.video_feed` (camera) + `window.audio_feed` (system audio)
  - Both videos share the same audio stream from screen capture
  - Format: video/webm (VP9 codec)
  - Bitrate: 1.5 Mbps

### 2. Recording Flow

#### Start Recording (permissions.js)
```javascript
// After permissions granted, start recording automatically
if (typeof window.startRecording === 'function') {
    window.startRecording();
}
```

#### Recording Management (recorder.js)
- `startRecording()`: Initializes two MediaRecorders
  - Screen recorder: Uses `window.entire_screen_feed`
  - Candidate recorder: Combines `window.video_feed` + `window.audio_feed`
- Data collected in chunks arrays every 1 second
- Recorders run throughout entire interview

#### End Recording (watch.js)
```javascript
// Timer expires → Mark interview complete → End interview
markInterviewCompleted().then(() => {
    endInterview();
});
```

#### Upload & Navigate (api.js → recorder.js)
```javascript
function endInterview() {
    // Call sendRecordings which:
    // 1. Stops both recorders
    // 2. Creates video blobs
    // 3. Uploads to Cloudflare
    // 4. Navigates to end page with URLs
    window.sendRecordings();
}
```

### 3. Cloudflare Upload

#### Upload Function (recorder.js)
```javascript
async function uploadToCloudflare(videoBlob, filename) {
    const response = await fetch(CLOUDFLARE_UPLOAD_URL, {
        method: 'POST',
        body: videoBlob,
        headers: {
            'Content-Type': 'video/webm'
        }
    });
    const data = await response.json();
    return data.url || data.result?.url;
}
```

#### Parallel Upload
```javascript
const [screenUrl, candidateUrl] = await Promise.all([
    uploadToCloudflare(screenBlob, 'screen_video'),
    uploadToCloudflare(candidateBlob, 'candidate_video')
]);
```

### 4. URL Persistence

#### Navigation with Query Params
```javascript
window.location.href = `/interview/end/${window.interviewId}/?screen_video=${encodeURIComponent(screenUrl)}&candidate_video=${encodeURIComponent(candidateUrl)}`;
```

#### Backend Storage (views.py)
```python
def end(request, id: int):
    # Get URLs from query parameters
    screen_video = request.GET.get('screen_video', '')
    candidate_video = request.GET.get('candidate_video', '')
    
    # Save to Interview model
    if screen_video:
        interview_obj.screen_video = screen_video
    if candidate_video:
        interview_obj.candidate_video = candidate_video
    
    interview_obj.save()
```

### 5. Interview Completion

#### Mark Complete Endpoint (views.py)
```python
@require_http_methods(["POST"])
@csrf_exempt
def end_interview_audio(request):
    # Called when timer expires
    # Sets interview.completed_at = datetime.now()
    # Saves score and feedback
    interview.completed_at = datetime.now()
    interview.save()
```

#### Frontend Call (watch.js)
```javascript
async function markInterviewCompleted() {
    const response = await fetch('/interview/api/end-interview/', {
        method: 'POST',
        body: JSON.stringify({ interview_id: window.interviewId })
    });
}
```

## Database Schema

### Interview Model (interview/models.py)
```python
class Interview(models.Model):
    screen_video = models.URLField(max_length=500, blank=True)
    candidate_video = models.URLField(max_length=500, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    score = models.PositiveIntegerField(default=0)
    notes = models.TextField(blank=True)
```

## Configuration

### TODO: Set Cloudflare URL
In `static/interview/recorder.js`:
```javascript
const CLOUDFLARE_UPLOAD_URL = 'YOUR_CLOUDFLARE_UPLOAD_URL';
```

This should be retrieved from backend or environment variable.

## Error Handling

1. **Upload Failure**: Still navigates to end page without URLs
2. **Recording Failure**: Logs error, continues interview
3. **Permission Denied**: Redirects to candidate dashboard

## Files Modified/Created

### Created:
- `static/interview/recorder.js` - Video recording and upload logic

### Modified:
- `static/interview/permissions.js` - Start recording after permissions
- `static/interview/api.js` - Call sendRecordings on end
- `static/interview/watch.js` - Mark interview complete before ending
- `interview/views.py` - Accept and save video URLs
- `templates/interview/index.html` - Include recorder.js script

## Testing Checklist

- [ ] Recording starts after permissions granted
- [ ] Both videos record simultaneously
- [ ] Videos have same audio stream
- [ ] Timer expiration marks interview complete
- [ ] Videos upload to Cloudflare successfully
- [ ] URLs saved to database
- [ ] End page loads with audio
- [ ] Graceful failure if upload fails
