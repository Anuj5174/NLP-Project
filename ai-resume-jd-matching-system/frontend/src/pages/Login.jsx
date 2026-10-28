import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import {
  Brain, Zap, Target, Search, Cpu,
  Mail, Lock, ArrowRight, Eye, EyeOff, Shield
} from 'lucide-react'

const features = [
  {
    icon: <Brain size={18} color="#3b6fff" strokeWidth={2} />,
    bg: '#3b6fff',
    title: 'AI-Powered Matching',
    desc: 'TF-IDF + spaCy NLP extracts 500+ skills automatically'
  },
  {
    icon: <Zap size={18} color="#f59e0b" strokeWidth={2} />,
    bg: '#f59e0b',
    title: '95% Time Savings',
    desc: 'Screen 100 resumes in 2 minutes instead of 20 hours'
  },
  {
    icon: <Target size={18} color="#10b981" strokeWidth={2} />,
    bg: '#10b981',
    title: 'Objective Scoring',
    desc: 'Eliminate bias with data-driven match scores 0–100%'
  },
  {
    icon: <Search size={18} color="#a78bfa" strokeWidth={2} />,
    bg: '#a78bfa',
    title: 'Skill Gap Analysis',
    desc: 'See exactly what skills candidates are missing'
  },
]

export default function Login() {
  const navigate = useNavigate()
  const { login } = useAuth()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [showPass, setShowPass] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [focused, setFocused] = useState('')

const handleSubmit = async () => {
  setError('')
  setLoading(true)
  try {
    const formData = new FormData()
    formData.append('username', email)      // ← uses email, not form.email
    formData.append('password', password)   // ← uses password, not form.password

    const response = await fetch('http://localhost:8000/api/v1/auth/login', {
      method: 'POST',
      body: formData
    })

    if (!response.ok) throw new Error('Invalid credentials')

    const data = await response.json()
    login(data.access_token, data.user || { email })
    navigate('/dashboard')

  } catch {
    setError('Invalid email or password. Please try again.')
  } finally {
    setLoading(false)
  }
}
  const handleKey = (e) => { if (e.key === 'Enter') handleSubmit() }

  return (
    <div style={{ display: 'flex', minHeight: '100vh', fontFamily: "'Plus Jakarta Sans', sans-serif", background: '#060810', overflow: 'hidden' }}>
      <style>{`

        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

        @keyframes fadeUp {
          from { opacity: 0; transform: translateY(20px); }
          to   { opacity: 1; transform: translateY(0); }
        }
        @keyframes fadeIn {
          from { opacity: 0; } to { opacity: 1; }
        }
        @keyframes float {
          0%,100% { transform: translateY(0px) rotate(0deg); }
          33%      { transform: translateY(-14px) rotate(1deg); }
          66%      { transform: translateY(-7px) rotate(-1deg); }
        }
        @keyframes orb-drift {
          0%,100% { transform: translate(0,0) scale(1); }
          50%      { transform: translate(30px, -20px) scale(1.08); }
        }
        @keyframes shimmer-line {
          0%   { transform: translateX(-100%); }
          100% { transform: translateX(100%); }
        }
        @keyframes ping {
          0%,100% { opacity: 1; transform: scale(1); }
          50%      { opacity: 0.5; transform: scale(1.3); }
        }
        @keyframes spin {
          from { transform: rotate(0deg); } to { transform: rotate(360deg); }
        }
        @keyframes slide-in-right {
          from { opacity: 0; transform: translateX(40px); }
          to   { opacity: 1; transform: translateX(0); }
        }

        .left-panel { animation: fadeIn 0.8s ease both; }
        .feat-item { animation: fadeUp 0.5s ease both; }
        .feat-item:nth-child(1) { animation-delay: 0.2s; }
        .feat-item:nth-child(2) { animation-delay: 0.32s; }
        .feat-item:nth-child(3) { animation-delay: 0.44s; }
        .feat-item:nth-child(4) { animation-delay: 0.56s; }

        .right-panel { animation: slide-in-right 0.7s cubic-bezier(0.22,1,0.36,1) 0.1s both; }

        .input-wrap { position: relative; }
        .inp {
          width: 100%; padding: 13px 16px 13px 44px;
          background: #0e1120; border: 1.5px solid #1c2035;
          border-radius: 10px; color: #e2e5f0;
          font-size: 14px; font-family: 'Plus Jakarta Sans', sans-serif;
          outline: none; transition: border-color 0.2s, box-shadow 0.2s;
        }
        .inp::placeholder { color: #3c4560; }
        .inp:focus { border-color: #3b6fff; box-shadow: 0 0 0 3px #3b6fff18; }

        .inp-icon {
          position: absolute; left: 14px; top: 50%;
          transform: translateY(-50%); pointer-events: none;
        }
        .inp-icon-right {
          position: absolute; right: 14px; top: 50%;
          transform: translateY(-50%); cursor: pointer;
          color: #3c4560; transition: color 0.15s;
          background: none; border: none; display: flex; align-items: center;
        }
        .inp-icon-right:hover { color: #e2e5f0; }

        .btn-submit {
          width: 100%; padding: 14px;
          background: #3b6fff; color: #fff; border: none;
          border-radius: 10px; font-size: 15px; font-weight: 700;
          cursor: pointer; font-family: 'Plus Jakarta Sans', sans-serif;
          display: flex; align-items: center; justify-content: center; gap: 8px;
          transition: all 0.2s;
          box-shadow: 0 4px 20px #3b6fff35;
          position: relative; overflow: hidden;
        }
        .btn-submit::after {
          content: '';
          position: absolute; inset: 0;
          background: linear-gradient(90deg, transparent, #ffffff18, transparent);
          transform: translateX(-100%);
        }
        .btn-submit:hover::after { animation: shimmer-line 0.6s ease forwards; }
        .btn-submit:hover:not(:disabled) {
          background: #4d7bff;
          box-shadow: 0 8px 32px #3b6fff50;
          transform: translateY(-1px);
        }
        .btn-submit:disabled { opacity: 0.6; cursor: not-allowed; transform: none; }

        .feat-card {
          display: flex; align-items: flex-start; gap: 14px;
          padding: 16px 18px; border-radius: 14px;
          background: rgba(255,255,255,0.03);
          border: 1px solid rgba(255,255,255,0.06);
          transition: all 0.25s; cursor: default;
        }
        .feat-card:hover {
          background: rgba(59,111,255,0.06);
          border-color: rgba(59,111,255,0.2);
          transform: translateX(4px);
        }

        .star-field {
          position: absolute; inset: 0; overflow: hidden; pointer-events: none;
        }
        .star {
          position: absolute; border-radius: 50%;
          background: #fff; animation: ping 3s ease-in-out infinite;
        }

        .glow-orb {
          position: absolute; border-radius: 50%;
          filter: blur(80px); pointer-events: none;
          animation: orb-drift 8s ease-in-out infinite;
        }

        .register-link {
          color: #3b6fff; font-weight: 700; text-decoration: none;
          transition: color 0.15s;
        }
        .register-link:hover { color: #6b8fff; }

        .error-box {
          display: flex; align-items: center; gap: 10px;
          padding: 12px 16px; background: #ef444412;
          border: 1px solid #ef444428; border-radius: 10px;
          animation: fadeUp 0.3s ease;
        }

        .spinner {
          width: 18px; height: 18px; border: 2.5px solid #ffffff30;
          border-top-color: #fff; border-radius: 50%;
          animation: spin 0.7s linear infinite;
        }
      `}</style>

      {/* ── LEFT PANEL ── */}
      <div className="left-panel auth-left-panel" style={{
        flex: '0 0 52%', position: 'relative', overflow: 'hidden',
        background: 'linear-gradient(135deg, #060810 0%, #090c1a 60%, #0a0c1e 100%)',
        borderRight: '1px solid #161929',
        display: 'flex', flexDirection: 'column', justifyContent: 'center',
        padding: '60px 64px'
      }}>
        {/* Glowing orbs */}
        <div className="glow-orb" style={{ width: '500px', height: '500px', background: '#3b6fff', opacity: 0.07, top: '-150px', left: '-150px' }} />
        <div className="glow-orb" style={{ width: '350px', height: '350px', background: '#7c5cfc', opacity: 0.08, bottom: '-80px', right: '-80px', animationDelay: '4s' }} />
        <div className="glow-orb" style={{ width: '200px', height: '200px', background: '#06b6d4', opacity: 0.05, top: '40%', right: '10%', animationDelay: '2s' }} />

        {/* Star field */}
        <div className="star-field">
          {[...Array(28)].map((_, i) => (
            <div key={i} className="star" style={{
              width: `${Math.random() * 2 + 1}px`,
              height: `${Math.random() * 2 + 1}px`,
              top: `${Math.random() * 100}%`,
              left: `${Math.random() * 100}%`,
              animationDelay: `${Math.random() * 4}s`,
              animationDuration: `${2 + Math.random() * 3}s`,
              opacity: Math.random() * 0.5 + 0.1
            }} />
          ))}
        </div>

        {/* Subtle grid */}
        <div style={{
          position: 'absolute', inset: 0,
          backgroundImage: 'linear-gradient(#1c2035 1px, transparent 1px), linear-gradient(90deg, #1c2035 1px, transparent 1px)',
          backgroundSize: '50px 50px', opacity: 0.18,
          maskImage: 'radial-gradient(ellipse 70% 80% at 30% 50%, black 10%, transparent 100%)',
          WebkitMaskImage: 'radial-gradient(ellipse 70% 80% at 30% 50%, black 10%, transparent 100%)',
          pointerEvents: 'none'
        }} />

        {/* Content */}
        <div style={{ position: 'relative', zIndex: 1, maxWidth: '440px' }}>
          {/* Logo */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '52px' }}>
            <div style={{ width: '38px', height: '38px', borderRadius: '10px', background: 'linear-gradient(135deg, #3b6fff, #7c5cfc)', display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: '0 4px 20px #3b6fff40' }}>
              <Cpu size={19} color="#fff" strokeWidth={2} />
            </div>
            <div>
              <div style={{ fontFamily: 'Plus Jakarta Sans', fontWeight: 800, fontSize: '17px', letterSpacing: '-0.4px', color: '#f0f2ff' }}>RecruitAI</div>
              <div style={{ fontSize: '10px', color: '#3c4560', letterSpacing: '1.2px', fontWeight: 600 }}>SMART HIRING</div>
            </div>
          </div>

          {/* Headline */}
          <h1 style={{
            fontFamily: "'Instrument Serif', serif",
            fontWeight: 400, fontSize: 'clamp(34px, 3.5vw, 52px)',
            lineHeight: 1.1, letterSpacing: '-0.5px',
            marginBottom: '16px', color: '#f0f2ff'
          }}>
            Hire smarter with{' '}
            <span style={{ fontStyle: 'italic', color: '#3b6fff' }}>
              Artificial Intelligence
            </span>
          </h1>

          <p style={{ fontSize: '15px', color: '#3c4560', lineHeight: 1.7, marginBottom: '44px', fontWeight: 400 }}>
            AI-powered resume screening that saves 95% of your time and eliminates hiring bias completely.
          </p>

          {/* Feature list */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            {features.map((f, i) => (
              <div key={i} className="feat-item feat-card">
                <div style={{
                  width: '38px', height: '38px', borderRadius: '10px', flexShrink: 0,
                  background: f.bg + '15', border: '1px solid ' + f.bg + '25',
                  display: 'flex', alignItems: 'center', justifyContent: 'center'
                }}>{f.icon}</div>
                <div>
                  <div style={{ fontFamily: 'Plus Jakarta Sans', fontWeight: 700, fontSize: '14px', color: '#e2e5f0', marginBottom: '3px' }}>{f.title}</div>
                  <div style={{ fontSize: '12.5px', color: '#3c4560', lineHeight: 1.5 }}>{f.desc}</div>
                </div>
              </div>
            ))}
          </div>

          {/* Bottom stats */}
          <div style={{ display: 'flex', gap: '32px', marginTop: '40px', paddingTop: '32px', borderTop: '1px solid #161929' }}>
            {[['95%', 'Time saved'], ['500+', 'Skills tracked'], ['90%+', 'Accuracy']].map(([val, label]) => (
              <div key={label}>
                <div style={{ fontFamily: 'Plus Jakarta Sans', fontWeight: 800, fontSize: '22px', letterSpacing: '-0.5px', color: '#3b6fff' }}>{val}</div>
                <div style={{ fontSize: '11px', color: '#3c4560', marginTop: '2px', fontWeight: 500 }}>{label}</div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* ── RIGHT PANEL ── */}
      <div className="right-panel auth-right-panel" style={{
        flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center',
        padding: '48px 40px', background: '#07090f', position: 'relative', overflow: 'hidden'
      }}>
        {/* Subtle glow behind form */}
        <div style={{ position: 'absolute', width: '400px', height: '400px', borderRadius: '50%', background: '#3b6fff', opacity: 0.04, filter: 'blur(80px)', top: '50%', left: '50%', transform: 'translate(-50%,-50%)', pointerEvents: 'none' }} />

        <div style={{ width: '100%', maxWidth: '400px', position: 'relative', zIndex: 1 }}>

          {/* Header */}
          <div style={{ marginBottom: '36px' }}>
            <h2 style={{
              fontFamily: "'Instrument Serif', serif",
              fontWeight: 400, fontSize: '36px',
              letterSpacing: '-0.5px', color: '#f0f2ff',
              lineHeight: 1.15, marginBottom: '8px'
            }}>Welcome back</h2>
            <p style={{ fontSize: '14px', color: '#3c4560', fontWeight: 400 }}>
              Sign in to your RecruitAI account
            </p>
          </div>

          {/* Error */}
          {error && (
            <div className="error-box" style={{ marginBottom: '20px' }}>
              <Shield size={14} color="#f87171" strokeWidth={2} />
              <span style={{ fontSize: '13px', color: '#f87171', fontWeight: 500 }}>{error}</span>
            </div>
          )}

          {/* Email */}
          <div style={{ marginBottom: '16px' }}>
            <label style={{ display: 'block', fontSize: '13px', fontWeight: 600, color: '#5a6380', marginBottom: '8px', letterSpacing: '0.2px' }}>
              Email Address
            </label>
            <div className="input-wrap">
              <Mail size={15} color={focused === 'email' ? '#3b6fff' : '#3c4560'} strokeWidth={2} className="inp-icon" />
              <input className="inp glow-border" type="email" placeholder="you@example.com"
                value={email} onChange={e => setEmail(e.target.value)}
                onFocus={() => setFocused('email')} onBlur={() => setFocused('')}
                onKeyDown={handleKey} />
            </div>
          </div>

          {/* Password */}
          <div style={{ marginBottom: '28px' }}>
            <label style={{ display: 'block', fontSize: '13px', fontWeight: 600, color: '#5a6380', marginBottom: '8px', letterSpacing: '0.2px' }}>
              Password
            </label>
            <div className="input-wrap">
              <Lock size={15} color={focused === 'password' ? '#3b6fff' : '#3c4560'} strokeWidth={2} className="inp-icon" />
              <input className="inp glow-border" type={showPass ? 'text' : 'password'} placeholder="Enter your password"
                value={password} onChange={e => setPassword(e.target.value)}
                onFocus={() => setFocused('password')} onBlur={() => setFocused('')}
                onKeyDown={handleKey} style={{ paddingRight: '44px' }} />
              <button className="inp-icon-right" onClick={() => setShowPass(!showPass)}>
                {showPass ? <EyeOff size={15} strokeWidth={2} /> : <Eye size={15} strokeWidth={2} />}
              </button>
            </div>
          </div>

          {/* Submit */}
          <button className="btn-submit" onClick={handleSubmit} disabled={loading || !email || !password}>
            {loading
              ? <><div className="spinner" /> Signing in...</>
              : <>Sign In to Dashboard <ArrowRight size={16} strokeWidth={2.5} /></>
            }
          </button>

          {/* Register */}
          <div style={{
            marginTop: '20px', padding: '16px',
            background: '#0e1120', border: '1px solid #161929',
            borderRadius: '10px', textAlign: 'center'
          }}>
            <span style={{ fontSize: '13.5px', color: '#3c4560' }}>
              Don't have an account?{' '}
              <Link to="/register" className="register-link">
                Create free account →
              </Link>
            </span>
          </div>

          {/* Security note */}
          <div style={{ textAlign: 'center', marginTop: '20px', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '6px' }}>
            <Shield size={12} color="#2a2f45" strokeWidth={2} />
            <span style={{ fontSize: '12px', color: '#2a2f45' }}>Secure login · Your data is encrypted</span>
          </div>
        </div>
      </div>
    </div>
  )
}