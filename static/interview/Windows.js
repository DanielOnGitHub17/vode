// Windows.js - Manages detached windows and taskbar
class WindowManager {
    constructor() {
        this.windows = {
            interviewer: {
                element: get("INTERVIEWER_WINDOW"),
                taskbarIcon: get("TASKBAR_INTERVIEWER"),
                isMinimized: false,
                zIndex: 1100
            },
            video: {
                element: get("VIDEO_WINDOW"),
                taskbarIcon: get("TASKBAR_VIDEO"),
                isMinimized: false,
                zIndex: 1000
            },
            chat: {
                element: get("CHAT_WINDOW"),
                taskbarIcon: get("TASKBAR_CHAT"),
                isMinimized: true,  // Start minimized
                zIndex: 999
            }
        };

        this.isDragging = false;
        this.draggedWindow = null;
        this.dragOffset = { x: 0, y: 0 };
        this.focusedWindow = null;
        this.nextZIndex = 2000;  // Start high to avoid conflicts
        
        // Bind methods to preserve "this" context
        this.onMouseDown = this.onMouseDown.bind(this);
        this.onMouseMove = this.onMouseMove.bind(this);
        this.onMouseUp = this.onMouseUp.bind(this);
        
        this.init();
    }

    init() {
        // Setup taskbar icons and dragging
        Object.keys(this.windows).forEach(key => {
            const win = this.windows[key];
            
            // Taskbar icon click handler
            win.taskbarIcon.addEventListener("click", () => this.toggle(key));            
            
            // Make draggable
            this.makeDraggable(win.element);
            
            // Set initial state
            if (win.isMinimized) {
                win.taskbarIcon.classList.add("minimized");
            }
        });

        // Global mouse events for dragging
        document.addEventListener("mousemove", this.onMouseMove);
        document.addEventListener("mouseup", this.onMouseUp);
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
        win.element.classList.remove("active");
        win.element.classList.add("hidden");
        win.taskbarIcon.classList.add("minimized");
        win.isMinimized = true;
    }

    restore(windowKey) {
        const win = this.windows[windowKey];
        win.element.classList.remove("hidden");
        win.element.classList.add("active");
        win.taskbarIcon.classList.remove("minimized");
        win.isMinimized = false;
    }

    makeDraggable(windowElement) {
        if (!windowElement) {
            console.error("[WindowManager] Cannot make null element draggable");
            return;
        }

        // Get the drag handle (the header)
        const handle = windowElement.querySelector(".window-header");
        if (!handle) {
            console.error(`[WindowManager] No .window-header found in ${windowElement.id}`);
            return;
        }

        // Attach mousedown to the handle
        handle.addEventListener("mousedown", (e) => this.onMouseDown(e, windowElement));
        
        // Also focus window on any click inside it
        windowElement.addEventListener("mousedown", () => this.focusWindow(windowElement));
        
        console.log(`[WindowManager] Made ${windowElement.id} draggable`);
    }

    focusWindow(windowElement) {
        // Remove focus from previously focused window
        if (this.focusedWindow && this.focusedWindow !== windowElement) {
            this.focusedWindow.classList.remove("focused");
        }

        // Focus the clicked window
        this.focusedWindow = windowElement;
        windowElement.classList.add("focused");
        
        // Bring to front by updating z-index
        windowElement.style.zIndex = this.nextZIndex++;
        
        console.log(`[WindowManager] Focused: ${windowElement.id}`);
    }

    onMouseDown(e, windowElement) {
        // Don't drag if clicking buttons
        if (e.target.tagName === "BUTTON" || e.target.closest("button")) {
            return;
        }

        // Focus this window
        this.focusWindow(windowElement);

        e.preventDefault();
        
        this.isDragging = true;
        this.draggedWindow = windowElement;

        const rect = windowElement.getBoundingClientRect();
        this.dragOffset.x = e.clientX - rect.left;
        this.dragOffset.y = e.clientY - rect.top;

        // Clear any right/bottom positioning so left/top can take over
        windowElement.style.right = "auto";
        windowElement.style.bottom = "auto";

        // Set initial left/top based on current position
        windowElement.style.left = rect.left + "px";
        windowElement.style.top = rect.top + "px";

        // Visual feedback
        windowElement.style.cursor = "grabbing";
        windowElement.style.userSelect = "none";

        console.log(`[WindowManager] Drag started: ${windowElement.id}`);
    }

    onMouseMove(e) {
        if (!this.isDragging || !this.draggedWindow) return;

        const newX = e.clientX - this.dragOffset.x;
        const newY = e.clientY - this.dragOffset.y;

        // Keep window within viewport bounds
        const maxX = window.innerWidth - this.draggedWindow.offsetWidth;
        const maxY = window.innerHeight - this.draggedWindow.offsetHeight;

        const constrainedX = Math.max(0, Math.min(newX, maxX));
        const constrainedY = Math.max(0, Math.min(newY, maxY));

        this.draggedWindow.style.left = constrainedX + "px";
        this.draggedWindow.style.top = constrainedY + "px";
    }

    onMouseUp() {
        if (!this.isDragging) return;

        this.isDragging = false;
        if (this.draggedWindow) {
            this.draggedWindow.style.cursor = "grab";
            this.draggedWindow.style.userSelect = "";
            this.draggedWindow = null;
        }

        console.log("[WindowManager] Drag ended");
    }
}

// Export for use in page.js
window.WindowManager = WindowManager;
