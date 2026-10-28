import { useState, useEffect } from 'react'
import { useAuth } from '../context/AuthContext'
import api from '../api/axios'
import { FileText, Briefcase, Target, TrendingUp, CheckCircle, ThumbsUp, Minus, XCircle, Clock } from 'lucide-react'

const StatCard = ({ icon: Icon, label, value, color, bg }) => (
  <div className="card" style={{ flex: 1, minWidth: '180px', position: 'relative', overflow: 'hidden' }}>
    <div style={{
      position: 'absolute', top: '-20px', right: '-20px', width: '80px', height: '80px',
      borderRadius: '50%', background: `${color}10`, pointerEvents: 'none'
    }}/>
    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '20px' }}>
      <div style={{
        width: '42px', height: '42px', borderRadius: '12px',
        background: `${color}15`, border: `1px solid ${color}30`,
        display: 'flex', alignItems: 'center', justifyContent: 'center'
      }}>
        <Icon size={20} color={color} strokeWidth={2} />
      </div>
      <div style={{
        padding: '4px 10px', borderRadius: '20px', fontSize: '11px',
        background: '#10b98115', color: '#10b981', fontWeight: 700, letterSpacing: '0.3px'
      }}>LIVE</div>
    </div>
    <div style={{ fontSize: '38px', fontFamily: 'Syne', fontWeight: 800, marginBottom: '6px', letterSpacing: '-1px' }}>{value}</div>
    <div style={{ fontSize: '13px', color: 'var(--text-secondary)', fontWeight: 500 }}>{label}</div>
  </div>
)

const VerdictBar = ({ icon: Icon, label, value, total, color }) => (
  <div className="hover-lift" style={{ marginBottom: '16px' }}>
    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
        <Icon size={14} color={color} />
        <span style={{ fontSize: '13px', color: 'var(--text-secondary)' }}>{label}</span>
      </div>
      <span style={{ fontSize: '13px', fontWeight: 700, color }}>{value}</span>
    </div>
    <div className="progress-bar" style={{ '--target-width': `${total > 0 ? (value / total) * 100 : 0}%`, height: '5px', background: '#ffffff08', borderRadius: '3px', overflow: 'hidden' }}>
      <div style={{
        height: '100%', width: '100%',
        background: `linear-gradient(90deg, ${color}, ${color}99)`,
        borderRadius: '3px'
      }} />
    </div>
  </div>
)

export default function Dashboard() {
  const { user } = useAuth()
  const [stats, setStats] = useState(null)
  const [recentMatches, setRecentMatches] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [statsRes, matchesRes] = await Promise.all([
          api.get('/dashboard/stats'),
          api.get('/dashboard/recent-matches')
        ])
        setStats(statsRes.data)
        setRecentMatches(matchesRes.data.recent_matches || [])
      } catch (err) {
        console.error(err)
      } finally {
        setLoading(false)
      }
    }
    fetchData()
  }, [])

  const getHour = () => new Date().getHours()
  const greeting = getHour() < 12 ? 'Good morning' : getHour() < 17 ? 'Good afternoon' : 'Good evening'

  if (loading) return (
    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '60vh', gap: '12px' }}>
      <div style={{ width: '20px', height: '20px', border: '2px solid #4f8eff', borderTopColor: 'transparent', borderRadius: '50%', animation: 'spin 0.8s linear infinite' }}/>
      <span style={{ color: 'var(--text-secondary)' }}>Loading dashboard...</span>
    </div>
  )

  const verdictColors = {
    'Highly Recommended': '#10b981',
    'Recommended': '#4f8eff',
    'Consider': '#f59e0b',
    'Not Recommended': '#ef4444'
  }

  return (
    <div className="fade-up page-enter">
      <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>

      {/* Header */}
      <div style={{ marginBottom: '36px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '8px' }}>
          <h1 style={{ fontSize: '34px', fontWeight: 800, letterSpacing: '-0.5px' }}>
            {greeting}, {user?.full_name?.split(' ')[0]}
          </h1>
          <span style={{ fontSize: '30px' }}>👋</span>
        </div>
        <p style={{ color: 'var(--text-secondary)', fontSize: '15px' }}>
          Here's your recruitment pipeline overview
        </p>
      </div>

      {/* Stat Cards */}
      <div className="dashboard-cards" style={{ display: 'flex', gap: '16px', marginBottom: '28px', flexWrap: 'wrap' }}>
        <div className="stat-card stagger-1 card"><StatCard icon={FileText} label="Total Resumes" value={stats?.total_resumes || 0} color="#4f8eff" /></div>
        <div className="stat-card stagger-2 card"><StatCard icon={Briefcase} label="Job Descriptions" value={stats?.total_job_descriptions || 0} color="#8b5cf6" /></div>
        <div className="stat-card stagger-3 card"><StatCard icon={Target} label="Total Matches" value={stats?.total_matches || 0} color="#10b981" /></div>
        <div className="stat-card stagger-4 card"><StatCard icon={TrendingUp} label="Avg Match Score" value={`${stats?.average_match_score || 0}%`} color="#f59e0b" /></div>
      </div>

      {/* Bottom Row */}
      <div className="dashboard-grid" style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: '16px' }}>

        {/* Verdict Breakdown */}
        <div className="card">
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '24px' }}>
            <Target size={16} color="var(--accent-blue)" />
            <h3 style={{ fontSize: '15px', fontWeight: 700 }}>Verdict Breakdown</h3>
          </div>
          <VerdictBar icon={CheckCircle} label="Highly Recommended" value={stats?.verdict_breakdown?.highly_recommended || 0} total={stats?.total_matches || 1} color="#10b981" />
          <VerdictBar icon={ThumbsUp} label="Recommended" value={stats?.verdict_breakdown?.recommended || 0} total={stats?.total_matches || 1} color="#4f8eff" />
          <VerdictBar icon={Minus} label="Consider" value={stats?.verdict_breakdown?.consider || 0} total={stats?.total_matches || 1} color="#f59e0b" />
          <VerdictBar icon={XCircle} label="Not Recommended" value={stats?.verdict_breakdown?.not_recommended || 0} total={stats?.total_matches || 1} color="#ef4444" />
        </div>

        {/* Recent Matches */}
        <div className="card">
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '24px' }}>
            <Clock size={16} color="var(--accent-blue)" />
            <h3 style={{ fontSize: '15px', fontWeight: 700 }}>Recent Matches</h3>
          </div>
          {recentMatches.length === 0 ? (
            <div style={{ textAlign: 'center', padding: '48px 20px' }}>
              <div style={{
                width: '56px', height: '56px', borderRadius: '16px', margin: '0 auto 16px',
                background: '#4f8eff10', border: '1px solid #4f8eff20',
                display: 'flex', alignItems: 'center', justifyContent: 'center'
              }}>
                <Target size={24} color="#4f8eff" />
              </div>
              <p style={{ color: 'var(--text-secondary)', fontSize: '14px', lineHeight: 1.6 }}>
                No matches yet.<br/>Upload resumes and create JDs to start!
              </p>
            </div>
          ) : (
            recentMatches.map((match, i) => (
              <div key={match.match_id} style={{
                display: 'flex', alignItems: 'center', justifyContent: 'space-between',
                padding: '14px 0', borderBottom: i < recentMatches.length - 1 ? '1px solid var(--border)' : 'none'
              }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
                  <div style={{
                    width: '38px', height: '38px', borderRadius: '10px',
                    background: '#4f8eff10', display: 'flex', alignItems: 'center', justifyContent: 'center'
                  }}>
                    <FileText size={16} color="#4f8eff" />
                  </div>
                  <div>
                    <div style={{ fontSize: '14px', fontWeight: 600 }}>Match #{match.match_id}</div>
                    <div style={{ fontSize: '12px', color: 'var(--text-secondary)' }}>{match.created_at?.slice(0, 10)}</div>
                  </div>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                  <div style={{
                    fontSize: '20px', fontWeight: 800, fontFamily: 'Syne',
                    color: match.match_score >= 60 ? '#10b981' : match.match_score >= 50 ? '#f59e0b' : '#ef4444'
                  }}>{match.match_score}%</div>
                  <div style={{
                    padding: '4px 12px', borderRadius: '20px', fontSize: '11px', fontWeight: 700,
                    background: `${verdictColors[match.verdict] || '#666'}18`,
                    color: verdictColors[match.verdict] || '#666',
                    letterSpacing: '0.2px'
                  }}>{match.verdict}</div>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  )
}