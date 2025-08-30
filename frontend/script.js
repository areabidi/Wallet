//const BASE_URL = window.location.origin;
const BASE_URL = "http://127.0.0.1:8000";  // FastAPI backend URL

// This is the base URL of your FastAPI backend. All your API calls will be made to this server.

// Gets the email & password from the form.
// Sends a POST request to /signup.
// If the response is OK (200), it alerts the user that signup was successful.
// If there's an error (like 400 or 500), it shows an error alert.
function signup() {
    const email = document.getElementById("signup-email").value;
    const password = document.getElementById("signup-password").value;

    fetch(`${BASE_URL}/signup`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
    })
    .then(res => {
        if (!res.ok) throw new Error("Signup failed");
        return res.json();
    })
    .then(data => alert("✅ Signup successful!"))
    .catch(err => alert("❌ " + err.message));
}


// Gets email & password from login form.
// Sends a POST request to /login.
// If successful:
// Receives a JWT token from the backend.
// Stores it in localStorage so it can be used later.
// Shows success or error messages.
function login() {
    const email = document.getElementById("login-email").value;
    const password = document.getElementById("login-password").value;

    fetch(`${BASE_URL}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
    })
    .then(res => {
        if (!res.ok) throw new Error("Login failed");
        return res.json();
    })
    .then(data => {
        localStorage.setItem("token", data.access_token);
        alert("✅ Login successful! Token saved.");
    })
    .catch(err => alert("❌ " + err.message));
}

// Checks if a token is stored in localStorage.
// If no token → asks user to log in.
// If token exists → makes a GET request to /protected, passing the token in the query string (e.g. /protected?token=abc123).
// If the backend accepts the token, it returns a welcome message.
// The message is shown inside the <p> with ID protected-response.
function accessProtected() {
    const token = localStorage.getItem("token");
    if (!token) {
        alert("❌ Please log in first!");
        return;
    }

    fetch(`${BASE_URL}/protected?token=${token}`)
        .then(res => {
            if (!res.ok) throw new Error("Access denied");
            return res.json();
        })
        .then(data => {
            document.getElementById("protected-response").innerText = data.message;
        })
        .catch(err => alert("❌ " + err.message));
}