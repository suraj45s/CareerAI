import { Link } from "react-router-dom";
import { useState } from "react";
import "../App.css";
function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const handleLogin = async (e) => {
  e.preventDefault();

  try {
    const response = await fetch(
      `http://127.0.0.1:8000/login?email=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}`,
      {
        method: "POST",
      }
    );

    const data = await response.json();

    if (!response.ok) {
      alert(data.detail || "Login failed");
      return;
    }

    localStorage.setItem("access_token", data.access_token);

    alert("Login successful!");

    console.log(data);

  } catch (error) {
    alert("Server error. Please try again.");
    console.error(error);
  }
};
  return (
    <div className="auth-page">

      <div className="auth-card">

        <div className="auth-logo">
          CareerAI
        </div>

        <h1>Welcome Back 👋</h1>

        <p className="auth-subtitle">
          Login to continue your career journey
        </p>

        <form className="auth-form" onSubmit={handleLogin}>

          <div className="form-group">
            <label>Email Address</label>
            <input
              type="email"
              placeholder="Enter your email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>

          <div className="form-group">
            <label>Password</label>
            <input
              type="password"
              placeholder="Enter your password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>

          <div className="form-options">
            <label className="remember">
              <input type="checkbox" />
              Remember me
            </label>

            <a href="#forgot">Forgot Password?</a>
          </div>

          <button type="submit" className="auth-btn">
            Login
          </button>

        </form>

        <p className="auth-footer">
          Don't have an account?{" "}
          <Link to="/register">Create Account</Link>
        </p>

        <Link to="/" className="back-home">
          ← Back to Home
        </Link>

      </div>

    </div>
  );
}

export default Login;