'use client';
import { useState } from 'react';
import { useRouter } from 'next/navigation';
import CodeLogo from './CodeLogo';

interface Props {
  userName: string;
  userRole?: string;
}

export default function LabHeader({ userName, userRole }: Props) {
  const router = useRouter();
  const [mode, setMode] = useState('Standard');

  function handleLogout() {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('cl_token');
      localStorage.removeItem('cl_user');
    }
    router.push('/login');
  }

  return (
    <header className="lab-header">
      <div className="h-left">
        <CodeLogo small />
      </div>
      <div className="h-center">
        Welcome, <em>{userName}</em>
      </div>
      <div className="h-right">
        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <a href="/courses" className="nav-link" style={{ fontWeight: 600, fontSize: 13 }}>Courses</a>
          {userRole === 'instructor' && (
            <a href="/create-exercise" className="nav-link" style={{ fontWeight: 600, fontSize: 13, color: '#267a14' }}>
              + Create Exercise
            </a>
          )}
          <button className="hamburger" style={{ fontSize: 17 }} aria-label="Menu">☰</button>
          <button
            onClick={handleLogout}
            className="btn btn-outline btn-sm"
          >
            Sign Out
          </button>
        </div>
        <div className="mode-row">
          <span>Mode:</span>
          <select
            className="mode-select"
            value={mode}
            onChange={e => setMode(e.target.value)}
          >
            <option>Standard</option>
            <option>Practice</option>
            <option>Exam</option>
          </select>
        </div>
      </div>
    </header>
  );
}
