/**
 * Real-time Debounced Search Handler for Cities & Activities
 */
let debounceTimer;

window.handleCitySearch = function(inputElement) {
    clearTimeout(debounceTimer);
    const query = inputElement.value.trim();

    if (query.length < 2) return;

    debounceTimer = setTimeout(() => {
        fetch(`/search/cities/api?q=${encodeURIComponent(query)}`)
            .then(res => res.json())
            .then(data => renderSearchResults(data))
            .catch(err => console.error('Error fetching cities:', err));
    }, 300);
};

function renderSearchResults(results) {
    const resultsContainer = document.getElementById('search-results-list');
    if (!resultsContainer) return;

    if (results.length === 0) {
        resultsContainer.innerHTML = `<p class="text-sm text-slate-500">No destinations found matching your query.</p>`;
        return;
    }

    resultsContainer.innerHTML = results.map(city => `
        <div class="p-3 border rounded-lg hover:bg-slate-50 flex justify-between items-center">
            <div>
                <p class="font-bold text-sm">${city.name}, ${city.country}</p>
                <p class="text-xs text-slate-400">Est. Daily Cost: $${city.avg_daily_cost}</p>
            </div>
            <button onclick="addStop('${city.id}')" class="bg-blue-600 text-white text-xs px-3 py-1.5 rounded">+ Add Stop</button>
        </div>
    `).join('');
}