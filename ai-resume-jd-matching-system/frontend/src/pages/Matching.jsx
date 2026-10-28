import { useState, useEffect, useRef } from 'react'
import api from '../api/axios'
import { Target, Zap, CheckCircle, XCircle, TrendingUp, Brain, BarChart3, Users, ChevronDown, Mail } from 'lucide-react'
import EmailShortlistModal from '../components/EmailShortlistModal'
import ExportButtons from '../components/ExportButtons'

// ── FIX 1: Score Circle with working fill animation ──────────────────────────
const ScoreCircle = ({ score }) => {
  const color = score >= 75 ? '#10b981' : score >= 60 ? '#4f8eff' : score >= 50 ? '#f59e0b' : '#ef4444'
  const size = 130
  const radius = 54
  const circumference = 2 * Math.PI * radius
  const offset = circumference - (score / 100) * circumference
  const circleRef = useRef(null)

  useEffect(() => {
    if (circleRef.current) {
      circleRef.current.style.strokeDashoffset = circumference
      setTimeout(() => {
        if (circleRef.current) {
          circleRef.current.style.strokeDashoffset = offset
        }
      }, 100)
    }
  }, [score, offset, circumference])

  return (
    <div style={{ textAlign: 'center', marginBottom: '20px' }}>
      <svg width={size} height={size} style={{ transform: 'rotate(-90deg)' }}>
        <circle cx={size/2} cy={size/2} r={radius} fill="none" stroke="#ffffff08" strokeWidth="10" />
        <circle
          ref={circleRef}
          cx={size/2} cy={size/2} r={radius}
          fill="none" stroke={color}
          strokeWidth="10" strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={circumference}
          style={{ transition: 'stroke-dashoffset 1.5s cubic-bezier(0.4,0,0.2,1)' }}
        />
      </svg>
      <div style={{ marginTop: '-90px', marginBottom: '20px' }}>
        <div style={{ fontSize: '32px', fontFamily: 'Syne', fontWeight: 800, color, letterSpacing: '-1px' }}>{score}%</div>
        <div style={{ fontSize: '12px', color: 'var(--text-secondary)', marginTop: '2px' }}>Match Score</div>
      </div>
    </div>
  )
}

const MetricCard = ({ icon: Icon, label, value, color }) => (
  <div style={{ background: '#ffffff05', border: '1px solid var(--border)', borderRadius: '12px', padding: '14px', textAlign: 'center' }}>
    <div style={{ width: '32px', height: '32px', borderRadius: '8px', background: `${color}15`, display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 8px' }}>
      <Icon size={15} color={color} />
    </div>
    <div style={{ fontSize: '20px', fontWeight: 800, fontFamily: 'Syne', color, letterSpacing: '-0.5px' }}>{value}%</div>
    <div style={{ fontSize: '11px', color: 'var(--text-secondary)', marginTop: '3px', lineHeight: 1.3 }}>{label}</div>
  </div>
)

// ── FIX 4: Skeleton loader ────────────────────────────────────────────────────
const SkeletonCard = () => (
  <div className="card" style={{ flex: 1, minWidth: '300px' }}>
    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '20px', alignItems: 'center' }}>
      <div style={{ width: '100px', height: '20px', background: '#ffffff10', borderRadius: '6px', animation: 'pulse 1.5s infinite' }} />
      <div style={{ width: '140px', height: '30px', background: '#ffffff10', borderRadius: '20px', animation: 'pulse 1.5s infinite' }} />
    </div>
    <div style={{ width: '130px', height: '130px', borderRadius: '50%', background: '#ffffff10', margin: '0 auto 20px', animation: 'pulse 1.5s infinite' }} />
    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '10px', marginBottom: '20px' }}>
      {[1,2,3].map(i => (
        <div key={i} style={{ height: '80px', background: '#ffffff08', borderRadius: '12px', animation: 'pulse 1.5s infinite' }} />
      ))}
    </div>
    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '14px', marginBottom: '16px' }}>
      <div style={{ height: '100px', background: '#ffffff08', borderRadius: '12px', animation: 'pulse 1.5s infinite' }} />
      <div style={{ height: '100px', background: '#ffffff08', borderRadius: '12px', animation: 'pulse 1.5s infinite' }} />
    </div>
    <div style={{ height: '80px', background: '#ffffff08', borderRadius: '12px', animation: 'pulse 1.5s infinite' }} />
  </div>
)

export default function Matching() {
  const [resumes, setResumes] = useState([])
  const [jds, setJds] = useState([])
  const [selectedResume, setSelectedResume] = useState('')
  const [selectedJd, setSelectedJd] = useState('')
  const [result, setResult] = useState(null)
  const [bulkResults, setBulkResults] = useState(null)
  const [loading, setLoading] = useState(false)
  const [mode, setMode] = useState('single')
  const [selectedMatchIds, setSelectedMatchIds] = useState([])
  const [showEmailModal, setShowEmailModal] = useState(false)
  const [showSingleEmailModal, setShowSingleEmailModal] = useState(false)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [resumesRes, jdsRes] = await Promise.all([
          api.get('/resumes/'),
          api.get('/jds/')
        ])
        setResumes(resumesRes.data.resumes || [])
        setJds(jdsRes.data || [])
      } catch (err) { console.error(err) }
    }
    fetchData()
  }, [])

  const handleSingleMatch = async () => {
    if (!selectedResume || !selectedJd) return alert('Select both resume and job description')
    setLoading(true); setResult(null)
    try {
      const res = await api.post(`/match/single?resume_id=${selectedResume}&jd_id=${selectedJd}`)
      setResult(res.data)
    } catch (err) {
      alert('Matching failed: ' + (err.response?.data?.detail || err.message))
    } finally { setLoading(false) }
  }

  const handleBulkMatch = async () => {
    if (!selectedJd) return alert('Select a job description')
    setLoading(true); setBulkResults(null); setSelectedMatchIds([])
    try {
      const res = await api.post(`/match/bulk?jd_id=${selectedJd}`)
      setBulkResults(res.data)
    } catch (err) {
      alert('Bulk matching failed: ' + (err.response?.data?.detail || err.message))
    } finally { setLoading(false) }
  }

  const verdictColor = (v) => {
    if (v === 'Highly Recommended') return '#10b981'
    if (v === 'Recommended') return '#4f8eff'
    if (v === 'Consider') return '#f59e0b'
    return '#ef4444'
  }

  const verdictIcon = (v) => {
    if (v === 'Highly Recommended') return <CheckCircle size={14} />
    if (v === 'Recommended') return <TrendingUp size={14} />
    if (v === 'Consider') return <BarChart3 size={14} />
    return <XCircle size={14} />
  }

  const selectStyle = {
    width: '100%', padding: '11px 14px', borderRadius: '10px',
    background: '#ffffff08', border: '1px solid var(--border)',
    color: 'var(--text-primary)', fontSize: '14px', outline: 'none',
    fontFamily: 'DM Sans, sans-serif', cursor: 'pointer', appearance: 'none'
  }

  return (
    <div className="fade-up">
      {/* FIX 2: Mobile responsive + all animations */}
      <style>{`
        @keyframes spin { to { transform: rotate(360deg); } }
        @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.4} }
        @media (max-width: 768px) {
          .matching-grid { flex-direction: column !important; }
          .matching-grid > div { width: 100% !important; min-width: unset !important; flex-shrink: 1 !important; }
          .metric-grid { grid-template-columns: 1fr 1fr !important; }
          .skills-grid { grid-template-columns: 1fr !important; }
        }
      `}</style>

      {/* Header */}
      <div style={{ marginBottom: '32px' }}>
        <h1 style={{ fontSize: '34px', fontWeight: 800, letterSpacing: '-0.5px', marginBottom: '6px' }}>AI Matching</h1>
        <p style={{ color: 'var(--text-secondary)', fontSize: '14px' }}>
          Match resumes against job descriptions using BERT + TF-IDF hybrid scoring
        </p>
      </div>

      {/* Mode Toggle */}
      <div style={{ display: 'flex', gap: '8px', marginBottom: '24px', background: '#ffffff08', padding: '4px', borderRadius: '12px', width: 'fit-content' }}>
        {[
          { id: 'single', icon: Target, label: 'Single Match' },
          { id: 'bulk', icon: Zap, label: 'Bulk Match' }
        ].map(({ id, icon: Icon, label }) => (
          <button key={id} onClick={() => { setMode(id); setResult(null); setBulkResults(null); setSelectedMatchIds([]) }} style={{
            display: 'flex', alignItems: 'center', gap: '8px',
            padding: '9px 20px', borderRadius: '9px', border: 'none', cursor: 'pointer',
            background: mode === id ? 'white' : 'transparent',
            color: mode === id ? '#0a0a0f' : 'var(--text-secondary)',
            fontWeight: mode === id ? 700 : 500, fontSize: '14px',
            fontFamily: 'DM Sans, sans-serif', transition: 'all 0.2s',
            boxShadow: mode === id ? '0 2px 8px #00000030' : 'none'
          }}>
            <Icon size={15} />{label}
          </button>
        ))}
      </div>

      {/* FIX 2: Added matching-grid className */}
      <div className="matching-grid" style={{ display: 'flex', gap: '20px', flexWrap: 'wrap', alignItems: 'flex-start' }}>

        {/* Controls Panel */}
        <div className="card" style={{ width: '300px', flexShrink: 0 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '24px' }}>
            <div style={{ width: '34px', height: '34px', borderRadius: '10px', background: mode === 'single' ? '#4f8eff20' : '#f59e0b20', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              {mode === 'single' ? <Target size={16} color="#4f8eff" /> : <Zap size={16} color="#f59e0b" />}
            </div>
            <h3 style={{ fontSize: '15px', fontWeight: 700 }}>
              {mode === 'single' ? 'Single Resume Match' : 'Bulk Match All Resumes'}
            </h3>
          </div>

          {mode === 'single' && (
            <div style={{ marginBottom: '16px', position: 'relative' }}>
              <label style={{ fontSize: '11px', color: 'var(--text-secondary)', fontWeight: 700, letterSpacing: '0.8px', marginBottom: '8px', display: 'block' }}>SELECT RESUME</label>
              <select style={selectStyle} value={selectedResume} onChange={e => setSelectedResume(e.target.value)}>
                <option value="">Choose a resume...</option>
                {resumes.map(r => (
                  <option key={r.resume_id} value={r.resume_id} style={{ background: '#16161f' }}>
                    {r.candidate_name || 'Unknown'} — {r.file_name?.substring(0, 25)}
                  </option>
                ))}
              </select>
              <ChevronDown size={14} color="var(--text-secondary)" style={{ position: 'absolute', right: '12px', top: '62%', pointerEvents: 'none' }} />
            </div>
          )}

          <div style={{ marginBottom: '24px', position: 'relative' }}>
            <label style={{ fontSize: '11px', color: 'var(--text-secondary)', fontWeight: 700, letterSpacing: '0.8px', marginBottom: '8px', display: 'block' }}>SELECT JOB DESCRIPTION</label>
            <select style={selectStyle} value={selectedJd} onChange={e => setSelectedJd(e.target.value)}>
              <option value="">Choose a job...</option>
              {jds.map(j => (
                <option key={j.jd_id} value={j.jd_id} style={{ background: '#16161f' }}>
                  {j.title} — {j.company_name || 'No company'}
                </option>
              ))}
            </select>
            <ChevronDown size={14} color="var(--text-secondary)" style={{ position: 'absolute', right: '12px', top: '62%', pointerEvents: 'none' }} />
          </div>

          <button
            onClick={mode === 'single' ? handleSingleMatch : handleBulkMatch}
            disabled={loading}
            style={{
              width: '100%', padding: '13px', borderRadius: '12px', border: 'none',
              background: loading ? '#333' : mode === 'single'
                ? 'linear-gradient(135deg, #4f8eff, #6366f1)'
                : 'linear-gradient(135deg, #f59e0b, #ef4444)',
              color: 'white', fontSize: '14px', fontWeight: 700, cursor: loading ? 'not-allowed' : 'pointer',
              fontFamily: 'DM Sans, sans-serif', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px',
              boxShadow: loading ? 'none' : '0 4px 20px #4f8eff30', transition: 'all 0.2s'
            }}
          >
            {loading ? (
              <><div style={{ width: '16px', height: '16px', border: '2px solid white', borderTopColor: 'transparent', borderRadius: '50%', animation: 'spin 0.8s linear infinite' }} /> Analyzing...</>
            ) : mode === 'single' ? (
              <><Target size={16} /> Run AI Match</>
            ) : (
              <><Zap size={16} /> Match All {resumes.length} Resumes</>
            )}
          </button>

          {mode === 'bulk' && (
            <div style={{ marginTop: '16px', padding: '12px', background: '#f59e0b08', border: '1px solid #f59e0b20', borderRadius: '10px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '12px', color: '#f59e0b' }}>
                <Users size={13} />
                <span>Will analyze all <strong>{resumes.length}</strong> resumes against selected JD</span>
              </div>
            </div>
          )}

          {/* Algorithm Breakdown */}
          <div style={{ marginTop: '20px', padding: '14px', background: '#ffffff05', borderRadius: '10px', border: '1px solid var(--border)' }}>
            <div style={{ fontSize: '11px', color: 'var(--text-secondary)', fontWeight: 700, letterSpacing: '0.8px', marginBottom: '10px' }}>NLP PIPELINE (5 PAPERS + EDIT DISTANCE)</div>
            {[
              ['Sentence-BERT Embedding', '36%', '#4f8eff'],
              ['TF-IDF Cosine Similarity', '24%', '#6366f1'],
              ['Fuzzy Set Skill Coverage (Paper 5)', '30%', '#8b5cf6'],
              ['BM25F Section Weighting (Paper 4)', 'Active', '#ec4899'],
              ['TextRank Keywords (Paper 2)', 'Active', '#f59e0b'],
              ['PMI Skill Expansion (Paper 3)', 'Active', '#06b6d4'],
              ['Custom Edit Distance DP', 'Typo-Safe', '#10b981'],
            ].map(([label, pct, color]) => (
              <div key={label} style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '6px' }}>
                <span style={{ fontSize: '12px', color: 'var(--text-secondary)' }}>{label}</span>
                <span style={{ fontSize: '12px', color, fontWeight: 700 }}>{pct}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Skeleton while loading */}
        {loading && mode === 'single' && <SkeletonCard />}

        {/* Single Result */}
        {result && mode === 'single' && (
          <div style={{ flex: 1, minWidth: '300px' }}>
            <div className="card scale-in" style={{ border: `1px solid ${verdictColor(result.verdict)}30`, marginBottom: '16px' }}>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '20px', flexWrap: 'wrap', gap: '8px' }}>
                <h3 style={{ fontSize: '15px', fontWeight: 700 }}>Match Result</h3>
                <span className="verdict-pill" style={{
                  display: 'inline-flex', alignItems: 'center', gap: '6px',
                  padding: '6px 14px', borderRadius: '20px', fontSize: '12px', fontWeight: 700,
                  background: `${verdictColor(result.verdict)}15`, color: verdictColor(result.verdict),
                  border: `1px solid ${verdictColor(result.verdict)}30`
                }}>
                  {verdictIcon(result.verdict)}{result.verdict}
                </span>
                <button
                  onClick={() => setShowSingleEmailModal(true)}
                  style={{ display: 'flex', alignItems: 'center', gap: '6px', padding: '7px 14px', background: '#2563eb', color: 'white', borderRadius: '10px', fontSize: '13px', fontWeight: 600, border: 'none', cursor: 'pointer' }}
                >
                  <Mail size={13} /> Email Candidate
                </button>
              </div>

              {/* Animated score circle */}
              <ScoreCircle score={result.match_score} />

              {/* Multi-Metric Grid */}
              <div className="metric-grid" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(130px, 1fr))', gap: '10px', marginBottom: '20px' }}>
                <MetricCard icon={Brain} label="BERT Semantic" value={(result.bert_score ? (result.bert_score * 100).toFixed(1) : (result.cosine_similarity * 100).toFixed(1))} color="#4f8eff" />
                <MetricCard icon={Target} label="BM25F Section Fit" value={(result.bm25f_score || result.bm25_score || 0).toFixed(1)} color="#ec4899" />
                <MetricCard icon={CheckCircle} label="Fuzzy Set Similarity" value={(result.fuzzy_similarity_score || result.skill_match_percentage || 0).toFixed(1)} color="#06b6d4" />
                <MetricCard icon={Target} label="Skill Coverage" value={result.skill_match_percentage?.toFixed(1) || '0'} color="#8b5cf6" />
                <MetricCard icon={BarChart3} label="Keyword Density" value={((result.keyword_density_score || result.keyword_density || 0) * 100).toFixed(1)} color="#10b981" />
              </div>

              {/* TextRank Executive Summary (Paper 2 — Mihalcea & Tarau 2004) */}
              {result.textrank_summary && (
                <div style={{ background: '#1e2235', border: '1px solid #3b6fff35', borderRadius: '12px', padding: '14px', marginBottom: '16px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '12px', fontWeight: 700, color: '#4f8eff', marginBottom: '6px' }}>
                    <Brain size={14} /> TextRank Executive Summary (Paper 2)
                  </div>
                  <p style={{ fontSize: '13px', lineHeight: 1.6, color: '#e2e5f0', margin: 0, fontStyle: 'italic' }}>
                    "{result.textrank_summary}"
                  </p>
                </div>
              )}

              {/* Custom Edit Distance Typo-Tolerant Matches */}
              {result.edit_distance_matches && result.edit_distance_matches.length > 0 && (
                <div style={{ background: '#10b98108', border: '1px solid #10b98130', borderRadius: '12px', padding: '14px', marginBottom: '16px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '12px', fontWeight: 700, color: '#10b981', marginBottom: '8px' }}>
                    <CheckCircle size={14} /> Custom Edit Distance Typo Matches ({result.edit_distance_matches.length})
                  </div>
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
                    {result.edit_distance_matches.map((m, i) => (
                      <span key={i} style={{ padding: '4px 10px', borderRadius: '8px', fontSize: '11px', fontWeight: 600, background: '#10b98115', color: '#10b981', border: '1px solid #10b98125' }}>
                        "{m.resume_skill}" &rarr; <strong>{m.jd_skill}</strong> (Dist: {m.edit_distance}, Sim: {(m.edit_similarity * 100).toFixed(0)}%)
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {/* Skills Grid */}
              <div className="skills-grid" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '14px', marginBottom: '16px' }}>
                <div style={{ background: '#10b98108', border: '1px solid #10b98125', borderRadius: '12px', padding: '14px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '12px', fontWeight: 700, color: '#10b981', marginBottom: '10px' }}>
                    <CheckCircle size={13} /> Matched Skills ({result.matched_skills?.length || 0})
                  </div>
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: '5px' }}>
                    {result.matched_skills?.map((s, i) => (
                      <span key={i} style={{ padding: '3px 9px', borderRadius: '20px', fontSize: '11px', fontWeight: 600, background: '#10b98118', color: '#10b981' }}>{s}</span>
                    ))}
                  </div>
                </div>
                <div style={{ background: '#ef444408', border: '1px solid #ef444425', borderRadius: '12px', padding: '14px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '12px', fontWeight: 700, color: '#ef4444', marginBottom: '10px' }}>
                    <XCircle size={13} /> Missing Skills ({result.missing_skills?.length || 0})
                  </div>
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: '5px' }}>
                    {result.missing_skills?.map((s, i) => (
                      <span key={i} style={{ padding: '3px 9px', borderRadius: '20px', fontSize: '11px', fontWeight: 600, background: '#ef444418', color: '#ef4444' }}>{s}</span>
                    ))}
                  </div>
                </div>
              </div>

              {/* AI Recommendation Box */}
              <div style={{ background: '#4f8eff08', border: '1px solid #4f8eff20', borderRadius: '12px', padding: '14px', marginBottom: '16px' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '12px', fontWeight: 700, color: '#4f8eff', marginBottom: '6px' }}>
                  <Brain size={13} /> AI Recommendation & Feedback
                </div>
                <p style={{ fontSize: '13px', lineHeight: 1.7, color: 'var(--text-primary)', margin: 0 }}>{result.recommendations}</p>
              </div>

              {/* Unsupervised TextRank JD Keywords */}
              {result.textrank_jd_keywords && result.textrank_jd_keywords.length > 0 && (
                <div style={{ background: '#f59e0b08', border: '1px solid #f59e0b20', borderRadius: '12px', padding: '12px' }}>
                  <div style={{ fontSize: '11px', fontWeight: 700, color: '#f59e0b', marginBottom: '6px', letterSpacing: '0.5px' }}>
                    TEXTRANK JD KEYWORDS (PAPER 2 UNSUPERVISED)
                  </div>
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: '4px' }}>
                    {result.textrank_jd_keywords.map((kw, idx) => (
                      <span key={idx} style={{ padding: '2px 8px', borderRadius: '6px', background: '#f59e0b15', color: '#f59e0b', fontSize: '11px' }}>
                        {kw}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Bulk Results */}
        {bulkResults && mode === 'bulk' && (
          <div style={{ flex: 1, minWidth: '300px' }}>
            {bulkResults.results?.length > 0 && (
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px', flexWrap: 'wrap', gap: '10px' }}>
                <span style={{ color: 'var(--text-secondary)', fontSize: '14px' }}>
                  {selectedMatchIds.length > 0
                    ? `${selectedMatchIds.length} candidate(s) selected`
                    : 'Select candidates to email'}
                </span>
                <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
                  <ExportButtons jdId={selectedJd} jdTitle={bulkResults.jd_title} />
                  {selectedMatchIds.length > 0 && (
                    <button
                      onClick={() => setShowEmailModal(true)}
                      style={{ display: 'flex', alignItems: 'center', gap: '8px', padding: '8px 16px', background: '#2563eb', color: 'white', borderRadius: '12px', fontSize: '14px', fontWeight: 500, border: 'none', cursor: 'pointer' }}
                    >
                      <Mail size={14} />
                      Email {selectedMatchIds.length} Shortlisted
                    </button>
                  )}
                </div>
              </div>
            )}

            <div className="card scale-in">
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '8px' }}>
                <h3 style={{ fontSize: '15px', fontWeight: 700 }}>Bulk Results</h3>
                <div style={{ display: 'flex', alignItems: 'center', gap: '6px', padding: '4px 12px', borderRadius: '20px', background: '#10b98115', fontSize: '12px', color: '#10b981', fontWeight: 700 }}>
                  <Users size={12} /> {bulkResults.total_resumes} Analyzed
                </div>
              </div>

              <p style={{ color: 'var(--text-secondary)', fontSize: '13px', marginBottom: '20px' }}>{bulkResults.jd_title} — ranked by match score</p>

              {bulkResults.results?.map((r, i) => (
                <div key={r.match_id} style={{
                  display: 'flex', alignItems: 'center', gap: '16px', padding: '14px',
                  borderRadius: '12px', marginBottom: '8px',
                  background: i === 0 ? '#10b98108' : i === 1 ? '#4f8eff05' : '#ffffff03',
                  border: `1px solid ${i === 0 ? '#10b98125' : i === 1 ? '#4f8eff20' : 'var(--border)'}`
                }}>
                  <input
                    type="checkbox"
                    checked={selectedMatchIds.includes(r.match_id)}
                    onChange={(e) => {
                      if (e.target.checked) {
                        setSelectedMatchIds(prev => [...prev, r.match_id])
                      } else {
                        setSelectedMatchIds(prev => prev.filter(id => id !== r.match_id))
                      }
                    }}
                  />
                  <div style={{
                    width: '32px', height: '32px', borderRadius: '10px', flexShrink: 0,
                    background: i === 0 ? '#10b98120' : i === 1 ? '#f59e0b20' : '#ffffff10',
                    display: 'flex', alignItems: 'center', justifyContent: 'center',
                    fontSize: '14px', fontWeight: 800, fontFamily: 'Syne',
                    color: i === 0 ? '#10b981' : i === 1 ? '#f59e0b' : 'var(--text-secondary)'
                  }}>#{i + 1}</div>
                  <div style={{ flex: 1 }}>
                    <div style={{ fontWeight: 700, fontSize: '14px', marginBottom: '3px' }}>{r.candidate_name || 'Unknown'}</div>
                    <div style={{ fontSize: '11px', color: 'var(--text-secondary)' }}>
                      {r.matched_skills?.slice(0, 4).join(' • ')}
                      {r.matched_skills?.length > 4 ? ` +${r.matched_skills.length - 4}` : ''}
                    </div>
                  </div>
                  <div style={{ textAlign: 'right' }}>
                    <div style={{ fontSize: '22px', fontWeight: 800, fontFamily: 'Syne', color: verdictColor(r.verdict), letterSpacing: '-0.5px' }}>{r.match_score}%</div>
                    <span style={{
                      display: 'inline-flex', alignItems: 'center', gap: '4px',
                      fontSize: '11px', color: verdictColor(r.verdict), fontWeight: 700,
                      padding: '2px 8px', borderRadius: '20px', background: `${verdictColor(r.verdict)}15`
                    }}>
                      {verdictIcon(r.verdict)} {r.verdict}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Empty state */}
        {!result && !bulkResults && !loading && (
          <div style={{ flex: 1, minWidth: '300px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <div style={{ textAlign: 'center', padding: '60px' }}>
              <div style={{ width: '72px', height: '72px', borderRadius: '20px', background: '#4f8eff10', border: '1px solid #4f8eff20', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 20px' }}>
                <Brain size={32} color="#4f8eff" />
              </div>
              <h3 style={{ fontSize: '18px', fontWeight: 700, marginBottom: '8px' }}>Ready to Match</h3>
              <p style={{ color: 'var(--text-secondary)', fontSize: '14px', lineHeight: 1.6, maxWidth: '260px' }}>
                Select a resume and job description, then click Run AI Match to see results.
              </p>
            </div>
          </div>
        )}
      </div>

      <EmailShortlistModal
        isOpen={showEmailModal}
        onClose={() => { setShowEmailModal(false); setSelectedMatchIds([]) }}
        matchIds={selectedMatchIds}
        jobTitle={bulkResults?.jd_title || ''}
        mode="bulk"
      />

      <EmailShortlistModal
        isOpen={showSingleEmailModal}
        onClose={() => setShowSingleEmailModal(false)}
        matchIds={result ? [result.match_id] : []}
        jobTitle={jds.find(j => j.jd_id == selectedJd)?.title || ''}
        candidateName={result?.candidate_name || ''}
        mode="single"
      />
    </div>
  )
}