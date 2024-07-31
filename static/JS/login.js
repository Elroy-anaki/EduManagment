function onLogin() {
  fetch("/api/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      email: document.getElementById("email").value,
      password: document.getElementById("password").value,
    }),
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      if (data.status === "success") {
        window.location.href = data.redirect;
      } else {
        document.getElementById("error-message").innerHTML = data.message;
        // alert(data.message);
      }
    })
    .catch((error) => console.error("Error:", error));
}
