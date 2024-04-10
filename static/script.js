// script.js
document.addEventListener('DOMContentLoaded', function() {
    // Fetch browser history data and render graph
    fetch('/get_browser_history')
        .then(response => response.json())
        .then(data => {
            // Process data and render graph using a library like Chart.js or D3.js
        })
        .catch(error => console.error('Error fetching browser history:', error));
});
