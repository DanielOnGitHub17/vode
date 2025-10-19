function endInterview() {
    // Disable code editor
    const codeEditor = get("CODE_EDITOR");
    if (codeEditor) {
        codeEditor.style.pointerEvents = 'none';
        codeEditor.style.opacity = '0.5';
    }

    // Show timeout message
    alert('Time is up! Your interview has ended.');
    
    // Redirect to interview end page
    let url = window.location.path.split('/')
    window.location.href = `/interview/end/${url[url.length - 1]}`;
}