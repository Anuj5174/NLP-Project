import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'

import {
  Brain, Zap, Target, BarChart3, Search, Users,
  ArrowRight, ChevronRight, Shield, Clock, TrendingUp,
  FileText, Briefcase, CheckCircle, Star, Cpu, Upload,
  GitMerge, Award, Github, Mail
} from 'lucide-react'

export default function LandingPage() {
  const navigate = useNavigate()
  const [scrolled, setScrolled] = useState(false)
  const [count1, setCount1] = useState(0)
  const [count2, setCount2] = useState(0)
  const [count3, setCount3] = useState(0)

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 40)
    window.addEventListener('scroll', onScroll)
    return () => window.removeEventListener('scroll', onScroll)
  }, [])

  useEffect(() => {
    const animCount = (target, setter, duration) => {
      let start = 0
      const step = target / (duration / 16)
      const timer = setInterval(() => {
        start += step
        if (start >= target) { setter(target); clearInterval(timer) }
        else setter(Math.floor(start))
      }, 16)
    }
    const delay = setTimeout(() => {
      animCount(95, setCount1, 1500)
      animCount(500, setCount2, 1800)
      animCount(90, setCount3, 1400)
    }, 600)
    return () => clearTimeout(delay)
  }, [])

  return (
    <div style={{ fontFamily: "'Plus Jakarta Sans', sans-serif", background: '#060810', color: '#e2e5f0', overflowX: 'hidden' }}>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
        html { scroll-behavior: smooth; }
        ::selection { background: #3b6fff30; color: #fff; }
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: #060810; }
        ::-webkit-scrollbar-thumb { background: #1e2235; border-radius: 3px; }

        .btn-main {
          display: inline-flex; align-items: center; gap: 8px;
          background: #3b6fff; color: #fff; border: none;
          border-radius: 10px; padding: 13px 28px;
          font-size: 14px; font-weight: 700; cursor: pointer;
          font-family: 'Plus Jakarta Sans', sans-serif;
          transition: all 0.2s;
          box-shadow: 0 0 0 1px #3b6fff, 0 8px 24px #3b6fff30;
        }
        .btn-main:hover {
          background: #4d7bff;
          box-shadow: 0 0 0 1px #4d7bff, 0 12px 36px #3b6fff50;
          transform: translateY(-1px);
        }
        .btn-ghost {
          display: inline-flex; align-items: center; gap: 8px;
          background: transparent; color: #a0a8c0;
          border: 1px solid #1e2235; border-radius: 10px;
          padding: 12px 24px; font-size: 14px; font-weight: 600;
          cursor: pointer; font-family: 'Plus Jakarta Sans', sans-serif;
          transition: all 0.2s;
        }
        .btn-ghost:hover { border-color: #3b6fff50; color: #e2e5f0; background: #3b6fff08; }

        .nav-btn {
          background: none; border: none; color: #7880a0;
          font-size: 14px; font-weight: 500; cursor: pointer;
          font-family: 'Plus Jakarta Sans', sans-serif;
          padding: 6px 0; transition: color 0.15s;
        }
        .nav-btn:hover { color: #e2e5f0; }

        .feature-card {
          background: #0b0d1a; border: 1px solid #161929;
          border-radius: 18px; padding: 30px;
          transition: all 0.3s; cursor: default;
        }
        .feature-card:hover {
          border-color: #3b6fff30; background: #0e1120;
          transform: translateY(-4px);
          box-shadow: 0 20px 60px #00000050;
        }

        .step-num {
          font-family: 'Instrument Serif', serif; font-style: italic;
          font-size: 72px; line-height: 1; color: #3b6fff15;
          position: absolute; top: 16px; right: 20px;
          pointer-events: none; user-select: none;
        }

        .tech-pill {
          display: inline-flex; align-items: center; gap: 7px;
          background: #0b0d1a; border: 1px solid #161929;
          border-radius: 50px; padding: 8px 16px;
          font-size: 13px; font-weight: 500; color: #7880a0;
          transition: all 0.2s;
        }
        .tech-pill:hover { border-color: #3b6fff40; color: #e2e5f0; }

        .glow { position: absolute; border-radius: 50%; filter: blur(100px); pointer-events: none; z-index: 0; }

        @keyframes fadeUp {
          from { opacity: 0; transform: translateY(24px); }
          to   { opacity: 1; transform: translateY(0); }
        }
        @keyframes float {
          0%,100% { transform: translateY(0); }
          50%      { transform: translateY(-10px); }
        }
        @keyframes ping {
          0%,100% { opacity: 1; } 50% { opacity: 0.4; }
        }

        .anim-1 { animation: fadeUp 0.6s ease 0.05s both; }
        .anim-2 { animation: fadeUp 0.6s ease 0.15s both; }
        .anim-3 { animation: fadeUp 0.6s ease 0.28s both; }
        .anim-4 { animation: fadeUp 0.6s ease 0.42s both; }
        .floating { animation: float 5s ease-in-out infinite; }
        .ping { animation: ping 2s ease-in-out infinite; }

        .stat-divider { border-right: 1px solid #161929; }
        .stat-divider:last-child { border-right: none; }

        @media (max-width: 900px) {
          .hero-inner { flex-direction: column !important; }
          .hero-visual { display: none !important; }
          .feat-grid { grid-template-columns: 1fr 1fr !important; }
          .steps-grid { grid-template-columns: 1fr !important; }
          .stat-divider { border-right: none !important; border-bottom: 1px solid #161929; }
          .stats-row { grid-template-columns: 1fr !important; }
        }
        @media (max-width: 600px) {
          .feat-grid { grid-template-columns: 1fr !important; }
        }

        @media (max-width: 768px) {
        .desktop-nav { display: none !important; }
        .hero-inner { flex-direction: column !important; gap: 40px !important; }
        .hero-visual { display: none !important; }
        .feat-grid { grid-template-columns: 1fr !important; }
        .steps-grid { grid-template-columns: 1fr !important; }
        .stats-row { grid-template-columns: 1fr !important; }
        .stat-divider { border-right: none !important; border-bottom: 1px solid #161929; }
        section { padding: 60px 20px !important; }
        nav { padding: 0 16px !important; }
      }

      @media (max-width: 480px) {
      h1 { font-size: 36px !important; }
      .btn-ghost { display: none; }
      }
      `}</style>

      {/* NAV */}
      <nav style={{
       position: 'fixed', top: 0, left: 0, right: 0, zIndex: 1000,
       height: '64px', padding: '0 20px',
       display: 'flex', alignItems: 'center', justifyContent: 'space-between',
       background: scrolled ? 'rgba(6,8,16,0.90)' : 'transparent',
       backdropFilter: scrolled ? 'blur(24px)' : 'none',
       borderBottom: scrolled ? '1px solid #161929' : 'none',
       transition: 'all 0.3s'
}}>
  {/* Logo */}
  <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
    <div style={{ width: '34px', height: '34px', borderRadius: '9px', background: 'linear-gradient(135deg, #3b6fff, #7c5cfc)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      <Cpu size={17} color="#fff" strokeWidth={2} />
    </div>
    <span style={{ fontFamily: 'Plus Jakarta Sans', fontWeight: 800, fontSize: '16px', letterSpacing: '-0.4px' }}>RecruitAI</span>
  </div>

  {/* Center links — HIDDEN on mobile */}
  <div style={{ display: 'flex', gap: '28px' }}
    className="desktop-nav">
    {[['features', 'Features'], ['how-it-works', 'How it works'], ['about', 'About']].map(([id, label]) => (
      <button key={id} className="nav-btn" onClick={() => document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' })}>{label}</button>
    ))}
  </div>

      {/* Right CTA */}
      <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
      <button className="nav-btn" onClick={() => navigate('/login')} style={{ display: window.innerWidth < 480 ? 'none' : 'block' }}>Sign in</button>
       <button className="btn-main" style={{ padding: '9px 16px', fontSize: '13px' }} onClick={() => navigate('/register')}>
      Get Started <ArrowRight size={14} />
       </button>
      </div>
     </nav>

      {/* HERO */}
      <section style={{ position: 'relative', minHeight: '100vh', display: 'flex', alignItems: 'center', padding: '120px 40px 80px', overflow: 'hidden' }}>
        <div className="glow" style={{ width: '700px', height: '700px', background: '#3b6fff', opacity: 0.05, top: '-200px', left: '-200px' }} />
        <div className="glow" style={{ width: '500px', height: '500px', background: '#7c5cfc', opacity: 0.06, top: '0', right: '-100px' }} />
        <div style={{
          position: 'absolute', inset: 0, zIndex: 0,
          backgroundImage: 'linear-gradient(#161929 1px, transparent 1px), linear-gradient(90deg, #161929 1px, transparent 1px)',
          backgroundSize: '60px 60px', opacity: 0.2,
          maskImage: 'radial-gradient(ellipse 80% 60% at 50% 40%, black 20%, transparent 100%)',
          WebkitMaskImage: 'radial-gradient(ellipse 80% 60% at 50% 40%, black 20%, transparent 100%)'
        }} />

        <div style={{ maxWidth: '1200px', margin: '0 auto', width: '100%', position: 'relative', zIndex: 1 }}>
          <div className="hero-inner" style={{ display: 'flex', alignItems: 'center', gap: '72px' }}>

            {/* LEFT */}
            <div style={{ flex: '1 1 520px' }}>
              <div className="anim-1" style={{
                display: 'inline-flex', alignItems: 'center', gap: '8px',
                background: '#3b6fff12', border: '1px solid #3b6fff30',
                borderRadius: '50px', padding: '6px 14px 6px 10px', marginBottom: '28px'
              }}>
                <span style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', width: '20px', height: '20px', borderRadius: '50%', background: '#3b6fff' }}>
                  <Zap size={11} color="#fff" strokeWidth={2.5} />
                </span>
                <span style={{ fontSize: '12px', fontWeight: 600, color: '#6b8fff', letterSpacing: '0.3px' }}>AI-Powered Resume Matching</span>
              </div>

              <h1 className="anim-2" style={{
                fontFamily: "'Instrument Serif', serif",
                fontSize: 'clamp(44px, 5.5vw, 76px)', fontWeight: 400,
                lineHeight: 1.08, letterSpacing: '-1px', marginBottom: '24px', color: '#f0f2ff'
              }}>
                Hire the right people,{' '}
                <span style={{ fontStyle: 'italic', color: '#3b6fff' }}>faster.</span>
              </h1>

              <p className="anim-3" style={{ fontSize: '17px', color: '#5a6380', lineHeight: 1.75, maxWidth: '460px', marginBottom: '40px', fontWeight: 400 }}>
                Upload resumes, add a job description, and watch our AI rank every candidate by skill match score — in seconds, not hours.
              </p>

              <div className="anim-4" style={{ display: 'flex', gap: '12px', flexWrap: 'wrap', marginBottom: '48px' }}>
                <button className="btn-main" style={{ fontSize: '15px', padding: '14px 30px' }} onClick={() => navigate('/register')}>
                  Start for free <ArrowRight size={15} />
                </button>
                <button className="btn-ghost" style={{ fontSize: '15px', padding: '13px 24px' }} onClick={() => navigate('/login')}>
                  View live demo
                </button>
              </div>

              <div className="anim-4" style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                <div style={{ display: 'flex' }}>
                  {[...Array(5)].map((_, i) => <Star key={i} size={13} fill="#f59e0b" color="#f59e0b" style={{ marginRight: '2px' }} />)}
                </div>
                <span style={{ fontSize: '13px', color: '#3c4560' }}>
                  Built with <span style={{ color: '#5a6380' }}>FastAPI ·BERT · spaCy · TF-IDF · React</span>
                </span>
              </div>
            </div>

            {/* RIGHT MOCKUP */}
            <div className="hero-visual floating" style={{ flex: '0 0 420px', position: 'relative' }}>
              <div style={{ background: '#0b0d1a', border: '1px solid #161929', borderRadius: '22px', padding: '24px', boxShadow: '0 40px 120px #00000070' }}>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '20px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                    <div style={{ width: '36px', height: '36px', borderRadius: '9px', background: '#3b6fff15', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                      <FileText size={16} color="#3b6fff" strokeWidth={2} />
                    </div>
                    <div>
                      <div style={{ fontSize: '13px', fontWeight: 600, color: '#e2e5f0' }}>resume_senior_dev.pdf</div>
                      <div style={{ fontSize: '11px', color: '#3c4560', marginTop: '1px' }}>Analyzed · 2s ago</div>
                    </div>
                  </div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '5px', background: '#10b98115', border: '1px solid #10b98130', borderRadius: '50px', padding: '4px 10px' }}>
                    <CheckCircle size={11} color="#10b981" strokeWidth={2.5} />
                    <span style={{ fontSize: '11px', fontWeight: 600, color: '#10b981' }}>Parsed</span>
                  </div>
                </div>

                <div style={{ background: '#060810', borderRadius: '14px', padding: '20px', marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '20px' }}>
                  <div style={{ position: 'relative', width: '88px', height: '88px', flexShrink: 0 }}>
                    <svg width="88" height="88" viewBox="0 0 88 88" style={{ transform: 'rotate(-90deg)' }}>
                      <circle cx="44" cy="44" r="36" fill="none" stroke="#161929" strokeWidth="7" />
                      <circle cx="44" cy="44" r="36" fill="none" stroke="url(#scoreGrad)" strokeWidth="7"
                        strokeDasharray={`${2 * Math.PI * 36 * 0.87} ${2 * Math.PI * 36}`} strokeLinecap="round" />
                      <defs>
                        <linearGradient id="scoreGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                          <stop offset="0%" stopColor="#3b6fff" /><stop offset="100%" stopColor="#7c5cfc" />
                        </linearGradient>
                      </defs>
                    </svg>
                    <div style={{ position: 'absolute', inset: 0, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
                      <span style={{ fontFamily: 'Plus Jakarta Sans', fontWeight: 800, fontSize: '20px', color: '#e2e5f0', letterSpacing: '-0.5px' }}>87%</span>
                      <span style={{ fontSize: '9px', color: '#3c4560', fontWeight: 600, letterSpacing: '0.3px' }}>MATCH</span>
                    </div>
                  </div>
                  <div style={{ flex: 1 }}>
                    <div style={{ fontSize: '15px', fontWeight: 700, color: '#e2e5f0', marginBottom: '4px' }}>Senior Python Dev</div>
                    <div style={{ fontSize: '12px', color: '#3c4560', marginBottom: '12px' }}>TechCorp Inc. · Full-time</div>
                    <div style={{ display: 'inline-flex', alignItems: 'center', gap: '5px', background: '#10b98112', border: '1px solid #10b98128', borderRadius: '6px', padding: '4px 10px' }}>
                      <Award size={11} color="#10b981" strokeWidth={2.5} />
                      <span style={{ fontSize: '11px', fontWeight: 700, color: '#10b981' }}>Highly Recommended</span>
                    </div>
                  </div>
                </div>

                <div style={{ marginBottom: '14px' }}>
                  <div style={{ fontSize: '10px', fontWeight: 700, color: '#3c4560', letterSpacing: '1px', marginBottom: '10px' }}>MATCHED SKILLS</div>
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
                    {['Python', 'FastAPI', 'PostgreSQL', 'spaCy', 'REST APIs', 'Docker'].map(s => (
                      <span key={s} style={{ background: '#3b6fff12', color: '#6b8fff', border: '1px solid #3b6fff22', borderRadius: '6px', padding: '4px 10px', fontSize: '11px', fontWeight: 600 }}>{s}</span>
                    ))}
                  </div>
                </div>

                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', padding: '10px 14px', background: '#ef444410', border: '1px solid #ef444420', borderRadius: '10px' }}>
                  <Search size={12} color="#f87171" strokeWidth={2.5} />
                  <span style={{ fontSize: '12px', color: '#f87171', fontWeight: 500 }}>Skill gap: Kubernetes, Terraform</span>
                </div>
              </div>

              {/* Floating TL */}
              <div style={{ position: 'absolute', top: '-18px', right: '-20px', background: '#0b0d1a', border: '1px solid #161929', borderRadius: '14px', padding: '12px 18px', boxShadow: '0 16px 48px #00000060' }}>
                <div style={{ fontSize: '10px', color: '#3c4560', fontWeight: 600, letterSpacing: '0.5px', marginBottom: '4px' }}>RESUMES RANKED</div>
                <div style={{ fontFamily: 'Plus Jakarta Sans', fontWeight: 800, fontSize: '24px', color: '#3b6fff', letterSpacing: '-1px' }}>2,847</div>
              </div>

              {/* Floating BL */}
              <div style={{ position: 'absolute', bottom: '-14px', left: '-20px', background: '#0b0d1a', border: '1px solid #161929', borderRadius: '14px', padding: '12px 18px', boxShadow: '0 16px 48px #00000060', display: 'flex', alignItems: 'center', gap: '10px' }}>
                <div style={{ width: '32px', height: '32px', borderRadius: '8px', background: '#10b98115', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                  <TrendingUp size={15} color="#10b981" strokeWidth={2} />
                </div>
                <div>
                  <div style={{ fontSize: '10px', color: '#3c4560', fontWeight: 600, letterSpacing: '0.5px' }}>TIME SAVED</div>
                  <div style={{ fontFamily: 'Plus Jakarta Sans', fontWeight: 800, fontSize: '20px', color: '#10b981', letterSpacing: '-0.5px' }}>95%</div>
                </div>
              </div>

              {/* Live dot */}
              <div style={{ position: 'absolute', top: '14px', left: '-14px', display: 'flex', alignItems: 'center', gap: '6px', background: '#0b0d1a', border: '1px solid #161929', borderRadius: '50px', padding: '6px 12px', boxShadow: '0 8px 24px #00000040' }}>
                <span className="ping" style={{ width: '7px', height: '7px', borderRadius: '50%', background: '#10b981', display: 'block' }} />
                <span style={{ fontSize: '11px', color: '#10b981', fontWeight: 600 }}>AI Running</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* STATS */}
      <div style={{ borderTop: '1px solid #161929', borderBottom: '1px solid #161929' }}>
        <div style={{ maxWidth: '1200px', margin: '0 auto', display: 'grid', gridTemplateColumns: 'repeat(3,1fr)' }} className="stats-row">
          {[
            { icon: <Clock size={20} color="#3b6fff" strokeWidth={2} />, val: count1 + '%', label: 'Faster than manual review' },
            { icon: <Brain size={20} color="#7c5cfc" strokeWidth={2} />, val: count2 + '+', label: 'Skills in database' },
            { icon: <Target size={20} color="#10b981" strokeWidth={2} />, val: count3 + '%+', label: 'Matching accuracy' },
          ].map((s, i) => (
            <div key={i} className="stat-divider" style={{ padding: '40px 32px', display: 'flex', alignItems: 'center', gap: '20px' }}>
              <div style={{ width: '48px', height: '48px', borderRadius: '12px', background: '#0b0d1a', border: '1px solid #161929', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>{s.icon}</div>
              <div>
                <div style={{ fontFamily: 'Plus Jakarta Sans', fontWeight: 800, fontSize: '32px', letterSpacing: '-1px', color: '#e2e5f0', lineHeight: 1 }}>{s.val}</div>
                <div style={{ fontSize: '13px', color: '#3c4560', marginTop: '5px', fontWeight: 500 }}>{s.label}</div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* FEATURES */}
      <section id="features" style={{ padding: '110px 40px', position: 'relative', overflow: 'hidden' }}>
        <div className="glow" style={{ width: '500px', height: '500px', background: '#7c5cfc', opacity: 0.05, top: '0', right: '-100px' }} />
        <div style={{ maxWidth: '1200px', margin: '0 auto', position: 'relative', zIndex: 1 }}>
          <div style={{ marginBottom: '60px', maxWidth: '600px' }}>
            <div style={{ display: 'inline-flex', alignItems: 'center', gap: '6px', background: '#3b6fff10', border: '1px solid #3b6fff25', borderRadius: '50px', padding: '5px 14px', marginBottom: '18px' }}>
              <Zap size={12} color="#6b8fff" strokeWidth={2.5} />
              <span style={{ fontSize: '12px', fontWeight: 700, color: '#6b8fff', letterSpacing: '0.5px' }}>FEATURES</span>
            </div>
            <h2 style={{ fontFamily: "'Instrument Serif', serif", fontWeight: 400, fontSize: 'clamp(32px, 4vw, 54px)', lineHeight: 1.1, letterSpacing: '-0.5px', color: '#f0f2ff', marginBottom: '16px' }}>
              Everything you need to<br />
              <span style={{ fontStyle: 'italic', color: '#3b6fff' }}>hire with confidence</span>
            </h2>
            <p style={{ fontSize: '16px', color: '#3c4560', lineHeight: 1.7 }}>A complete AI recruitment pipeline — from resume parsing to ranked shortlists.</p>
          </div>

          <div className="feat-grid" style={{ display: 'grid', gridTemplateColumns: 'repeat(3,1fr)', gap: '16px' }}>
            {[
              { icon: <Brain size={22} color="#3b6fff" strokeWidth={1.8} />, bg: '#3b6fff', title: 'NLP Skill Extraction', desc: 'spaCy automatically pulls 500+ skills from any resume — programming languages, frameworks, databases, soft skills and more.' },
              { icon: <GitMerge size={22} color="#7c5cfc" strokeWidth={1.8} />, bg: '#7c5cfc', title: 'BERT + TF-IDF Matching', desc: 'BERT semantic embeddings + TF-IDF cosine similarity produce a hybrid match score with 65% verdict accuracy on tested data.' },
              { icon: <Zap size={22} color="#f59e0b" strokeWidth={1.8} />, bg: '#f59e0b', title: 'Bulk Processing', desc: 'Upload 100 resumes at once. Match all candidates against any JD and get ranked results in under 2 minutes.' },
              { icon: <Award size={22} color="#10b981" strokeWidth={1.8} />, bg: '#10b981', title: 'Smart Verdicts', desc: 'Every match gets a clear verdict: Highly Recommended, Recommended, Consider, or Not Recommended.' },
              { icon: <Search size={22} color="#06b6d4" strokeWidth={1.8} />, bg: '#06b6d4', title: 'Skill Gap Analysis', desc: 'See exactly which required skills a candidate is missing so you make faster, more informed hiring decisions.' },
              { icon: <BarChart3 size={22} color="#ec4899" strokeWidth={1.8} />, bg: '#ec4899', title: 'Analytics Dashboard', desc: 'Recharts dashboard showing match distributions, top candidates, verdict breakdowns, and hiring trends.' },
            ].map((f, i) => (
              <div key={i} className="feature-card">
                <div style={{ width: '46px', height: '46px', borderRadius: '12px', background: f.bg + '15', border: '1px solid ' + f.bg + '25', display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '18px' }}>{f.icon}</div>
                <h3 style={{ fontFamily: 'Plus Jakarta Sans', fontWeight: 700, fontSize: '16px', marginBottom: '10px', color: '#e2e5f0', letterSpacing: '-0.2px' }}>{f.title}</h3>
                <p style={{ fontSize: '13.5px', color: '#3c4560', lineHeight: 1.75 }}>{f.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* HOW IT WORKS */}
      <section id="how-it-works" style={{ padding: '110px 40px' }}>
        <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
          <div style={{ textAlign: 'center', marginBottom: '64px' }}>
            <div style={{ display: 'inline-flex', alignItems: 'center', gap: '6px', background: '#3b6fff10', border: '1px solid #3b6fff25', borderRadius: '50px', padding: '5px 14px', marginBottom: '18px' }}>
              <Cpu size={12} color="#6b8fff" strokeWidth={2.5} />
              <span style={{ fontSize: '12px', fontWeight: 700, color: '#6b8fff', letterSpacing: '0.5px' }}>HOW IT WORKS</span>
            </div>
            <h2 style={{ fontFamily: "'Instrument Serif', serif", fontWeight: 400, fontSize: 'clamp(32px, 4vw, 54px)', letterSpacing: '-0.5px', color: '#f0f2ff', lineHeight: 1.1 }}>
              From upload to shortlist<br />
              <span style={{ fontStyle: 'italic', color: '#3b6fff' }}>in three steps</span>
            </h2>
          </div>

          <div className="steps-grid" style={{ display: 'grid', gridTemplateColumns: 'repeat(3,1fr)', gap: '20px' }}>
            {[
              { icon: <Upload size={24} color="#3b6fff" strokeWidth={1.8} />, bg: '#3b6fff', n: '01', title: 'Upload Resumes', desc: 'Drag and drop PDF resumes. pdfplumber extracts all text, then spaCy NLP identifies every skill automatically.' },
              { icon: <Briefcase size={24} color="#7c5cfc" strokeWidth={1.8} />, bg: '#7c5cfc', n: '02', title: 'Add Job Description', desc: 'Paste your JD directly. Define the role, required skills, and experience level. Supports any industry or stack.' },
              { icon: <TrendingUp size={24} color="#10b981" strokeWidth={1.8} />, bg: '#10b981', n: '03', title: 'Get Ranked Results', desc: 'BERT + TF-IDF hybrid AI scores every resume. Export results as CSV/PDF or email shortlisted candidates directly.' },
            ].map((s, i) => (
              <div key={i} style={{ background: '#0b0d1a', border: '1px solid #161929', borderRadius: '18px', padding: '32px 28px', position: 'relative', overflow: 'hidden', transition: 'all 0.25s' }}
                onMouseEnter={e => { e.currentTarget.style.borderColor = s.bg + '40'; e.currentTarget.style.transform = 'translateY(-4px)' }}
                onMouseLeave={e => { e.currentTarget.style.borderColor = '#161929'; e.currentTarget.style.transform = 'translateY(0)' }}>
                <div className="step-num">{s.n}</div>
                <div style={{ width: '52px', height: '52px', borderRadius: '14px', background: s.bg + '15', border: '1px solid ' + s.bg + '25', display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '20px' }}>{s.icon}</div>
                <div style={{ fontSize: '11px', fontWeight: 700, color: '#3c4560', letterSpacing: '1.5px', marginBottom: '10px' }}>STEP {s.n}</div>
                <h3 style={{ fontFamily: 'Plus Jakarta Sans', fontWeight: 700, fontSize: '18px', color: '#e2e5f0', marginBottom: '12px', letterSpacing: '-0.3px' }}>{s.title}</h3>
                <p style={{ fontSize: '14px', color: '#3c4560', lineHeight: 1.75 }}>{s.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ABOUT */}
      <section id="about" style={{ padding: '110px 40px', position: 'relative', overflow: 'hidden' }}>
        <div className="glow" style={{ width: '500px', height: '500px', background: '#3b6fff', opacity: 0.04, bottom: '-100px', left: '-100px' }} />
        <div style={{ maxWidth: '1200px', margin: '0 auto', display: 'flex', gap: '80px', alignItems: 'center', flexWrap: 'wrap', position: 'relative', zIndex: 1 }}>
          <div style={{ flex: '1 1 340px' }}>
            <div style={{ display: 'inline-flex', alignItems: 'center', gap: '6px', background: '#3b6fff10', border: '1px solid #3b6fff25', borderRadius: '50px', padding: '5px 14px', marginBottom: '20px' }}>
              <Shield size={12} color="#6b8fff" strokeWidth={2.5} />
              <span style={{ fontSize: '12px', fontWeight: 700, color: '#6b8fff', letterSpacing: '0.5px' }}>ABOUT THE PROJECT</span>
            </div>
            <h2 style={{ fontFamily: "'Instrument Serif', serif", fontWeight: 400, fontSize: 'clamp(28px, 3.5vw, 46px)', letterSpacing: '-0.5px', lineHeight: 1.15, marginBottom: '20px', color: '#f0f2ff' }}>
              Real AI solving<br />
              <span style={{ fontStyle: 'italic', color: '#3b6fff' }}>a real problem</span>
            </h2>
            <p style={{ fontSize: '15px', color: '#3c4560', lineHeight: 1.8, marginBottom: '14px' }}>
              RecruitAI is a final-year BCS project using production-grade technologies — FastAPI, PostgreSQL, spaCy NLP, and React — to automate the most time-consuming part of hiring.
            </p>
            <p style={{ fontSize: '15px', color: '#3c4560', lineHeight: 1.8 }}>
              Traditional resume screening takes 23 hours per hire on average. RecruitAI cuts that to minutes using BERT + TF-IDF hybrid scoring, achieving 65% verdict accuracy on 20 tested resume-JD pairs.
            </p>
          </div>
          <div style={{ flex: '1 1 300px', display: 'flex', flexWrap: 'wrap', gap: '10px' }}>
            {[
              { icon: <Cpu size={15} color="#3b6fff" strokeWidth={2} />, label: 'FastAPI' },
              { icon: <Shield size={15} color="#10b981" strokeWidth={2} />, label: 'PostgreSQL' },
              { icon: <Brain size={15} color="#7c5cfc" strokeWidth={2} />, label: 'spaCy NLP' },
              { icon: <GitMerge size={15} color="#f59e0b" strokeWidth={2} />, label: 'TF-IDF' },
              { icon: <Target size={15} color="#06b6d4" strokeWidth={2} />, label: 'Cosine Similarity' },
              { icon: <BarChart3 size={15} color="#ec4899" strokeWidth={2} />, label: 'Recharts' },
              { icon: <Zap size={15} color="#f59e0b" strokeWidth={2} />, label: 'React + Vite' },
              { icon: <Shield size={15} color="#10b981" strokeWidth={2} />, label: 'JWT Auth' },
              { icon: <Users size={15} color="#3b6fff" strokeWidth={2} />, label: 'bcrypt' },
              { icon: <FileText size={15} color="#a78bfa" strokeWidth={2} />, label: 'pdfplumber' },
            ].map((t, i) => (
              <div key={i} className="tech-pill">{t.icon}<span>{t.label}</span></div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section style={{ padding: '80px 40px 100px' }}>
        <div style={{ maxWidth: '760px', margin: '0 auto' }}>
          <div style={{ background: 'linear-gradient(135deg, #3b6fff0d, #7c5cfc0d)', border: '1px solid #3b6fff22', borderRadius: '28px', padding: '72px 56px', textAlign: 'center', position: 'relative', overflow: 'hidden' }}>
            <div className="glow" style={{ width: '400px', height: '300px', background: '#3b6fff', opacity: 0.08, top: '-100px', left: '50%', transform: 'translateX(-50%)' }} />
            <div style={{ position: 'relative', zIndex: 1 }}>
              <h2 style={{ fontFamily: "'Instrument Serif', serif", fontWeight: 400, fontSize: 'clamp(28px, 4vw, 50px)', letterSpacing: '-0.5px', marginBottom: '16px', color: '#f0f2ff', lineHeight: 1.15 }}>
                Ready to screen<br />
                <span style={{ fontStyle: 'italic', color: '#3b6fff' }}>smarter?</span>
              </h2>
              <p style={{ fontSize: '16px', color: '#3c4560', marginBottom: '36px', lineHeight: 1.7 }}>No credit card required. Free for students and small teams.</p>
              <div style={{ display: 'flex', gap: '12px', justifyContent: 'center', flexWrap: 'wrap' }}>
                <button className="btn-main" style={{ fontSize: '15px', padding: '15px 32px' }} onClick={() => navigate('/register')}>
                  Create free account <ArrowRight size={15} />
                </button>
                <button className="btn-ghost" style={{ fontSize: '15px' }} onClick={() => navigate('/login')}>
                  Sign in <ChevronRight size={15} />
                </button>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* FOOTER */}
<footer style={{ borderTop: '1px solid #161929', padding: '28px 40px', display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '12px' }}>
  <div style={{ display: 'flex', alignItems: 'center', gap: '9px' }}>
    <div style={{ width: '28px', height: '28px', borderRadius: '7px', background: 'linear-gradient(135deg, #3b6fff, #7c5cfc)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      <Cpu size={14} color="#fff" strokeWidth={2} />
    </div>
    <span style={{ fontFamily: 'Plus Jakarta Sans', fontWeight: 800, fontSize: '14px', letterSpacing: '-0.3px' }}>RecruitAI</span>
  </div>

  <span style={{ fontSize: '12px', color: '#2a2f45' }}>Final Year BCS Project · 2026</span>

  <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
    <a href="https://github.com/Sadiya-Shaikh" target="_blank" rel="noreferrer"
      style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '13px', color: '#3c4560', textDecoration: 'none', transition: 'color 0.15s' }}
      onMouseEnter={e => e.currentTarget.style.color = '#e2e5f0'}
      onMouseLeave={e => e.currentTarget.style.color = '#3c4560'}>
      <Github size={15} strokeWidth={2} />
      GitHub
    </a>
    <a href="mailto:sadiya.shaikh755n@gmail.com"
      style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '13px', color: '#3c4560', textDecoration: 'none', transition: 'color 0.15s' }}
      onMouseEnter={e => e.currentTarget.style.color = '#e2e5f0'}
      onMouseLeave={e => e.currentTarget.style.color = '#3c4560'}>
      <Mail size={15} strokeWidth={2} />
      Contact
    </a>
  </div>
</footer>
</div>
)
}