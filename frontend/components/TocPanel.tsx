'use client';
import { useState } from 'react';
import { useRouter } from 'next/navigation';
import type { TopicNode, ExerciseRef } from '@/lib/api';

interface Props {
  courseId: string;
  tree: TopicNode[];
  activeExerciseId?: string;
}

function statusIcon(s: string) {
  if (s === 'correct')   return <span className="ex-icon ex-correct">✔</span>;
  if (s === 'wrong')     return <span className="ex-icon ex-wrong">✘</span>;
  if (s === 'attempted') return <span className="ex-icon ex-wrong">◐</span>;
  return <span className="ex-icon ex-blank">○</span>;
}

function TopicTree({ nodes, activeId }: { nodes: TopicNode[]; activeId?: string }) {
  return (
    <>
      {nodes.map(node => (
        <li key={node.id}>
          <TopicAccordion node={node} activeId={activeId} />
        </li>
      ))}
    </>
  );
}

function TopicAccordion({ node, activeId }: { node: TopicNode; activeId?: string }) {
  const [open, setOpen] = useState(true);
  const router = useRouter();
  return (
    <>
      <button
        className="tree-label"
        onClick={() => setOpen(o => !o)}
        title={node.label}
      >
        <span style={{ fontSize: 10, marginRight: 3 }}>{open ? '▼' : '▶'}</span>
        {node.label}
      </button>
      {open && (
        <ul className="tree-children">
          {node.exercises.map((ex: ExerciseRef) => (
            <li key={ex.id}>
              <button
                className={`tree-item${ex.id === activeId ? ' active' : ''}`}
                onClick={() => router.push(`/exercise/${ex.id}`)}
                title={ex.label}
              >
                {statusIcon(ex.status)}
                <span style={{ overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                  {ex.label}
                </span>
              </button>
            </li>
          ))}
          {node.children && (
            <TopicTree nodes={node.children} activeId={activeId} />
          )}
        </ul>
      )}
    </>
  );
}

export default function TocPanel({ courseId, tree, activeExerciseId }: Props) {
  const [collapsed, setCollapsed] = useState(false);
  const router = useRouter();

  return (
    <>
      <div className={`toc-panel${collapsed ? ' collapsed' : ''}`}>
        <div className="toc-header">
          <span className="toc-title">
            <span style={{ fontSize: 16, color: '#267a14' }}>☰</span>
            Table of Contents
          </span>
          <span className="toc-icons">
            <span title="Expand all">⊞</span>
            <span title="Collapse all">⊟</span>
          </span>
        </div>
        <div className="toc-body">
          <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
            <TopicTree nodes={tree} activeId={activeExerciseId} />
          </ul>
        </div>
      </div>
      <div
        className={`toc-handle${collapsed ? ' flipped' : ''}`}
        onClick={() => setCollapsed(c => !c)}
        title={collapsed ? 'Expand TOC' : 'Collapse TOC'}
        role="button"
        aria-label={collapsed ? 'Expand TOC' : 'Collapse TOC'}
      />
    </>
  );
}
