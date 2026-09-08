import { Link } from "react-router-dom";
import "../App.css";

function Login() {
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

        <form className="auth-form">

          <div className="form-group">
            <label>Email Address</label>
            <input
              type="email"
              placeholder="Enter your email"
            />
          </div>

          <div className="form-group">
            <label>Password</label>
            <input
              type="password"
              placeholder="Enter your password"
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