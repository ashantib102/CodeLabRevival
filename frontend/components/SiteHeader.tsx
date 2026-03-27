'use client';
import { useRouter } from 'next/navigation';
import CodeLogo from './CodeLogo';

interface Props {
  userName: string;
}

export default function SiteHeader({ userName }: Props) {
  const router = useRouter();

  function handleLogout() {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('cl_token');
      localStorage.removeItem('cl_user');
    }
    router.push('/login');
  }

  return (
    <header className="site-header">
      <div className="h-left">
        <CodeLogo />
      </div>
      <div className="h-center">
        Welcome, <em>{userName}</em>
      </div>
      <div className="h-right">
        <a href="/courses" className="nav-link" style={{ fontWeight: 600 }}>Courses</a>
        <button className="hamburger" aria-label="Menu" title="Menu">☰</button>
        <button
          onClick={handleLogout}
          className="btn btn-outline btn-sm"
          title="Sign out"
        >
          Sign Out
        </button>
      </div>
    </header>
  );
}
