'use client';
import { useEffect, useState, Suspense } from 'react';
import { useRouter, useParams, useSearchParams } from 'next/navigation';
import LabHeader from '@/components/LabHeader';
import NotifBanner from '@/components/NotifBanner';
import TocPanel from '@/components/TocPanel';
import { api, getUser, getToken } from '@/lib/api';
import type { SubmissionResult, LabStructure, DiffLine } from '@/lib/api';

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
    if (!result.course_id) return;
    api.getLabStructure(result.course_id)
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

  const gradeColor = (g: string) => {
    if (g.startsWith('A')) return '#16a34a';  // green
    if (g.startsWith('B')) return '#2563eb';  // blue
    if (g.startsWith('C')) return '#d97706';  // amber
    if (g.startsWith('D')) return '#ea580c';  // orange
    return '#dc2626';                          // F = red
  };

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
                {/* Status + Grade summary */}
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
                  <div style={{ marginLeft: 'auto', display: 'flex', alignItems: 'center', gap: 10 }}>
                    {/* Letter grade badge */}
                    {result.grade && (
                      <div style={{
                        display: 'flex', flexDirection: 'column', alignItems: 'center',
                        background: gradeColor(result.grade),
                        color: '#fff',
                        borderRadius: 6,
                        padding: '4px 14px',
                        minWidth: 52,
                      }}>
                        <span style={{ fontSize: 22, fontWeight: 800, lineHeight: 1.1 }}>
                          {result.grade}
                        </span>
                        <span style={{ fontSize: 9, opacity: 0.85, textTransform: 'uppercase', letterSpacing: 1 }}>
                          grade
                        </span>
                      </div>
                    )}
                    {/* Similarity score */}
                    <div style={{
                      display: 'flex', flexDirection: 'column', alignItems: 'center',
                      background: '#f4f4f4', border: '1px solid #ddd',
                      borderRadius: 6, padding: '4px 12px', minWidth: 52,
                    }}>
                      <span style={{ fontSize: 18, fontWeight: 700, color: '#333', lineHeight: 1.1 }}>
                        {result.score}%
                      </span>
                      <span style={{ fontSize: 9, color: '#888', textTransform: 'uppercase', letterSpacing: 1 }}>
                        similarity
                      </span>
                    </div>
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
              <SolutionDiff
                diff={result.diff}
                solutionCode={result.solution_code}
                yourCode={result.your_code}
              />
            )}

            {tab === 'tracking' && (
              <div>
                <h3 style={{ marginBottom: 12 }}>Submission History</h3>
                <table className="tracking-table">
                  <thead>
                    <tr><th>#</th><th>Submission ID</th><th>Result</th><th>Similarity</th><th>Grade</th></tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>1</td>
                      <td style={{ fontFamily: 'monospace', fontSize: 11 }}>{result.submission_id}</td>
                      <td style={{ color: statusColor }}>{statusLabel}</td>
                      <td>{result.score}%</td>
                      <td>
                        <span style={{
                          fontWeight: 700, fontSize: 14,
                          color: gradeColor(result.grade),
                        }}>
                          {result.grade || '—'}
                        </span>
                      </td>
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

// ── Diff Viewer ───────────────────────────────────────────────────────────────

const DIFF_BG: Record<string, string> = {
  equal:       'transparent',
  insert:      '#e6ffed',
  delete:      '#ffeef0',
  replace_old: '#ffeef0',
  replace_new: '#e6ffed',
};

const DIFF_BORDER: Record<string, string> = {
  equal:       'transparent',
  insert:      '#34d058',
  delete:      '#d73a49',
  replace_old: '#d73a49',
  replace_new: '#34d058',
};

const DIFF_PREFIX: Record<string, string> = {
  equal:       ' ',
  insert:      '+',
  delete:      '-',
  replace_old: '-',
  replace_new: '+',
};

function SolutionDiff({
  diff,
  solutionCode,
  yourCode,
}: {
  diff: DiffLine[];
  solutionCode: string;
  yourCode: string;
}) {
  if (!solutionCode) {
    return (
      <p style={{ color: '#777', fontStyle: 'italic', padding: 8 }}>
        No reference solution available for this exercise.
      </p>
    );
  }

  const hasDiff = diff && diff.length > 0;

  return (
    <div>
      {/* Legend */}
      <div style={{
        display: 'flex', gap: 16, marginBottom: 12, fontSize: 12, alignItems: 'center'
      }}>
        <strong style={{ fontSize: 13 }}>Solution vs Your Submission</strong>
        <span style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
          <span style={{ width: 12, height: 12, background: '#e6ffed', border: '1px solid #34d058', display: 'inline-block', borderRadius: 2 }} />
          added by you / extra
        </span>
        <span style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
          <span style={{ width: 12, height: 12, background: '#ffeef0', border: '1px solid #d73a49', display: 'inline-block', borderRadius: 2 }} />
          in solution / missing
        </span>
        <span style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
          <span style={{ width: 12, height: 12, background: 'transparent', border: '1px solid #ccc', display: 'inline-block', borderRadius: 2 }} />
          unchanged
        </span>
      </div>

      {hasDiff ? (
        /* Unified diff view */
        <div style={{
          fontFamily: 'monospace',
          fontSize: 12,
          lineHeight: '1.6',
          border: '1px solid #ddd',
          borderRadius: 4,
          overflow: 'auto',
          maxHeight: 520,
        }}>
          <div style={{
            display: 'grid',
            gridTemplateColumns: '36px 36px 18px 1fr',
            background: '#f6f8fa',
            borderBottom: '1px solid #ddd',
            padding: '4px 8px',
            fontWeight: 700,
            fontSize: 11,
            color: '#555',
          }}>
            <span>Sol</span>
            <span>You</span>
            <span />
            <span>Code</span>
          </div>
          {diff.map((line, i) => (
            <div
              key={i}
              style={{
                display: 'grid',
                gridTemplateColumns: '36px 36px 18px 1fr',
                background: DIFF_BG[line.type] ?? 'transparent',
                borderLeft: `3px solid ${DIFF_BORDER[line.type] ?? 'transparent'}`,
                padding: '1px 8px',
              }}
            >
              <span style={{ color: '#999', userSelect: 'none' }}>
                {line.line_no_left ?? ''}
              </span>
              <span style={{ color: '#999', userSelect: 'none' }}>
                {line.line_no_right ?? ''}
              </span>
              <span style={{
                color: line.type === 'equal' ? '#aaa' :
                       line.type.startsWith('replace_') || line.type === 'delete' ? '#d73a49' : '#28a745',
                fontWeight: 700,
                userSelect: 'none',
              }}>
                {DIFF_PREFIX[line.type] ?? ' '}
              </span>
              <span style={{ whiteSpace: 'pre' }}>{line.content}</span>
            </div>
          ))}
        </div>
      ) : (
        /* Identical — just show code */
        <div>
          <div style={{ marginBottom: 6, color: '#267a14', fontWeight: 600 }}>
            ✔ Your submission matches the solution exactly.
          </div>
          <pre style={{
            background: '#f6f8fa', border: '1px solid #ddd', borderRadius: 4,
            padding: '10px 14px', fontSize: 12, overflow: 'auto', maxHeight: 480,
          }}>
            {solutionCode}
          </pre>
        </div>
      )}
    </div>
  );
}
