import { useEffect, useState } from 'react';
import type { RouteName } from '../App';
import { marketService } from '../services/marketService';
import type { User } from '../types';

interface ProfilePageProps {
  navigate: (route: RouteName) => void;
  isAuthenticated: boolean;
}

function ProfilePage({ navigate, isAuthenticated }: ProfilePageProps) {
  const [profile, setProfile] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('login');
      return;
    }

    marketService
      .getProfile()
      .then(setProfile)
      .catch((err) => setError(err instanceof Error ? err.message : 'Failed to load profile'))
      .finally(() => setLoading(false));
  }, [isAuthenticated, navigate]);

  if (loading) return <div className="card">Loading profile...</div>;
  if (error) return <div className="alert error">{error}</div>;
  if (!profile) return <div className="card">Profile not found.</div>;

  return (
    <section className="stack-large">
      <div className="card profile-hero">
        <div className="avatar-circle">{profile.username.slice(0, 1).toUpperCase()}</div>
        <div>
          <p className="eyebrow">Customer profile</p>
          <h1>{profile.full_name || profile.username}</h1>
          <p className="muted">@{profile.username} · {profile.email}</p>
        </div>
      </div>

      <div className="stats-grid">
        <div className="card">
          <h3>Role</h3>
          <p>{profile.role}</p>
        </div>
        <div className="card">
          <h3>Status</h3>
          <p>{profile.is_active ? 'Active' : 'Inactive'}</p>
        </div>
        <div className="card">
          <h3>Joined</h3>
          <p>{new Date(profile.created_at).toLocaleString()}</p>
        </div>
      </div>

      <div className="card stack-small">
        <h2>Quick actions</h2>
        <div className="row-gap">
          <button className="primary-button" onClick={() => navigate('cart')}>Open cart</button>
          <button className="ghost-button" onClick={() => navigate('orders')}>My orders</button>
          <button className="ghost-button" onClick={() => navigate('reviews')}>My review area</button>
        </div>
      </div>
    </section>
  );
}

export default ProfilePage;
