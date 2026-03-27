'use client';
import { useEffect, useState, Suspense } from 'react';
import { useRouter, useParams, useSearchParams } from 'next/navigation';
import LabHeader from '@/components/LabHeader';
import NotifBanner from '@/components/NotifBanner';
import TocPanel from '@/components/TocPanel';
import { api, getUser, getToken } from '@/lib/api';
import type { SubmissionResult, LabStructure } from '@/lib/api';

type ResTab = 'work' | 'solutions' | 'results' | 'tracking';

export default function ResultsPage() {
  return (
    <Suspense fallback={<div style={{ padding: 20 }}>Loading…</div>}>
      <ResultsInner />
    </Suspense>
  );
}

function ResultsInner() {
  const router       = useRouter();
  const params       = useParams<{ submissionId: string }>();
  const searchParams = useSearchParams();
  const user = typeof window !== 'undefined' ? getUser() : null;

  const [result, setResult] = useState<SubmissionResult | null>(null);
  const [lab, setLab]       = useState<LabStructure | null>(null);
  const [tab, setTab]       = useState<ResTab>('results');
  const [error, setError]   = useState('');

  useEffect(() => {
    if (!getToken()) { router.replace('/login'); return; }

    // Try to read result from URL param (passed from exercise page)
    const raw = searchParams.get('data');
    if (raw) {
      try {
        const parsed = JSON.parse(decodeURIComponent(raw)) as SubmissionResult;
        setResult(parsed);
        return;
      } catch { /* fall through to API */ }
    }
    // Fallback: not implemented in this prototype
    setError('Result not found');
  }, [params.submissionId, searchParams, router]);

  useEffect(() => {
    if (!result) return;
    api.getLabStructure(result.exercise_id.slice(0, 5) || 'default')
      .then(setLab)
      .catch(() => { /* TOC optional */ });
  }, [result]);

  if (error)  return <div style={{ padding: 20, color: '#c0392b' }}>Error: {error}</div>;
  if (!result) return <div style={{ padding: 20 }}>Loading results…</div>;

  const isCompilerError = result.status === 'compiler_error';
  const isCorrect       = result.status === 'correct';

  const statusLabel =
    result.status === 'correct'        ? '✔ Correct'          :
    result.status === 'compiler_error' ? '✘ Compiler Error'   :
    result.status === 'runtime_error'  ? '✘ Runtime Error'    :
    '✘ Wrong Output';

  const statusColor =
    result.status === 'correct' ? '#267a14' : '#c0392b';

  return (
    <div className="lab-wrap">
      <LabHeader userName={user?.name ?? 'User'} />
      <NotifBanner />

      <div className="lab-main">
        {lab && (
          <TocPanel
            courseId=""
            tree={lab.tree}
            activeExerciseId={result.exercise_id}
          />
        )}

        <div className="content-panel">
          <div className="tabs-bar">
            <div className="tabs-left">
              {(['work', 'solutions', 'results', 'tracking'] as ResTab[]).map(t => (
                <button
                  key={t}
                  className={`tab-btn${tab === t ? ' active' : ''}`}
                  onClick={() => setTab(t)}
                >
                  {t === 'work' ? 'Work Area' : t.charAt(0).toUpperCase() + t.slice(1)}
                </button>
              ))}
            </div>
            <div className="tabs-right">
              <span title="Refresh">↻</span>
              <span title="Help">?</span>
            </div>
          </div>

          <div className="content-area">
            {tab === 'results' && (
              <>
                {/* Status summary */}
                <div style={{
                  display: 'flex', alignItems: 'center', gap: 12,
                  marginBottom: 16, padding: '10px 14px',
                  background: isCorrect ? '#f0fff0' : '#fff0f0',
                  border: `1px solid ${statusColor}`,
                  borderRadius: 3
                }}>
                  <span style={{ fontSize: 24, color: statusColor }}>
                    {isCorrect ? '✔' : '✘'}
                  </span>
                  <div>
                    <div style={{ fontWeight: 700, color: statusColor, fontSize: 15 }}>
                      {statusLabel}
                    </div>
                    <div style={{ fontSize: 12, color: '#555', marginTop: 2 }}>
                      {result.message}
                    </div>
                  </div>
                  <div style={{ marginLeft: 'auto' }}>
                    <span className={`badge ${isCorrect ? 'badge-correct' : 'badge-wrong'}`}
                      style={{ fontSize: 14, padding: '3px 10px' }}>
                      Score: {result.score}%
                    </span>
                  </div>
                </div>

                {/* Compiler/Runtime errors */}
                {result.compiler_output && (
                  <div className="section-card" style={{ marginBottom: 12 }}>
                    <div className="section-hdr red">
                      <span>▶</span>
                      {isCompilerError ? 'Compiler Errors' : 'Runtime Errors'}
                    </div>
                    <div className="section-body" style={{ padding: 0 }}>
                      <pre className="terminal" style={{ margin: 0 }}>
                        {result.compiler_output}
                      </pre>
                    </div>
                  </div>
                )}

                {/* Your Submission */}
                <div className="section-card">
                  <div className="section-hdr red">
                    <span>▶</span> Your Submission
                  </div>
                  <div className="section-body" style={{ padding: 0 }}>
                    <div className="diff-legend">
                      <span>your output</span>
                    </div>
                    <div className="diff-area">
                      {result.your_code.split('\n').map((line, i) => (
                        <div key={i} className="diff-line">
                          <span className="diff-line-num">{i + 1}</span>
                          <span className="diff-yours">{line}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>

                <div style={{ marginTop: 14, display: 'flex', gap: 8 }}>
                  <button
                    className="btn btn-outline btn-sm"
                    onClick={() => router.back()}
                  >
                    ← Back to Exercise
                  </button>
                </div>
              </>
            )}

            {tab === 'work' && (
              <div>
                <p style={{ marginBottom: 10 }}>
                  <button
                    className="btn btn-outline btn-sm"
                    onClick={() => router.push(`/exercise/${result.exercise_id}`)}
                  >
                    ← Go to Exercise
                  </button>
                </p>
                <pre className="terminal" style={{ whiteSpace: 'pre-wrap' }}>
                  {result.your_code}
                </pre>
              </div>
            )}

            {tab === 'solutions' && (
              <p style={{ color: '#555' }}>Solutions are not available.</p>
            )}

            {tab === 'tracking' && (
              <div>
                <h3 style={{ marginBottom: 12 }}>Submission History</h3>
                <table className="tracking-table">
                  <thead>
                    <tr><th>#</th><th>Submission ID</th><th>Result</th><th>Score</th></tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>1</td>
                      <td style={{ fontFamily: 'monospace', fontSize: 11 }}>{result.submission_id}</td>
                      <td style={{ color: statusColor }}>{statusLabel}</td>
                      <td>{result.score}%</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
