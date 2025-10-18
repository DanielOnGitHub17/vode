// Windows.js - Manages detached windows and taskbar
class WindowManager {
    constructor() {
        this.windows = {
            interviewer: {
                element: get('INTERVIEWER_WINDOW'),
                taskbarIcon: get('TASKBAR_INTERVIEWER'),
                isMinimized: false
            },
            video: {
                element: get('VIDEO_WINDOW'),
                taskbarIcon: get('TASKBAR_VIDEO'),
                isMinimized: false
            },
            chat: {
                element: get('CHAT_WINDOW'),
                taskbarIcon: get('TASKBAR_CHAT'),
                isMinimized: true  // Start minimized
            }
        };

        this.draggedWindow = null;
        this.dragOffset = { x: 0, y: 0 };
        
        this.init();
    }

    init() {
        // Setup taskbar icons
        Object.keys(this.windows).forEach(key => {
            const win = this.windows[key];
            
            // Taskbar icon click - toggle minimize/restore
            win.taskbarIcon.addEventListener('click', () => this.toggle(key));
            
            // Make draggable
            this.makeDraggable(win.element);
            
            // Set initial taskbar icon state
            if (win.isMinimized) {
                win.taskbarIcon.classList.add('minimized');
            }
        });

        // Setup global mouse events for dragging
        document.addEventListener('mousemove', (e) => this.onMouseMove(e));
        document.addEventListener('mouseup', () => this.onMouseUp());
    }

    toggle(windowKey) {
        const win = this.windows[windowKey];
        if (win.isMinimized) {
            this.restore(windowKey);
        } else {
            this.minimize(windowKey);
        }
    }

    minimize(windowKey) {
        const win = this.windows[windowKey];
        win.element.classList.remove('active');
        win.element.classList.add('hidden');
        win.taskbarIcon.classList.add('minimized');
        win.isMinimized = true;
    }

    restore(windowKey) {
        const win = this.windows[windowKey];
        win.element.classList.remove('hidden');
        win.element.classList.add('active');
        win.taskbarIcon.classList.remove('minimized');
        win.isMinimized = false;
    }

    makeDraggable(windowElement) {
        // Special handling for interviewer window - make entire window draggable
        const isInterviewer = windowElement.id === 'INTERVIEWER_WINDOW';
        const dragTarget = isInterviewer ? windowElement : windowElement.querySelector('.window-header');
        
        dragTarget.addEventListener('mousedown', (e) => {
            // For non-interviewer windows, don't drag if clicking buttons
            if (!isInterviewer) {
                const isButton = e.target.tagName === 'BUTTON' || e.target.closest('button');
                if (isButton) return;
            }
            
            // Prevent text selection during drag
            e.preventDefault();
            
            this.draggedWindow = windowElement;
            const rect = windowElement.getBoundingClientRect();
            this.dragOffset.x = e.clientX - rect.left;
            this.dragOffset.y = e.clientY - rect.top;
            
            // Visual feedback
            windowElement.style.cursor = 'grabbing';
            windowElement.style.userSelect = 'none';
        });
    }

    onMouseMove(e) {
        if (!this.draggedWindow) return;
        
        const newX = e.clientX - this.dragOffset.x;
        const newY = e.clientY - this.dragOffset.y;
        
        // Keep window within viewport bounds
        const maxX = window.innerWidth - this.draggedWindow.offsetWidth;
        const maxY = window.innerHeight - this.draggedWindow.offsetHeight;
        
        this.draggedWindow.style.left = Math.max(0, Math.min(newX, maxX)) + 'px';
        this.draggedWindow.style.top = Math.max(0, Math.min(newY, maxY)) + 'px';
    }

    onMouseUp() {
        if (this.draggedWindow) {
            this.draggedWindow.style.cursor = '';
            this.draggedWindow.style.userSelect = '';
            this.draggedWindow = null;
        }
    }
}

// Export for use in page.js
window.WindowManager = WindowManager;
