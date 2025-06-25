const beaconUrl = atob("aHR0cHM6Ly9jaGFsbHJlcG9kLm9ucmVuZGVyLmNvbS9waW5n");

fetch(beaconUrl, {
  method: "POST",
  body: JSON.stringify({ user: "anonymous", time: Date.now() }),
  headers: { "Content-Type": "application/json" }
})
.then(res => {
  if (res.ok) {
    document.getElementById("status").textContent = "✅ Connexion établie.";
    setTimeout(() => {
      window.location.href = "/redir";
    }, 2000);
  } else {
    document.getElementById("status").textContent = "⚠️ Serveur distant indisponible.";
  }
})
.catch((err) => {
  console.error(err);
  document.getElementById("status").textContent = "❌ Échec de connexion.";
});
