/**
 * Dynamic Budget Recalculator and Cost Breakdown Calculator
 */
window.recalculateBudget = function() {
    const activityCosts = Array.from(document.querySelectorAll('[data-activity-cost]'))
        .reduce((sum, el) => sum + parseFloat(el.getAttribute('data-activity-cost') || 0), 0);

    const lodgingCosts = parseFloat(document.getElementById('lodging-total')?.innerText.replace('$', '') || 0);
    const transportCosts = parseFloat(document.getElementById('transport-total')?.innerText.replace('$', '') || 0);

    const total = activityCosts + lodgingCosts + transportCosts;

    const totalDisplay = document.getElementById('total-budget-display');
    if (totalDisplay) {
        totalDisplay.innerText = `$${total.toFixed(2)}`;
    }

    // Budget Limit Alert Handler
    const targetLimit = parseFloat(document.getElementById('target-budget-limit')?.value || 0);
    if (targetLimit > 0 && total > targetLimit) {
        window.showToast('Warning: Your itinerary exceeds your set budget limit!', 'error');
    }
};