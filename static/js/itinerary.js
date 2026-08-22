/**
 * Itinerary Builder - Interactive Drag, Stop & Activity Handler
 */
document.addEventListener('DOMContentLoaded', () => {
    initItineraryDragAndDrop();
});

function initItineraryDragAndDrop() {
    const items = document.querySelectorAll('.draggable-card');
    const container = document.getElementById('timeline-container');

    if (!container) return;

    items.forEach(item => {
        item.addEventListener('dragstart', () => item.classList.add('dragging'));
        item.addEventListener('dragend', () => item.classList.remove('dragging'));
    });

    container.addEventListener('dragover', (e) => {
        e.preventDefault();
        const afterElement = getDragAfterElement(container, e.clientY);
        const draggable = document.querySelector('.dragging');
        if (!draggable) return;

        if (afterElement == null) {
            container.appendChild(draggable);
        } else {
            container.insertBefore(draggable, afterElement);
        }
    });
}

function getDragAfterElement(container, y) {
    const draggableElements = [...container.querySelectorAll('.draggable-card:not(.dragging)')];

    return draggableElements.reduce((closest, child) => {
        const box = child.getBoundingClientRect();
        const offset = y - box.top - box.height / 2;
        if (offset < 0 && offset > closest.offset) {
            return { offset: offset, element: child };
        } else {
            return closest;
        }
    }, { offset: Number.NEGATIVE_INFINITY }).element;
}

// Dynamic Activity Addition Callback
window.addActivityToStop = function(stopId, activityName, cost) {
    window.showToast(`Added ${activityName} ($${cost}) to Stop`);
    // Trigger recalculation if budget.js is loaded
    if (window.recalculateBudget) window.recalculateBudget();
};