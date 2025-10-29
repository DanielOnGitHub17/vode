// Wait for DOM to load
document.addEventListener("DOMContentLoaded", () => {
    // Get elements
    const audio = document.getElementById("END_AUDIO");
    const outerCircle = document.getElementById("outer-circle");
    const innerCircle = document.getElementById("inner-circle");
    const endButton = document.getElementById("end-button");
    const endButtonContainer = document.getElementById("end-button-container");
    const circlesContainer = document.getElementById("circles-container");

    // Handle End button click
    endButton.addEventListener("click", () => {
        // Hide button, show circles
        endButtonContainer.classList.add("hidden");
        circlesContainer.classList.remove("hidden");

        // Start audio
        audio.play();

        // Start simple pulse animation
        animateCircles();
    });

    // Simple pulse animation
    function animateCircles() {
        let time = 0;

        function pulse() {
            requestAnimationFrame(pulse);
            time += 0.05;

            // Outer circle - slow pulse
            const outerScale = 1 + Math.sin(time) * 0.1;
            outerCircle.style.transform = `scale(${outerScale})`;

            // Inner circle - faster pulse
            const innerScale = 1 + Math.sin(time * 1.5) * 0.15;
            innerCircle.style.transform = `scale(${innerScale})`;
        }

        pulse();
    }

    // Audio event listeners
    audio.addEventListener("ended", () => {
        // Redirect 3 seconds after audio ends
        setTimeout(() => {
            window.location.href = "/candidate/";
        }, 3000);
    });

    audio.addEventListener("error", (e) => {
        console.error("Audio playback error:", e);
        // Redirect after 3 seconds on error
        setTimeout(() => {
            window.location.href = "/candidate/";
        }, 3000);
    });
});
