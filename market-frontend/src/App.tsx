import { useEffect, useMemo, useState } from 'react';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import ProfilePage from './pages/ProfilePage';
import MainPage from './pages/MainPage';
import CartPage from './pages/CartPage';
import ReviewPage from './pages/ReviewPage';
import OrderItemsPage from './pages/OrderItemsPage';
import Header from './components/Header';
import { authService } from './services/authService';

export type RouteName = 'main' | 'login' | 'register' | 'profile' | 'cart' | 'reviews' | 'orders';

function readRoute(): RouteName {
  const hash = window.location.hash.replace('#', '').trim();
  if (hash === 'login') return 'login';
  if (hash === 'register') return 'register';
  if (hash === 'profile') return 'profile';
  if (hash === 'cart') return 'cart';
  if (hash === 'reviews') return 'reviews';
  if (hash === 'orders') return 'orders';
  return 'main';
}

function App() {
  const [route, setRoute] = useState<RouteName>(readRoute());
  const [isAuthenticated, setIsAuthenticated] = useState(authService.isAuthenticated());

  useEffect(() => {
    const onHashChange = () => setRoute(readRoute());
    window.addEventListener('hashchange', onHashChange);
    return () => window.removeEventListener('hashchange', onHashChange);
  }, []);

  const navigate = (next: RouteName) => {
    window.location.hash = next === 'main' ? '' : next;
    setRoute(next);
  };

  const handleAuthChanged = () => setIsAuthenticated(authService.isAuthenticated());

  const page = useMemo(() => {
    switch (route) {
      case 'login':
        return <LoginPage navigate={navigate} onAuthChanged={handleAuthChanged} />;
      case 'register':
        return <RegisterPage navigate={navigate} onAuthChanged={handleAuthChanged} />;
      case 'profile':
        return <ProfilePage navigate={navigate} isAuthenticated={isAuthenticated} />;
      case 'cart':
        return <CartPage navigate={navigate} isAuthenticated={isAuthenticated} />;
      case 'reviews':
        return <ReviewPage navigate={navigate} isAuthenticated={isAuthenticated} />;
      case 'orders':
        return <OrderItemsPage navigate={navigate} isAuthenticated={isAuthenticated} />;
      case 'main':
      default:
        return <MainPage navigate={navigate} isAuthenticated={isAuthenticated} />;
    }
  }, [route, isAuthenticated]);

  return (
    <div className="app-shell">
      <Header
        navigate={navigate}
        isAuthenticated={isAuthenticated}
        onLogout={() => {
          authService.logout();
          handleAuthChanged();
          navigate('main');
        }}
      />
      <main className="page-container">{page}</main>
    </div>
  );
}

export default App;
