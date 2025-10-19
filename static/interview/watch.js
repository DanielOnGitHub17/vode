// TIMER_BADGE
/*
Timer Watch:
- TIMER_BADGE contains the time duration in its text content
- data-started-time contains when the interview started
- Add 30 seconds grace period to the duration
- When total time expires, call endInterview() to end the interview
*/

const TIMER_BADGE = get('TIMER_BADGE');

// Parse the duration and start time
function initializeTimer() {
    const timerText = TIMER_BADGE.textContent.trim(); // e.g., "60:00" or "01:30:00"
    const startedTime = TIMER_BADGE.getAttribute('data-started-time'); // ISO timestamp
    
    // Parse timer duration to seconds
    const timeParts = timerText.split(':').map(Number);
    let durationSeconds;
    
    if (timeParts.length === 2) {
        // MM:SS format
        durationSeconds = (timeParts[0] * 60) + timeParts[1];
    } else if (timeParts.length === 3) {
        // HH:MM:SS format
        durationSeconds = (timeParts[0] * 3600) + (timeParts[1] * 60) + timeParts[2];
    } else {
        console.error('Invalid timer format:', timerText);
        return;
    }
    
    // Add 30 seconds grace period
    const totalDurationSeconds = durationSeconds + 30;
    
    // Calculate end time
    const startTime = new Date(startedTime).getTime();
    const endTime = startTime + (totalDurationSeconds * 1000);
    
    // Start the countdown
    startCountdown(endTime);
}

function startCountdown(endTime) {
    const interval = setInterval(() => {
        const now = Date.now();
        const remainingMs = endTime - now;
        
        if (remainingMs <= 0) {
            // Time's up!
            clearInterval(interval);
            TIMER_BADGE.textContent = '00:00';
            TIMER_BADGE.classList.remove('bg-primary');
            TIMER_BADGE.classList.add('bg-danger');
            
            // End the interview
            endInterview();
        } else {
            // Update timer display
            const totalSeconds = Math.floor(remainingMs / 1000);
            const hours = Math.floor(totalSeconds / 3600);
            const minutes = Math.floor((totalSeconds % 3600) / 60);
            const seconds = totalSeconds % 60;
            
            let displayTime;
            if (hours > 0) {
                displayTime = `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
            } else {
                displayTime = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
            }
            
            TIMER_BADGE.textContent = displayTime;
            
            // Change color when less than 5 minutes remaining
            if (totalSeconds <= 300 && totalSeconds > 0) {
                TIMER_BADGE.classList.remove('bg-primary');
                TIMER_BADGE.classList.add('bg-warning');
            }
        }
    }, 1000); // Update every second
}


// Initialize timer when page loads
onload = () => {
    if (TIMER_BADGE) {
        initializeTimer();
    } else {
        console.error('TIMER_BADGE element not found');
    }
}
