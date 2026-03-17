import { useState } from 'react';
import type { RouteName } from '../App';
import { authService } from '../services/authService';

interface RegisterPageProps {
  navigate: (route: RouteName) => void;
  onAuthChanged: () => void;
}

function RegisterPage({ navigate, onAuthChanged }: RegisterPageProps) {
  const [form, setForm] = useState({ email: '', username: '', full_name: '', password: '' });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const updateField = (name: keyof typeof form, value: string) => setForm((prev) => ({ ...prev, [name]: value }));

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');
    try {
      await authService.register(form);
      await authService.login({ email: form.email, password: form.password });
      onAuthChanged();
      setSuccess('Account created successfully.');
      navigate('main');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="auth-layout">
      <form className="card auth-card" onSubmit={handleSubmit}>
        <div>
          <h1>Create account</h1>
          <p className="muted">Build your own marketplace profile in a clean portfolio style.</p>
        </div>
        <label>
          <span>Full name</span>
          <input value={form.full_name} onChange={(e) => updateField('full_name', e.target.value)} placeholder="Batyr Aman" />
        </label>
        <label>
          <span>Username</span>
          <input value={form.username} onChange={(e) => updateField('username', e.target.value)} placeholder="batyr_01" required />
        </label>
        <label>
          <span>Email</span>
          <input type="email" value={form.email} onChange={(e) => updateField('email', e.target.value)} placeholder="you@example.com" required />
        </label>
        <label>
          <span>Password</span>
          <input type="password" value={form.password} onChange={(e) => updateField('password', e.target.value)} placeholder="Create a strong password" required />
        </label>
        {error ? <div className="alert error">{error}</div> : null}
        {success ? <div className="alert success">{success}</div> : null}
        <button className="primary-button" type="submit" disabled={loading}>
          {loading ? 'Creating...' : 'Register'}
        </button>
        <button type="button" className="ghost-button" onClick={() => navigate('login')}>
          Already have an account
        </button>
      </form>
    </section>
  );
}

export default RegisterPage;
