'use client';
import { useState } from 'react';

export default function NotifBanner() {
  const [visible, setVisible] = useState(true);
  if (!visible) return null;
  return (
    <div className="notif-banner">
      <span className="notif-left">
        <button className="notif-close" onClick={() => setVisible(false)} aria-label="Dismiss">✕</button>
        <span>
          <strong>Class(es) that you need to attend remotely are marked with a&nbsp;
          <span style={{ fontStyle: 'italic' }}>remote</span> tag below.</strong>
          &nbsp;Scroll down to see if this applies to you.
        </span>
      </span>
      <span className="notif-right">
        (Click X to dismiss this message)
      </span>
    </div>
  );
}
