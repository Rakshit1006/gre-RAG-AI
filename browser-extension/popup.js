// Check if backend is running
async function checkBackendStatus() {
  const statusEl = document.getElementById('status');
  
  try {
    const response = await fetch('http://localhost:8000/health');
    if (response.ok) {
      statusEl.textContent = '✓ Connected to GRE Mentor';
      statusEl.className = 'status connected';
    } else {
      throw new Error('Backend not responding');
    }
  } catch (error) {
    statusEl.textContent = '✗ Backend not running. Start the server.';
    statusEl.className = 'status disconnected';
  }
}

checkBackendStatus();
