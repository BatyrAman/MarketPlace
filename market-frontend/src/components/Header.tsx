import type { RouteName } from '../App';

interface HeaderProps {
  navigate: (route: RouteName) => void;
  isAuthenticated: boolean;
  onLogout: () => void;
}

function Header({ navigate, isAuthenticated, onLogout }: HeaderProps) {
  return (
    <header className="header">
      <div className="brand" onClick={() => navigate('main')}>
        MarketPlace
      </div>
      <nav className="nav-links">
        <button onClick={() => navigate('main')}>Home</button>
        <button onClick={() => navigate('cart')}>Cart</button>
        <button onClick={() => navigate('orders')}>Orders</button>
        <button onClick={() => navigate('reviews')}>Reviews</button>
        {isAuthenticated ? (
          <>
            <button onClick={() => navigate('profile')}>Profile</button>
            <button className="primary-button" onClick={onLogout}>Logout</button>
          </>
        ) : (
          <>
            <button onClick={() => navigate('login')}>Login</button>
            <button className="primary-button" onClick={() => navigate('register')}>Register</button>
          </>
        )}
      </nav>
    </header>
  );
}

export default Header;
