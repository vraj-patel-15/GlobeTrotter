/**
 * Lightweight Dynamic Calendar & Timeline Renderer
 */
document.addEventListener('DOMContentLoaded', () => {
    const calendarContainer = document.getElementById('calendar-grid');
    if (calendarContainer) {
        renderTripCalendar(calendarContainer);
    }
});

function renderTripCalendar(container) {
    const daysInMonth = 30; // Sample render cycle
    let html = '';

    for (let day = 1; day <= daysInMonth; day++) {
        html += `
            <div class="border border-slate-200 rounded-lg p-2 min-h-[80px] bg-white hover:border-blue-400 transition">
                <span class="text-xs font-bold text-slate-400">${day}</span>
                <div class="mt-1" id="day-events-${day}"></div>
            </div>
        `;
    }
    container.innerHTML = html;
}