import { useState } from 'react';
import { mockLogin } from '../data/mockData';

// ==========================================================================
// LOGIN PAGE
// Basic username/password form. Uses mockLogin() from mockData.js instead
// of a real backend. Wrong credentials show an inline error message.
// ==========================================================================

function LoginPage({ onLoginSuccess }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  function handleSubmit(e) {
    e.preventDefault();

    if (!username.trim() || !password.trim()) {
      setError('Please enter both username and password.');
      return;
    }

    const result = mockLogin(username.trim(), password);

    if (result.success) {
      setError('');
      onLoginSuccess();
    } else {
      setError(result.message);
    }
  }

  return (
    <div className="login-page">
      <div className="login-card">
        <div className="login-card__header">
          <div className="navbar__logo-mark navbar__logo-mark--lg">A</div>
          <h1>Verification Desk Login</h1>
          <p className="text-muted">
            Secure access for authorized verification officers only.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="login-form">
          <label className="form-label" htmlFor="username">
            Username
          </label>
          <input
            id="username"
            type="text"
            className="form-input"
            placeholder="e.g. officer1"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            autoComplete="username"
          />

          <label className="form-label" htmlFor="password">
            Password
          </label>
          <input
            id="password"
            type="password"
            className="form-input"
            placeholder="Enter your password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            autoComplete="current-password"
          />

          {error && <div className="alert alert--error">{error}</div>}

          <button type="submit" className="btn btn--primary btn--full">
            Log In
          </button>
        </form>

        <p className="login-hint">
          Demo credentials — username: <code>officer1</code>, password:{' '}
          <code>authenova123</code>
        </p>
      </div>
    </div>
  );
}

export default LoginPage;