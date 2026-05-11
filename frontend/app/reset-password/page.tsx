'use client';
import { useState, FormEvent, useEffect } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import CodeLogo from '@/components/CodeLogo';
import { api } from '@/lib/api';

export default function ResetPasswordPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const token = searchParams.get('token');

  const [password, setPassword] = useState('');
  const [confirm, setConfirm] = useState('');
  const [passwordErr, setPasswordErr] = useState('');
  const [confirmErr, setConfirmErr] = useState('');
  const [submitErr, setSubmitErr] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);
  const [tokenValid, setTokenValid] = useState<boolean | null>(null);

  useEffect(() => {
    if (!token) {
      setTokenValid(false);
    } else {
      // In a real app, you might validate the token here
      setTokenValid(true);
    }
  }, [token]);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setPasswordErr('');
    setConfirmErr('');
    setSubmitErr('');
    setSuccess('');

    if (password.length < 6) {
      setPasswordErr('Password must be at least 6 characters');
      return;
    }
    if (password !== confirm) {
      setConfirmErr('Passwords do not match');
      return;
    }
    if (!token) {
      setSubmitErr('Invalid reset token');
      return;
    }

    setLoading(true);
    try {
      await api.resetPassword(token, password);
      setSuccess('Password reset successfully! Redirecting to login...');
      setTimeout(() => router.push('/login'), 2000);
    } catch (err: unknown) {
      setSubmitErr(err instanceof Error ? err.message : 'Reset failed');
    } finally {
      setLoading(false);
    }
  }

  if (tokenValid === false) {
    return (
      <div className="login-wrap">
        <header className="login-hdr">
          <CodeLogo />
        </header>
        <main className="login-main">
          <div className="login-card">
            <h2>Invalid Reset Link</h2>
            <p style={{ color: '#c0392b', textAlign: 'center' }}>
              This password reset link is invalid or has expired.
            </p>
            <div className="login-links">
              <a href="/forgot-password">Request a new reset link</a>
            </div>
          </div>
        </main>
      </div>
    );
  }

  if (tokenValid === null) {
    return (
      <div className="login-wrap">
        <header className="login-hdr">
          <CodeLogo />
        </header>
        <main className="login-main">
          <div className="login-card">
            <h2>Loading...</h2>
          </div>
        </main>
      </div>
    );
  }

  return (
    <div className="login-wrap">
      <header className="login-hdr">
        <CodeLogo />
      </header>

      <main className="login-main">
        <div className="login-card">
          <h2>Reset Password</h2>

          {submitErr && (
            <p style={{ color: '#c0392b', textAlign: 'center', marginBottom: 12, fontSize: 13 }}>
              ⚠ {submitErr}
            </p>
          )}

          {success && (
            <p style={{ color: '#27ae60', textAlign: 'center', marginBottom: 12, fontSize: 13 }}>
              ✓ {success}
            </p>
          )}

          <form onSubmit={handleSubmit} noValidate>
            <div className="login-row">
              <label htmlFor="password">New Password</label>
              <div className="login-field">
                <input
                  id="password"
                  type="password"
                  autoComplete="new-password"
                  className={`login-input${passwordErr ? ' error' : ''}`}
                  value={password}
                  onChange={e => setPassword(e.target.value)}
                />
                {passwordErr && <span className="field-error">⚠ {passwordErr}</span>}
              </div>
            </div>

            <div className="login-row">
              <label htmlFor="confirm">Confirm Password</label>
              <div className="login-field">
                <input
                  id="confirm"
                  type="password"
                  autoComplete="new-password"
                  className={`login-input${confirmErr ? ' error' : ''}`}
                  value={confirm}
                  onChange={e => setConfirm(e.target.value)}
                />
                {confirmErr && <span className="field-error">⚠ {confirmErr}</span>}
              </div>
            </div>

            <div style={{ display: 'flex', justifyContent: 'center', marginTop: 8 }}>
              <button
                type="submit"
                className="btn btn-green"
                disabled={loading}
                style={{ minWidth: 130 }}
              >
                {loading ? '⏳ Resetting…' : '🔑 Reset Password'}
              </button>
            </div>
          </form>
        </div>
      </main>
    </div>
  );
}