import{Link} from "react-router-dom";
import "../App.css";

function App() {
  return (
    <div className="app">
      <nav className="navbar">
        <div className="logo">CareerAI</div>

        <div className="nav-links">
  <a href="#features">Features</a>
  <a href="#about">About</a>

  <Link to="/login" className="login-btn">
    Login
  </Link>

  <Link to="/register" className="signup-btn">
    Get Started
  </Link>
</div>
      </nav>

      <main className="hero">
        <div className="hero-content">
          <div className="badge">🚀 AI-Powered Career Platform</div>

          <h1>
            Build Your Career
            <span> With AI</span>
          </h1>

          <p>
            Analyze your resume, discover the right career path,
            identify skill gaps, and prepare for your dream job.
          </p>

          <div className="hero-buttons">
            <button className="primary-btn">Get Started →</button>
            <button className="secondary-btn">Explore Features</button>
          </div>

          <div className="stats">
            <div>
              <strong>AI</strong>
              <small>Career Analysis</small>
            </div>

            <div>
              <strong>100+</strong>
              <small>Job Roles</small>
            </div>

            <div>
              <strong>24/7</strong>
              <small>AI Assistance</small>
            </div>
          </div>
        </div>

        <div className="hero-card">
          <div className="card-header">
            <span>Career Readiness</span>
            <span>82%</span>
          </div>

          <div className="progress">
            <div className="progress-bar"></div>
          </div>

          <div className="recommendation">
            <div className="icon">💼</div>
            <div>
              <h3>Software Engineer</h3>
              <p>91% Match</p>
            </div>
          </div>

          <div className="skills">
            <div>
              <span>Python</span>
              <b>90%</b>
            </div>

            <div>
              <span>SQL</span>
              <b>85%</b>
            </div>

            <div>
              <span>React</span>
              <b>72%</b>
            </div>
          </div>
        </div>
      </main>

      <section id="features" className="features">
        <h2>Everything You Need to Grow</h2>
        <p>One intelligent platform for your complete career journey.</p>

        <div className="feature-grid">
          <div className="feature-card">
            <div>📄</div>
            <h3>Resume Analyzer</h3>
            <p>AI analyzes your resume and extracts your key skills.</p>
          </div>

          <div className="feature-card">
            <div>🎯</div>
            <h3>Job Matching</h3>
            <p>Find career opportunities that match your profile.</p>
          </div>

          <div className="feature-card">
            <div>🧠</div>
            <h3>Skill Gap Analysis</h3>
            <p>Discover exactly which skills you need to improve.</p>
          </div>

          <div className="feature-card">
            <div>🤖</div>
            <h3>AI Interview Prep</h3>
            <p>Practice interviews with AI-powered preparation.</p>
          </div>
        </div>
      </section>
    </div>
  );
}

export default App;