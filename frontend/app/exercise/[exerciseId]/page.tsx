'use client';
import { useEffect, useState, useRef } from 'react';
import { useRouter, useParams } from 'next/navigation';
import LabHeader from '@/components/LabHeader';
import NotifBanner from '@/components/NotifBanner';
import TocPanel from '@/components/TocPanel';
import { api, getUser, getToken } from '@/lib/api';
import type { Exercise, LabStructure, SampleRun } from '@/lib/api';

type WorkTab    = 'work' | 'solutions' | 'tracking';
type SampleTab  = 'input' | 'output';

export default function ExercisePage() {
  const router   = useRouter();
  const params   = useParams<{ exerciseId: string }>();
  const exerciseId = params.exerciseId;
  const user = typeof window !== 'undefined' ? getUser() : null;

  const [exercise, setExercise]     = useState<Exercise | null>(null);
  const [lab, setLab]               = useState<LabStructure | null>(null);
  const [code, setCode]             = useState('');
  const [workTab, setWorkTab]       = useState<WorkTab>('work');
  const [sampleIdx, setSampleIdx]   = useState(0);
  const [sampleTab, setSampleTab]   = useState<SampleTab>('input');
  const [submitting, setSubmitting] = useState(false);
  const [error, setError]           = useState('');

  useEffect(() => {
    if (!getToken()) { router.replace('/login'); return; }
    api.getExercise(exerciseId)
      .then(ex => {
        setExercise(ex);
        setCode(ex.starter_code);
        return api.getLabStructure(ex.course_id);
      })
      .then(setLab)
      .catch(err => setError(err.message ?? 'Failed to load exercise'));
  }, [exerciseId, router]);

  async function handleSubmit() {
    if (!exercise) return;
    setSubmitting(true);
    try {
      const result = await api.submitCode(exercise.id, code);
      router.push(`/results/${result.submission_id}?data=${encodeURIComponent(JSON.stringify(result))}`);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Submission failed');
    } finally {
      setSubmitting(false);
    }
  }

  if (error)    return <div style={{ padding: 20, color: '#c0392b' }}>Error: {error}</div>;
  if (!exercise) return <div style={{ padding: 20 }}>Loading exercise…</div>;

  const sample: SampleRun | undefined = exercise.sample_runs[sampleIdx];

  return (
    <div className="lab-wrap">
      <LabHeader userName={user?.name ?? 'User'} />
      <NotifBanner />

      <div className="lab-main">
        {lab && (
          <TocPanel
            courseId={exercise.course_id}
            tree={lab.tree}
            activeExerciseId={exerciseId}
          />
        )}

        <div className="content-panel" style={{ display: 'flex', flexDirection: 'column' }}>
          {/* Tabs */}
          <div className="tabs-bar">
            <div className="tabs-left">
              {(['work', 'solutions', 'tracking'] as WorkTab[]).map(t => (
                <button
                  key={t}
                  className={`tab-btn${workTab === t ? ' active' : ''}`}
                  onClick={() => setWorkTab(t)}
                >
                  {t.charAt(0).toUpperCase() + t.slice(1)}{t === 'work' ? ' Area' : ''}
                </button>
              ))}
            </div>
            <div className="tabs-right">
              <span title="Refresh">↻</span>
              <span title="Help">?</span>
            </div>
          </div>

          {workTab === 'work' && (
            <div style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
              <div className="content-area" style={{ flex: '0 0 auto', maxHeight: '55%', overflowY: 'auto' }}>
                {/* Breadcrumb */}
                <div className="breadcrumb">
                  {exercise.topic} <span>›</span> {exercise.title}
                </div>

                {/* Instructions */}
                <div className="section-card" style={{ marginBottom: 10 }}>
                  <div className="section-hdr green">
                    <span>▶</span> Instructions
                  </div>
                  <div className="section-body">
                    <div
                      className="instr-text"
                      dangerouslySetInnerHTML={{ __html: exercise.instructions }}
                    />
                  </div>
                </div>

                {/* Sample Runs */}
                {exercise.sample_runs.length > 0 && (
                  <div className="section-card">
                    <div className="run-hdr">
                      <span>▶ Sample Run</span>
                      <span style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                        <button
                          className="run-nav-btn"
                          disabled={sampleIdx === 0}
                          onClick={() => setSampleIdx(i => i - 1)}
                        >◀</button>
                        <span style={{ fontSize: 12 }}>
                          {sampleIdx + 1} / {exercise.sample_runs.length}
                        </span>
                        <button
                          className="run-nav-btn"
                          disabled={sampleIdx === exercise.sample_runs.length - 1}
                          onClick={() => setSampleIdx(i => i + 1)}
                        >▶</button>
                      </span>
                    </div>

                    <div className="run-tab-bar">
                      <button
                        className={`run-tab${sampleTab === 'input' ? ' active' : ''}`}
                        onClick={() => setSampleTab('input')}
                      >
                        Interactive Session
                      </button>
                      <button
                        className={`run-tab${sampleTab === 'output' ? ' active' : ''}`}
                        onClick={() => setSampleTab('output')}
                      >
                        Sample Run Output
                      </button>
                    </div>

                    <div className="terminal-checks">
                      <span className="check-group">
                        <span>✔ Exact spaces</span>
                        <span>✔ Exact newlines</span>
                      </span>
                      <button className="invis-btn">Make Invisible</button>
                    </div>

                    <pre className="terminal">
                      {sampleTab === 'input' ? (
                        <>
                          {sample?.input.split('\n').map((line, i) => (
                            <div key={i}>
                              <span className="t-stdin">{line}</span>
                            </div>
                          ))}
                        </>
                      ) : (
                        <>
                          {sample?.output.split('\n').map((line, i) => (
                            <div key={i}>
                              <span className="t-stdout">{line}</span>
                            </div>
                          ))}
                        </>
                      )}
                    </pre>
                  </div>
                )}
              </div>

              {/* Submit bar */}
              <div className="submit-bar">
                <button
                  className="btn btn-green"
                  onClick={handleSubmit}
                  disabled={submitting}
                >
                  {submitting ? '⏳ Submitting…' : '▶ Submit'}
                </button>
                <div className="hist-group">
                  <label htmlFor="history-sel" style={{ fontSize: 12, color: '#555' }}>
                    Submission History:
                  </label>
                  <select id="history-sel" className="dropdown">
                    <option>Select a submission</option>
                  </select>
                </div>
              </div>

              {/* Code editor */}
              <textarea
                className="code-editor"
                value={code}
                onChange={e => setCode(e.target.value)}
                spellCheck={false}
                aria-label="Code editor"
              />
            </div>
          )}

          {workTab === 'solutions' && (
            <div className="content-area">
              <p style={{ color: '#555' }}>Solutions are not available for this exercise.</p>
            </div>
          )}

          {workTab === 'tracking' && (
            <div className="content-area">
              <h3 style={{ marginBottom: 12 }}>Exercise Tracking</h3>
              <table className="tracking-table">
                <thead>
                  <tr><th>#</th><th>Date</th><th>Result</th><th>Score</th></tr>
                </thead>
                <tbody>
                  <tr><td colSpan={4} style={{ color: '#888', textAlign: 'center' }}>
                    No submissions yet.
                  </td></tr>
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
