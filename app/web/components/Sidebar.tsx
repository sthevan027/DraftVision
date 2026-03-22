'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';

const items = [
  { href: '/', label: 'Início' },
  { href: '/dashboard', label: 'Dashboard' },
  { href: '/players', label: 'Jogadores' },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-56 min-h-screen bg-surface border-r border-zinc-700/50 flex flex-col">
      <div className="p-4 border-b border-zinc-700/50">
        <Link href="/" className="text-xl font-bold text-primary">
          DraftVision
        </Link>
      </div>
      <nav className="flex-1 p-2">
        {items.map(({ href, label }) => (
          <Link
            key={href}
            href={href}
            className={`block px-4 py-2 rounded-lg text-sm transition-colors ${
              pathname === href || (href !== '/' && pathname.startsWith(href))
                ? 'bg-primary/20 text-primary'
                : 'text-zinc-400 hover:text-zinc-100 hover:bg-zinc-800/50'
            }`}
          >
            {label}
          </Link>
        ))}
      </nav>
    </aside>
  );
}
