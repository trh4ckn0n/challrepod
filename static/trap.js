fetch("/ping", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ user: navigator.userAgent })
});
