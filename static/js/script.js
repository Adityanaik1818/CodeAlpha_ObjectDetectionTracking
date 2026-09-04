// Function to poll the Flask /api/stats route every second
function updateDashboardStats() {
    fetch('/api/stats')
        .then(response => response.json())
        .then(data => {
            // Update FPS, Detections, and Unique Objects
            document.getElementById('fps-val').innerText = data.fps;
            document.getElementById('det-val').innerText = data.current_detections;
            document.getElementById('unique-val').innerText = data.unique_objects;
            
            // Update the Status badge dynamically
            const statusEl = document.getElementById('status-val');
            if (data.active) {
                statusEl.innerHTML = '<span style="color: #22c55e; font-weight: bold;">🟢 Online</span>';
            } else {
                statusEl.innerHTML = '<span style="color: #ef4444; font-weight: bold;">🔴 Offline</span>';
            }
        })
        .catch(error => {
            console.error('Error fetching statistics:', error);
            const statusEl = document.getElementById('status-val');
            statusEl.innerHTML = '<span style="color: #ef4444; font-weight: bold;">🔴 Offline</span>';
        });
}

// Run the update function every 1000ms (1 second)
setInterval(updateDashboardStats, 1000);

// Run immediately on page load
window.onload = updateDashboardStats;