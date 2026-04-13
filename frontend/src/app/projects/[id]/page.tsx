import React from 'react';

export default function ProjectWorkspace({ params }: { params: { id: string } }) {
  return (
    <main className="min-h-screen p-8 md:p-12 space-y-8">
      {/* Breadcrumbs & Navigation */}
      <nav className="flex gap-2 text-sm text-slate-500 items-center">
        <span className="hover:text-indigo-400 cursor-pointer">Workspaces</span>
        <span>/</span>
        <span className="text-white font-medium">Legacy Corp Site Review</span>
      </nav>

      {/* Hero Section */}
      <header className="flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Project: Legacy Corp (2004)</h1>
          <p className="text-slate-400">Reconstructing semantic architecture for Webflow migration.</p>
        </div>
        <div className="flex gap-3">
          <button className="bg-white/5 hover:bg-white/10 px-4 py-2 rounded-xl text-sm font-semibold transition-all">
            Export Draft
          </button>
          <button className="bg-indigo-600 hover:bg-indigo-500 text-white px-6 py-2 rounded-xl text-sm font-semibold transition-all">
            Finalize Migration
          </button>
        </div>
      </header>

      {/* Three Column Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        
        {/* Left: Audit Quick-Look (3 cols) */}
        <aside className="lg:col-span-3 space-y-6">
          <div className="glass-card p-5 space-y-4">
            <h3 className="text-xs font-bold uppercase tracking-widest text-slate-500">Audit Pulse</h3>
            <div className="space-y-3">
              <div className="flex justify-between items-center text-sm">
                <span className="text-slate-300">Crawl Depth</span>
                <span className="font-mono text-indigo-400">12/20</span>
              </div>
              <div className="flex justify-between items-center text-sm">
                <span className="text-slate-300">Broken Links</span>
                <span className="font-mono text-pink-500">42</span>
              </div>
              <div className="flex justify-between items-center text-sm">
                <span className="text-slate-300">Duplicate Titles</span>
                <span className="font-mono text-orange-400">128</span>
              </div>
            </div>
            <div className="pt-4 border-t border-white/5">
               <button className="w-full text-xs font-bold bg-white/5 py-2 rounded-lg hover:bg-white/10 transition-colors">
                Regenerate Audit
              </button>
            </div>
          </div>

          <div className="glass-card p-5 space-y-4 border-cyan-500/20">
            <h3 className="text-xs font-bold uppercase tracking-widest text-cyan-400">Canva Bridge</h3>
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded bg-cyan-500/10 flex items-center justify-center text-xl">🖼️</div>
              <div className="flex-1">
                <div className="text-sm font-bold">12 Assets Pushed</div>
                <div className="text-[10px] text-slate-500 uppercase">Synced 4m ago</div>
              </div>
            </div>
            <div className="space-y-2">
              <button className="w-full text-xs font-bold bg-cyan-500 hover:bg-cyan-400 text-white py-2 rounded-lg shadow-lg shadow-cyan-500/20 transition-all active:scale-95">
                 Generate Marketing Assets
              </button>
              <button className="w-full text-xs font-bold bg-white/5 text-slate-400 py-2 rounded-lg hover:bg-white/10 transition-colors">
                 Manage Templates
              </button>
            </div>
          </div>
        </aside>

        {/* Center: Component Review (6 cols) */}
        <section className="lg:col-span-6 space-y-6">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-bold">Reconstruction Review</h2>
            <div className="flex gap-2">
              <span className="text-xs bg-indigo-500/20 text-indigo-400 px-2 py-0.5 rounded">6 Components AI-Synthesized</span>
            </div>
          </div>

          {[
            { type: 'Hero', status: 'Pending', content: 'Modernized introductory section with optimized CTA.' },
            { type: 'FeatureList', status: 'Accepted', content: 'Service offerings mapped from nested legacy table layouts.' },
            { type: 'NarrativeBlock', status: 'Flagged', content: 'AI suggested introspection from 2004 mission statement.' }
          ].map((comp, i) => (
            <div key={i} className={`glass-card p-6 space-y-4 border-l-4 ${comp.status === 'Accepted' ? 'border-l-emerald-500' : comp.status === 'Flagged' ? 'border-l-orange-500' : 'border-l-indigo-500'}`}>
              <div className="flex justify-between items-center">
                <span className="text-xs font-black uppercase tracking-widest opacity-60">{comp.type}</span>
                <span className={`text-[10px] font-bold px-2 py-0.5 rounded ${comp.status === 'Accepted' ? 'bg-emerald-500/20 text-emerald-400' : 'bg-white/5 text-slate-400'}`}>
                  {comp.status}
                </span>
              </div>
              <p className="text-sm text-slate-300 leading-relaxed italic border-l-2 border-white/10 pl-4">
                "{comp.content}"
              </p>
              <div className="flex gap-2 pt-2">
                <button className="text-[10px] font-bold bg-emerald-500 hover:bg-emerald-600 text-white px-3 py-1.5 rounded transition-all">Accept</button>
                <button className="text-[10px] font-bold bg-white/5 hover:bg-white/10 px-3 py-1.5 rounded transition-all">Edit</button>
                <button className="text-[10px] font-bold bg-pink-500/10 hover:bg-pink-500/20 text-pink-400 px-3 py-1.5 rounded transition-all">Reject</button>
              </div>
            </div>
          ))}
        </section>

        {/* Right: Technical Metadata (3 cols) */}
        <aside className="lg:col-span-3 space-y-6 text-xs transform translate-y-2 opacity-80">
          <div className="space-y-4">
             <h3 className="font-bold uppercase tracking-widest text-slate-500">Technical Context</h3>
             <div className="space-y-4">
               <div className="space-y-1">
                 <div className="text-slate-500 uppercase text-[9px]">Original Site Generator</div>
                 <div className="font-mono">FrontPage 5.0 (2002)</div>
               </div>
               <div className="space-y-1">
                 <div className="text-slate-500 uppercase text-[9px]">LLM Parser Confidence</div>
                 <div className="text-indigo-400 font-bold">92.4%</div>
               </div>
               <div className="space-y-1">
                 <div className="text-slate-500 uppercase text-[9px]">Privacy Shield</div>
                 <div className="text-emerald-500 font-bold">Active (Enterprise Cloud)</div>
               </div>
             </div>
          </div>
        </aside>

      </div>
    </main>
  );
}
