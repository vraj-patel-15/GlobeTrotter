/**
 * Main Application Core JS - Global State & Utilities
 */
document.addEventListener('DOMContentLoaded', () => {
    initApp();
});

function initApp() {
    console.log('GlobalTrotters initialized.');
    setupGlobalNavigation();
}

// Global Toast Notification Helper
window.showToast = function(message, type = 'info') {
    const toast = document.createElement('div');
    const bgClass = type === 'error' ? 'bg-red-600' : 'bg-slate-900';
    toast.className = `fixed bottom-5 right-5 ${bgClass} text-white text-sm px-4 py-3 rounded-lg shadow-lg z-50 fade-in transition-all`;
    toast.innerText = message;
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.style.opacity = '0';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
};

// Global Active Link Highlighting
function setupGlobalNavigation() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('nav a');
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('text-blue-600', 'font-bold');
            link.classList.remove('text-slate-600');
        }
    });
}