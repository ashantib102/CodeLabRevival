'use client';
import { useState, FormEvent } from 'react';
import CodeLogo from '@/components/CodeLogo';
import { api } from '@/lib/api';

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState('');
  const [emailErr, setEmailErr] = useState('');
  const [submitErr, setSubmitErr] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setEmailErr('');
    setSubmitErr('');
    setSuccess('');

    if (!email.trim()) {
      setEmailErr('Please enter your email address');
      return;
    }

    setLoading(true);
    try {
      await api.forgotPassword(email.trim());
      setSuccess('If an account with that email exists, a password reset link has been sent.');
    } catch (err: unknown) {
      setSubmitErr(err instanceof Error ? err.message : 'Request failed');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="login-wrap">
      <header className="login-hdr">
        <CodeLogo />
      </header>

      <main className="login-main">
        <div className="login-card">
          <h2>Forgot Password</h2>

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
              <label htmlFor="email">Email</label>
              <div className="login-field">
                <input
                  id="email"
                  type="email"
                  autoComplete="email"
                  className={`login-input${emailErr ? ' error' : ''}`}
                  value={email}
                  onChange={e => setEmail(e.target.value)}
                  placeholder="you@example.com"
                />
                {emailErr && <span className="field-error">⚠ {emailErr}</span>}
              </div>
            </div>

            <div style={{ display: 'flex', justifyContent: 'center', marginTop: 8 }}>
              <button
                type="submit"
                className="btn btn-green"
                disabled={loading}
                style={{ minWidth: 130 }}
              >
                {loading ? '⏳ Sending…' : '📧 Send Reset Link'}
              </button>
            </div>
          </form>

          <div className="login-links">
            Remember your password? <a href="/login">Sign in here</a>
          </div>
        </div>
      </main>
    </div>
  );
}