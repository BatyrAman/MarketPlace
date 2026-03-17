import { useState } from 'react';
import type { RouteName } from '../App';
import { authService } from '../services/authService';

interface LoginPageProps {
  navigate: (route: RouteName) => void;
  onAuthChanged: () => void;
}

function LoginPage({ navigate, onAuthChanged }: LoginPageProps) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setLoading(true);
    setError('');
    try {
      await authService.login({ email, password });
      onAuthChanged();
      navigate('main');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="auth-layout">
      <form className="card auth-card" onSubmit={handleSubmit}>
        <div>
          <h1>Welcome back</h1>
          <p className="muted">Login to manage your cart, orders and reviews.</p>
        </div>
        <label>
          <span>Email</span>
          <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="you@example.com" required />
        </label>
        <label>
          <span>Password</span>
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="••••••••" required />
        </label>
        {error ? <div className="alert error">{error}</div> : null}
        <button className="primary-button" type="submit" disabled={loading}>
          {loading ? 'Signing in...' : 'Login'}
        </button>
        <button type="button" className="ghost-button" onClick={() => navigate('register')}>
          Create account
        </button>
      </form>
    </section>
  );
}

export default LoginPage;
