// SVG logo box + text used in both headers
export default function CodeLogo({ small = false }: { small?: boolean }) {
  const sz = small ? 32 : 42;
  return (
    <a href="/courses" className="logo-wrap">
      <svg width={sz} height={sz} viewBox="0 0 42 42" fill="none" aria-hidden>
        <rect width="42" height="42" rx="4" fill="#267a14" />
        <text x="50%" y="54%" dominantBaseline="middle" textAnchor="middle"
          fontSize="20" fontWeight="bold" fill="white" fontFamily="monospace">&gt;_</text>
      </svg>
      <div className="logo-text">
        <span className="logo-name" style={small ? { fontSize: 20 } : {}}>CodeLab</span>
        <span className="logo-by">by TuringsCraft</span>
      </div>
    </a>
  );
}
