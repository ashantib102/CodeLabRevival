'use client';
import { useState, FormEvent, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import SiteHeader from '@/components/SiteHeader';
import NotifBanner from '@/components/NotifBanner';
import { api, getUser, getToken } from '@/lib/api';
import type { SampleRun } from '@/lib/api';

interface SampleRunForm extends SampleRun {
  id: string;
}

export default function CreateExercisePage() {
  const router = useRouter();
  const user = typeof window !== 'undefined' ? getUser() : null;

  const [title, setTitle] = useState('');
  const [instructions, setInstructions] = useState('');
  const [topic, setTopic] = useState('');
  const [starterCode, setStarterCode] = useState('');
  const [sampleRuns, setSampleRuns] = useState<SampleRunForm[]>([
    { id: '1', input: '', output: '' }
  ]);

  const [titleErr, setTitleErr] = useState('');
  const [instructionsErr, setInstructionsErr] = useState('');
  const [topicErr, setTopicErr] = useState('');
  const [submitErr, setSubmitErr] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!getToken()) {
      router.replace('/login');
      return;
    }
    if (user?.role !== 'instructor') {
      router.replace('/courses');
      return;
    }
  }, [router, user]);

  const addSampleRun = () => {
    const newId = (sampleRuns.length + 1).toString();
    setSampleRuns([...sampleRuns, { id: newId, input: '', output: '' }]);
  };

  const removeSampleRun = (id: string) => {
    if (sampleRuns.length > 1) {
      setSampleRuns(sampleRuns.filter(run => run.id !== id));
    }
  };

  const updateSampleRun = (id: string, field: 'input' | 'output', value: string) => {
    setSampleRuns(sampleRuns.map(run =>
      run.id === id ? { ...run, [field]: value } : run
    ));
  };

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setTitleErr('');
    setInstructionsErr('');
    setTopicErr('');
    setSubmitErr('');
    setSuccess('');

    let valid = true;
    if (!title.trim()) {
      setTitleErr('Please enter a title');
      valid = false;
    }
    if (!instructions.trim()) {
      setInstructionsErr('Please enter instructions');
      valid = false;
    }
    if (!topic.trim()) {
      setTopicErr('Please enter a topic');
      valid = false;
    }

    if (!valid) return;

    setLoading(true);
    try {
      const exerciseData = {
        title: title.trim(),
        instructions: instructions.trim(),
        topic: topic.trim(),
        starter_code: starterCode.trim(),
        sample_runs: sampleRuns.map(({ id, ...run }) => run),
      };

      await api.createExercise(exerciseData);
      setSuccess('Exercise created successfully! Redirecting...');
      setTimeout(() => router.push('/courses'), 2000);
    } catch (err: unknown) {
      setSubmitErr(err instanceof Error ? err.message : 'Failed to create exercise');
    } finally {
      setLoading(false);
    }
  }

  if (!user || user.role !== 'instructor') {
    return <div style={{ padding: 20 }}>Access denied. Instructor access required.</div>;
  }

  return (
    <div className="page-wrap">
      <SiteHeader userName={user.name} userRole={user.role} />
      <NotifBanner />

      <main className="page-body">
        <div style={{ maxWidth: 800, margin: '0 auto' }}>
          <h2 style={{ marginBottom: 20, color: '#267a14' }}>Create New Exercise</h2>

          {submitErr && (
            <p style={{ color: '#c0392b', marginBottom: 16, padding: 12, background: '#ffeaea', borderRadius: 4 }}>
              ⚠ {submitErr}
            </p>
          )}

          {success && (
            <p style={{ color: '#27ae60', marginBottom: 16, padding: 12, background: '#eaffea', borderRadius: 4 }}>
              ✓ {success}
            </p>
          )}

          <form onSubmit={handleSubmit}>
            <div style={{ marginBottom: 20 }}>
              <label style={{ display: 'block', marginBottom: 6, fontWeight: 600 }}>
                Exercise Title *
              </label>
              <input
                type="text"
                value={title}
                onChange={e => setTitle(e.target.value)}
                placeholder="e.g., Hello World Program"
                style={{
                  width: '100%',
                  padding: '8px 12px',
                  border: titleErr ? '1px solid #c0392b' : '1px solid #ccc',
                  borderRadius: 4,
                  fontSize: 14
                }}
              />
              {titleErr && <span style={{ color: '#c0392b', fontSize: 12 }}>{titleErr}</span>}
            </div>

            <div style={{ marginBottom: 20 }}>
              <label style={{ display: 'block', marginBottom: 6, fontWeight: 600 }}>
                Topic/Category *
              </label>
              <input
                type="text"
                value={topic}
                onChange={e => setTopic(e.target.value)}
                placeholder="e.g., CODELAB WARMUP, IMPERATIVE PROGRAMMING"
                style={{
                  width: '100%',
                  padding: '8px 12px',
                  border: topicErr ? '1px solid #c0392b' : '1px solid #ccc',
                  borderRadius: 4,
                  fontSize: 14
                }}
              />
              {topicErr && <span style={{ color: '#c0392b', fontSize: 12 }}>{topicErr}</span>}
            </div>

            <div style={{ marginBottom: 20 }}>
              <label style={{ display: 'block', marginBottom: 6, fontWeight: 600 }}>
                Instructions * (HTML supported)
              </label>
              <textarea
                value={instructions}
                onChange={e => setInstructions(e.target.value)}
                placeholder="Describe the exercise requirements..."
                rows={6}
                style={{
                  width: '100%',
                  padding: '8px 12px',
                  border: instructionsErr ? '1px solid #c0392b' : '1px solid #ccc',
                  borderRadius: 4,
                  fontSize: 14,
                  fontFamily: 'monospace'
                }}
              />
              {instructionsErr && <span style={{ color: '#c0392b', fontSize: 12 }}>{instructionsErr}</span>}
            </div>

            <div style={{ marginBottom: 20 }}>
              <label style={{ display: 'block', marginBottom: 6, fontWeight: 600 }}>
                Starter Code (Optional)
              </label>
              <textarea
                value={starterCode}
                onChange={e => setStarterCode(e.target.value)}
                placeholder="Provide initial code template..."
                rows={8}
                style={{
                  width: '100%',
                  padding: '8px 12px',
                  border: '1px solid #ccc',
                  borderRadius: 4,
                  fontSize: 13,
                  fontFamily: 'SFMono-Regular, Consolas, monospace',
                  lineHeight: 1.4
                }}
              />
            </div>

            <div style={{ marginBottom: 20 }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 10 }}>
                <label style={{ fontWeight: 600 }}>Sample Runs</label>
                <button
                  type="button"
                  onClick={addSampleRun}
                  style={{
                    padding: '4px 8px',
                    background: '#267a14',
                    color: 'white',
                    border: 'none',
                    borderRadius: 3,
                    cursor: 'pointer',
                    fontSize: 12
                  }}
                >
                  + Add Sample
                </button>
              </div>

              {sampleRuns.map((run, index) => (
                <div key={run.id} style={{
                  border: '1px solid #ddd',
                  borderRadius: 4,
                  padding: 12,
                  marginBottom: 10,
                  background: '#fafafa'
                }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
                    <span style={{ fontWeight: 600, fontSize: 13 }}>Sample {index + 1}</span>
                    {sampleRuns.length > 1 && (
                      <button
                        type="button"
                        onClick={() => removeSampleRun(run.id)}
                        style={{
                          padding: '2px 6px',
                          background: '#c0392b',
                          color: 'white',
                          border: 'none',
                          borderRadius: 3,
                          cursor: 'pointer',
                          fontSize: 11
                        }}
                      >
                        Remove
                      </button>
                    )}
                  </div>

                  <div style={{ display: 'flex', gap: 10 }}>
                    <div style={{ flex: 1 }}>
                      <label style={{ display: 'block', marginBottom: 4, fontSize: 12, fontWeight: 600 }}>
                        Input
                      </label>
                      <textarea
                        value={run.input}
                        onChange={e => updateSampleRun(run.id, 'input', e.target.value)}
                        placeholder="Program input..."
                        rows={3}
                        style={{
                          width: '100%',
                          padding: '6px 8px',
                          border: '1px solid #ccc',
                          borderRadius: 3,
                          fontSize: 12,
                          fontFamily: 'monospace'
                        }}
                      />
                    </div>
                    <div style={{ flex: 1 }}>
                      <label style={{ display: 'block', marginBottom: 4, fontSize: 12, fontWeight: 600 }}>
                        Expected Output
                      </label>
                      <textarea
                        value={run.output}
                        onChange={e => updateSampleRun(run.id, 'output', e.target.value)}
                        placeholder="Expected output..."
                        rows={3}
                        style={{
                          width: '100%',
                          padding: '6px 8px',
                          border: '1px solid #ccc',
                          borderRadius: 3,
                          fontSize: 12,
                          fontFamily: 'monospace'
                        }}
                      />
                    </div>
                  </div>
                </div>
              ))}
            </div>

            <div style={{ display: 'flex', gap: 12, justifyContent: 'center', marginTop: 30 }}>
              <button
                type="button"
                onClick={() => router.push('/courses')}
                style={{
                  padding: '10px 20px',
                  background: '#666',
                  color: 'white',
                  border: 'none',
                  borderRadius: 4,
                  cursor: 'pointer'
                }}
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={loading}
                style={{
                  padding: '10px 30px',
                  background: '#267a14',
                  color: 'white',
                  border: 'none',
                  borderRadius: 4,
                  cursor: loading ? 'not-allowed' : 'pointer',
                  fontWeight: 600
                }}
              >
                {loading ? 'Creating...' : 'Create Exercise'}
              </button>
            </div>
          </form>
        </div>
      </main>
    </div>
  );
}