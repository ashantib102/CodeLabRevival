'use client';
import { useState, FormEvent } from 'react';
import { useRouter } from 'next/navigation';
import CodeLogo from '@/components/CodeLogo';
import { api } from '@/lib/api';

export default function SelfEnrollPage() {
  const router = useRouter();
  const [accessCode, setAccessCode] = useState('');
  const [accessCodeErr, setAccessCodeErr] = useState('');
  const [submitErr, setSubmitErr] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setAccessCodeErr('');
    setSubmitErr('');
    setSuccess('');

    if (!accessCode.trim()) {
      setAccessCodeErr('Please enter an access code');
      return;
    }

    setLoading(true);
    try {
      const result = await api.enrollInCourse(accessCode.trim());
      setSuccess(result.message);
      setTimeout(() => router.push('/courses'), 2000);
    } catch (err: unknown) {
      setSubmitErr(err instanceof Error ? err.message : 'Enrollment failed');
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
          <h2>Student Self-Enrollment</h2>
          <p style={{ textAlign: 'center', marginBottom: 20, color: '#666', fontSize: 14 }}>
            Enter the access code provided by your instructor to enroll in a course.
          </p>

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
              <label htmlFor="accessCode">Access Code</label>
              <div className="login-field">
                <input
                  id="accessCode"
                  type="text"
                  className={`login-input${accessCodeErr ? ' error' : ''}`}
                  value={accessCode}
                  onChange={e => setAccessCode(e.target.value)}
                  placeholder="e.g., TCAB-32741-HWYW-67"
                  style={{ textTransform: 'uppercase' }}
                />
                {accessCodeErr && <span className="field-error">⚠ {accessCodeErr}</span>}
              </div>
            </div>

            <div style={{ display: 'flex', justifyContent: 'center', marginTop: 8 }}>
              <button
                type="submit"
                className="btn btn-green"
                disabled={loading}
                style={{ minWidth: 130 }}
              >
                {loading ? '⏳ Enrolling…' : '📚 Enroll'}
              </button>
            </div>
          </form>

          <div className="login-links">
            <a href="/courses">Back to Courses</a><br />
            <a href="/login">Back to Login</a>
          </div>
        </div>
      </main>
    </div>
  );
}