'use client';
import { useEffect, useState } from 'react';
import { useRouter, useParams } from 'next/navigation';
import LabHeader from '@/components/LabHeader';
import NotifBanner from '@/components/NotifBanner';
import TocPanel from '@/components/TocPanel';
import { api, getUser, getToken } from '@/lib/api';
import type { LabStructure, TopicNode, ExerciseRef } from '@/lib/api';

type Tab = 'topic' | 'tracking';

// Flatten tree to get a quick count of exercises by status
function countStatuses(tree: TopicNode[]): { correct: number; total: number } {
  let correct = 0; let total = 0;
  function walk(nodes: TopicNode[]) {
    for (const n of nodes) {
      for (const ex of n.exercises) {
        total++;
        if (ex.status === 'correct') correct++;
      }
      if (n.children) walk(n.children);
    }
  }
  walk(tree);
  return { correct, total };
}

function TocOverview({ tree, onSelectExercise }: {
  tree: TopicNode[];
  onSelectExercise: (id: string) => void;
}) {
  return (
    <div className="toc-overview">
      <h3>Table of Contents</h3>
      <ul className="toc-ov-tree">
        {tree.map(node => (
          <li key={node.id} className="indent-1">
            <span style={{ fontWeight: 600 }}>▶ {node.label}</span>
            <ul className="toc-ov-tree" style={{ marginLeft: 0 }}>
              {node.exercises.map((ex: ExerciseRef) => (
                <li key={ex.id} className="indent-2">
                  <span style={{
                    color: ex.status === 'correct' ? '#267a14'
                      : ex.status === 'wrong' ? '#c0392b' : '#888',
                    fontSize: 11
                  }}>
                    {ex.status === 'correct' ? '✔' : ex.status === 'wrong' ? '✘' : '○'}
                  </span>
                  <button
                    style={{ background: 'none', border: 'none', cursor: 'pointer', color: '#1a6bbf', fontSize: 13 }}
                    onClick={() => onSelectExercise(ex.id)}
                  >
                    {ex.label}
                  </button>
                </li>
              ))}
              {node.children?.map(child => (
                <li key={child.id} className="indent-2">
                  <span style={{ fontWeight: 600 }}>▶ {child.label}</span>
                </li>
              ))}
            </ul>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default function LabPage() {
  const router = useRouter();
  const params = useParams<{ courseId: string }>();
  const courseId = params.courseId;
  const user = typeof window !== 'undefined' ? getUser() : null;

  const [lab, setLab]   = useState<LabStructure | null>(null);
  const [tab, setTab]   = useState<Tab>('topic');
  const [error, setError] = useState('');

  useEffect(() => {
    if (!getToken()) { router.replace('/login'); return; }
    api.getLabStructure(courseId)
      .then(setLab)
      .catch(err => setError(err.message ?? 'Failed to load lab'));
  }, [courseId, router]);

  if (error) return <div style={{ padding: 20, color: '#c0392b' }}>Error: {error}</div>;
  if (!lab)  return <div style={{ padding: 20 }}>Loading lab…</div>;

  const { correct, total } = countStatuses(lab.tree);

  return (
    <div className="lab-wrap">
      <LabHeader userName={user?.name ?? 'User'} />
      <NotifBanner />

      <div className="lab-main">
        <TocPanel courseId={courseId} tree={lab.tree} />

        <div className="content-panel">
          <div className="tabs-bar">
            <div className="tabs-left">
              <button
                className={`tab-btn${tab === 'topic' ? ' active' : ''}`}
                onClick={() => setTab('topic')}
              >
                Topic
              </button>
              <button
                className={`tab-btn${tab === 'tracking' ? ' active' : ''}`}
                onClick={() => setTab('tracking')}
              >
                Tracking
              </button>
            </div>
            <div className="tabs-right">
              <span title="Refresh">↻</span>
              <span title="Help">?</span>
            </div>
          </div>

          <div className="content-area">
            {tab === 'topic' && (
              <>
                <div className="breadcrumb">
                  {lab.title}
                </div>

                <div style={{ display: 'flex', gap: 16, marginBottom: 14, flexWrap: 'wrap' }}>
                  <div className="badges">
                    <span className="badge badge-correct">{correct} Done</span>
                    <span className="badge badge-dash">{total - correct} Remaining</span>
                    <span className="badge badge-circle">{total} Total</span>
                  </div>
                </div>

                <TocOverview
                  tree={lab.tree}
                  onSelectExercise={id => router.push(`/exercise/${id}`)}
                />
              </>
            )}

            {tab === 'tracking' && (
              <div>
                <h3 style={{ marginBottom: 12, fontSize: 14 }}>Progress Tracking</h3>
                <table className="tracking-table">
                  <thead>
                    <tr>
                      <th>Exercise</th>
                      <th>Status</th>
                      <th>Score</th>
                    </tr>
                  </thead>
                  <tbody>
                    {lab.tree.flatMap(n => n.exercises).map((ex: ExerciseRef) => (
                      <tr key={ex.id}>
                        <td>
                          <button
                            style={{ background: 'none', border: 'none', color: '#1a6bbf', cursor: 'pointer', fontSize: 12 }}
                            onClick={() => router.push(`/exercise/${ex.id}`)}
                          >
                            {ex.label}
                          </button>
                        </td>
                        <td style={{
                          color: ex.status === 'correct' ? '#267a14'
                            : ex.status === 'wrong' ? '#c0392b' : '#888'
                        }}>
                          {ex.status === 'correct' ? '✔ Correct'
                            : ex.status === 'wrong' ? '✘ Wrong'
                            : '— Not attempted'}
                        </td>
                        <td>{ex.status === 'correct' ? '100%' : ex.status === 'wrong' ? '0%' : '—'}</td>
                      </tr>
                    ))}
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
