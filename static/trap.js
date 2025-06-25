console.log("Trap JS loaded! Sending beacon...");

fetch('/ping', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ user: "trap.js" })
})
.then(response => response.json())
.then(data => console.log("Ping status:", data.status))
.catch(err => console.error("Ping error:", err));
