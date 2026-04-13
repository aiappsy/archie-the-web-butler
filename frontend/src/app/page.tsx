import React from 'react';

export default function Home() {
  return (
    <main className="min-h-screen p-8 md:p-12 lg:p-24 space-y-12">
      {/* Header Section */}
      <header className="flex justify-between items-center animate-in fade-in slide-in-from-top-4 duration-1000">
        <div className="space-y-1">
          <h1 className="text-4xl font-bold archie-gradient-text tracking-tight">Archie – The Web Butler</h1>
          <p className="text-slate-400 font-medium">AI Content Reconstruction System (AICRS)</p>
        </div>
        <button className="bg-indigo-600 hover:bg-indigo-500 text-white px-6 py-2.5 rounded-xl font-semibold transition-all shadow-lg shadow-indigo-500/20 active:scale-95">
          New Reconstruction
        </button>
      </header>

      {/* Main Stats/Audit Section */}
      <section className="grid grid-cols-1 md:grid-cols-3 gap-6 animate-in fade-in slide-in-from-bottom-8 duration-700 delay-200">
        <div className="glass-card p-6 space-y-4">
          <div className="flex items-center justify-between">
            <span className="text-slate-400 text-sm font-semibold uppercase tracking-wider">Active Projects</span>
            <div className="w-2 h-2 rounded-full bg-emerald-500 shadow-[0_0_8px_rgba(16,185,129,0.8)]" />
          </div>
          <div className="text-4xl font-bold tracking-tight">12</div>
          <p className="text-xs text-slate-500 italic">4 pending reconstruction</p>
        </div>

        <div className="glass-card p-6 space-y-4">
          <span className="text-slate-400 text-sm font-semibold uppercase tracking-wider">Legacy Assets Identified</span>
          <div className="text-4xl font-bold tracking-tight">2.4k</div>
          <p className="text-xs text-slate-500 italic">Optimized to WebP via Archie</p>
        </div>

        <div className="glass-card p-6 space-y-4 border-indigo-500/20">
          <span className="text-slate-400 text-sm font-semibold uppercase tracking-wider">Agency ROI Impact</span>
          <div className="text-4xl font-bold tracking-tight text-indigo-400">+82%</div>
          <p className="text-xs text-slate-500 italic">Avg. project timeline reduction</p>
        </div>
      </section>

      {/* Projects List / Active Workspace */}
      <section className="space-y-6 animate-in fade-in slide-in-from-bottom-8 duration-1000 delay-500">
        <div className="flex items-center justify-between border-b border-white/5 pb-4">
          <h2 className="text-xl font-semibold">Active Workspaces</h2>
          <span className="text-sm text-indigo-400 hover:underline cursor-pointer">View All</span>
        </div>

        <div className="space-y-4">
          {/* Project Card Instance */}
          <div className="glass-card p-6 flex flex-col md:flex-row items-start md:items-center justify-between gap-6 hover:bg-white/[0.05]">
            <div className="flex gap-4 items-center">
              <div className="w-12 h-12 rounded-lg bg-indigo-500/20 flex items-center justify-center border border-indigo-500/30">
                <span className="text-indigo-400 font-bold text-xl">L</span>
              </div>
              <div>
                <h3 className="font-semibold text-lg">Legacy Corp Site (v2004)</h3>
                <p className="text-sm text-slate-500">Target: Webflow • 450 pages</p>
              </div>
            </div>
            
            <div className="flex gap-4 w-full md:w-auto">
              <div className="px-3 py-1 bg-white/5 rounded-full text-xs font-semibold text-slate-300 border border-white/10">
                Audit Phase Complete
              </div>
              <button className="flex-1 md:flex-none text-sm font-semibold bg-gradient-to-r from-cyan-500 to-indigo-500 hover:from-cyan-400 hover:to-indigo-400 text-white px-4 py-2 rounded-lg transition-all shadow-lg shadow-cyan-500/10 active:scale-95">
                Push to Canva
              </button>
              <button className="flex-1 md:flex-none text-sm font-semibold bg-white/10 hover:bg-white/20 px-4 py-2 rounded-lg transition-colors">
                Open Project
              </button>
            </div>
          </div>

          <div className="glass-card p-6 flex flex-col md:flex-row items-start md:items-center justify-between gap-6 opacity-60">
             <div className="flex gap-4 items-center">
              <div className="w-12 h-12 rounded-lg bg-pink-500/20 flex items-center justify-center border border-pink-500/30">
                <span className="text-pink-400 font-bold text-xl">S</span>
              </div>
              <div>
                <h3 className="font-semibold text-lg">Solomon Estate Real Estate</h3>
                <p className="text-sm text-slate-500">Target: WordPress • 82 pages</p>
              </div>
            </div>
            
            <div className="flex gap-4 w-full md:w-auto">
              <div className="px-3 py-1 bg-pink-500/20 rounded-full text-xs font-semibold text-pink-400 border border-pink-500/30">
                In Analysis...
              </div>
              <button className="flex-1 md:flex-none text-sm font-semibold bg-white/10 hover:bg-white/20 px-4 py-2 rounded-lg transition-colors">
                Monitor
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Bottom CTA / Branding */}
      <footer className="pt-12 border-t border-white/5 text-center space-y-2 opacity-50">
        <p className="text-sm">Powered by Advanced Agentic Code Reconstruction</p>
        <p className="text-xs uppercase tracking-[0.2em]">Sovereign • Semantic • Scalable</p>
      </footer>
    </main>
  );
}
