'use client';
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import SiteHeader from '@/components/SiteHeader';
import NotifBanner from '@/components/NotifBanner';
import { api, getUser, getToken } from '@/lib/api';
import type { CoursesResponse, Semester, Course } from '@/lib/api';

export default function CoursesPage() {
  const router = useRouter();
  const [data, setData]           = useState<CoursesResponse | null>(null);
  const [error, setError]         = useState('');
  const [collapsed, setCollapsed] = useState<Record<string, boolean>>({});
  const user = typeof window !== 'undefined' ? getUser() : null;

  useEffect(() => {
    if (!getToken()) { router.replace('/login'); return; }
    api.getCourses()
      .then(setData)
      .catch(err => {
        if (err.message?.includes('401') || err.message?.includes('Not authenticated')) {
          router.replace('/login');
        } else {
          setError(err.message ?? 'Failed to load courses');
        }
      });
  }, [router]);

  function toggleSemester(term: string) {
    setCollapsed(c => ({ ...c, [term]: !c[term] }));
  }

  if (error) return <div style={{ padding: 20, color: '#c0392b' }}>Error: {error}</div>;
  if (!data)  return <div style={{ padding: 20 }}>Loading courses…</div>;

  const isInstructor = data.role === 'instructor';

  return (
    <div className="page-wrap">
      <SiteHeader userName={user?.name ?? 'User'} />
      <NotifBanner />

      <main className="page-body">
        <div className="instr-bar">
          {isInstructor ? (
            <>
              <span>
                You are an Instructor of <strong>{data.total}</strong> course{data.total !== 1 ? 's' : ''}
              </span>
              <button className="btn btn-green btn-sm">+ Create a Course</button>
            </>
          ) : (
            <span>You are enrolled in <strong>{data.total}</strong> course{data.total !== 1 ? 's' : ''}</span>
          )}
        </div>

        <div className="courses-card">
          <div className="card-toolbar">
            <span style={{ fontWeight: 600, fontSize: 13 }}>
              <button className="btn btn-outline btn-sm">Open All</button>
            </span>
            <span className="toolbar-icons">
              <span className="ico" title="Refresh">↻</span>
              <span className="ico" title="Grid view">⊞</span>
              <span className="ico-gray" title="Help">?</span>
            </span>
          </div>

          {data.semesters.map((sem: Semester) => (
            <div key={sem.term} style={{ marginBottom: 16 }}>
              <button
                className="semester-toggle"
                onClick={() => toggleSemester(sem.term)}
              >
                <span style={{ fontSize: 10 }}>{collapsed[sem.term] ? '▶' : '▼'}</span>
                {sem.term}
              </button>

              {!collapsed[sem.term] && (
                <table className="courses-table">
                  <thead>
                    <tr>
                      <th>Go</th>
                      <th>Course</th>
                      <th>Course #</th>
                      <th>Title</th>
                      <th>Section</th>
                      <th>Instructor</th>
                      <th>Language</th>
                      <th>Access Code</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {sem.courses.map((c: Course) => (
                      <tr key={c.course_id}>
                        <td>
                          <button
                            className="btn btn-green btn-sm"
                            onClick={() => router.push(`/lab/${c.course_id}`)}
                          >
                            Go
                          </button>
                        </td>
                        <td style={{ fontWeight: 600 }}>
                          {c.course_id}
                        </td>
                        <td>{c.number}</td>
                        <td>{c.title}</td>
                        <td>
                          <span className="sec-tag">{c.section}</span>
                        </td>
                        <td>{c.instructor}</td>
                        <td>{c.language}</td>
                        <td>
                          <span style={{ fontFamily: 'monospace', fontSize: 12 }}>
                            {c.access_code || '—'}
                          </span>
                        </td>
                        <td>
                          <span className="row-actions">
                            {isInstructor && (
                              <>
                                <button className="btn btn-outline btn-sm">Edit</button>
                                <button className="btn btn-sm" style={{ background: '#e8e8e8', color: '#333' }}>
                                  Roster
                                </button>
                              </>
                            )}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </div>
          ))}
        </div>
      </main>
    </div>
  );
}
