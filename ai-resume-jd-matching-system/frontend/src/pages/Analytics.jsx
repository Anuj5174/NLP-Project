import { useState, useEffect } from 'react'
import api from '../api/axios'
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  PieChart, Pie, Cell, LineChart, Line, Legend, AreaChart, Area
} from 'recharts'
import { BarChart3, TrendingUp, Target, Award, Users, Zap } from 'lucide-react'

const COLORS = {
  'Highly Recommended': '#10b981',
  'Recommended': '#4f8eff',
  'Consider': '#f59e0b',
  'Not Recommended': '#ef4444'
}

const CustomTooltip = ({ active, payload, label }) => {
  if (active && payload && payload.length) {
    return (
      <div style={{
        background: '#1a1a2e', border: '1px solid #ffffff20', borderRadius: '10px',
        padding: '10px 14px', fontSize: '13px'
      }}>
        {label && <div style={{ color: 'var(--text-secondary)', marginBottom: '4px' }}>{label}</div>}
        {payload.map((p, i) => (
          <div key={i} style={{ color: p.color || '#fff', fontWeight: 700 }}>
            {p.name}: {p.value}
          </div>
        ))}
      </div>
    )
  }
  return null
}

const SummaryCard = ({ icon: Icon, label, value, sub, color }) => (
  <div className="card" style={{ flex: 1, minWidth: '140px' }}>
    <div style={{ width: '40px', height: '40px', borderRadius: '12px', background: `${color}15`, border: `1px solid ${color}25`, display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '16px' }}>
      <Icon size={18} color={color} />
    </div>
    <div style={{ fontSize: '36px', fontFamily: 'Syne', fontWeight: 800, letterSpacing: '-1px', marginBottom: '4px' }}>{value}</div>
    <div style={{ fontSize: '13px', color: 'var(--text-secondary)', marginBottom: '2px' }}>{label}</div>
    {sub && <div style={{ fontSize: '12px', color, fontWeight: 600 }}>{sub}</div>}
  </div>
)

export default function Analytics() {
  const [stats, setStats] = useState(null)
  const [matches, setMatches] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [statsRes, matchesRes] = await Promise.all([
          api.get('/dashboard/stats'),
          api.get('/dashboard/recent-matches')
        ])
        setStats(statsRes.data)
        setMatches(matchesRes.data.recent_matches || [])
      } catch (err) {
        console.error(err)
      } finally {
        setLoading(false)
      }
    }
    fetchData()
  }, [])

  if (loading) return (
    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '60vh', gap: '12px' }}>
      <div style={{ width: '20px', height: '20px', border: '2px solid #4f8eff', borderTopColor: 'transparent', borderRadius: '50%', animation: 'spin 0.8s linear infinite' }} />
      <span style={{ color: 'var(--text-secondary)' }}>Loading analytics...</span>
      <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>
    </div>
  )

  // Verdict Pie Data
  const verdictData = [
    { name: 'Highly Recommended', value: stats?.verdict_breakdown?.highly_recommended || 0 },
    { name: 'Recommended', value: stats?.verdict_breakdown?.recommended || 0 },
    { name: 'Consider', value: stats?.verdict_breakdown?.consider || 0 },
    { name: 'Not Recommended', value: stats?.verdict_breakdown?.not_recommended || 0 },
  ].filter(d => d.value > 0)

  // Score Distribution
  const scoreRanges = [
    { range: '0-20%', count: 0 },
    { range: '21-40%', count: 0 },
    { range: '41-60%', count: 0 },
    { range: '61-80%', count: 0 },
    { range: '81-100%', count: 0 },
  ]
  matches.forEach(m => {
    const s = m.match_score
    if (s <= 20) scoreRanges[0].count++
    else if (s <= 40) scoreRanges[1].count++
    else if (s <= 60) scoreRanges[2].count++
    else if (s <= 80) scoreRanges[3].count++
    else scoreRanges[4].count++
  })

  // Matches over time (group by date)
  const timeMap = {}
  matches.forEach(m => {
    const date = m.created_at?.slice(0, 10) || 'Unknown'
    timeMap[date] = (timeMap[date] || 0) + 1
  })
  const timeData = Object.entries(timeMap)
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([date, count]) => ({ date, count }))

  // Score trend over time
  const scoreTrend = [...matches]
    .reverse()
    .map((m, i) => ({ index: `#${m.match_id}`, score: m.match_score }))

  const hasData = matches.length > 0
  const bestMatch = matches.length > 0 ? Math.max(...matches.map(m => m.match_score)) : 0
  const avgScore = matches.length > 0 ? Math.round(matches.reduce((a, m) => a + m.match_score, 0) / matches.length) : 0
  const highlyRec = stats?.verdict_breakdown?.highly_recommended || 0

  return (
    <div className="fade-up page-enter">
      <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>

      {/* Header */}
      <div style={{ marginBottom: '36px' }}>
        <h1 style={{ fontSize: '34px', fontWeight: 800, letterSpacing: '-0.5px', marginBottom: '6px' }}>Analytics</h1>
        <p style={{ color: 'var(--text-secondary)', fontSize: '14px' }}>Deep insights into your recruitment pipeline</p>
      </div>

      {/* Summary Cards */}
      <div style={{ display: 'flex', gap: '16px', marginBottom: '24px', flexWrap: 'wrap' }}>
        <SummaryCard icon={Users} label="Total Resumes" value={stats?.total_resumes || 0} color="#4f8eff" sub="In database" />
        <SummaryCard icon={Target} label="Total Matches" value={stats?.total_matches || 0} color="#8b5cf6" sub="AI analyzed" />
        <SummaryCard icon={TrendingUp} label="Avg Score" value={`${avgScore}%`} color="#10b981" sub="Match accuracy" />
        <SummaryCard icon={Award} label="Best Match" value={`${bestMatch}%`} color="#f59e0b" sub="Highest score" />
        <SummaryCard icon={Zap} label="Top Candidates" value={highlyRec} color="#ec4899" sub="Highly recommended" />
      </div>

      {!hasData ? (
        <div className="card" style={{ textAlign: 'center', padding: '80px' }}>
          <div style={{ width: '64px', height: '64px', borderRadius: '20px', background: '#4f8eff10', border: '1px solid #4f8eff20', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 20px' }}>
            <BarChart3 size={28} color="#4f8eff" />
          </div>
          <h3 style={{ fontSize: '18px', fontWeight: 700, marginBottom: '8px' }}>No data yet</h3>
          <p style={{ color: 'var(--text-secondary)', fontSize: '14px' }}>Run some matches to see analytics charts here</p>
        </div>
      ) : (
        <>
          {/* Row 1 - Pie + Bar */}
          <div className="analytics-grid" style={{ display: 'grid', gridTemplateColumns: '1fr 1.5fr', gap: '16px', marginBottom: '16px' }}>

            {/* Verdict Pie */}
            <div className="card stagger-1">
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '24px' }}>
                <div style={{ width: '32px', height: '32px', borderRadius: '8px', background: '#8b5cf615', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                  <Target size={15} color="#8b5cf6" />
                </div>
                <h3 style={{ fontSize: '15px', fontWeight: 700 }}>Verdict Distribution</h3>
              </div>
              {verdictData.length > 0 ? (
                <>
                  <ResponsiveContainer width="100%" height={200}>
                    <PieChart>
                      <Pie data={verdictData} cx="50%" cy="50%" innerRadius={55} outerRadius={85}
                        paddingAngle={3} dataKey="value"
                      >
                        {verdictData.map((entry, i) => (
                          <Cell key={i} fill={COLORS[entry.name]} stroke="transparent" />
                        ))}
                      </Pie>
                      <Tooltip content={<CustomTooltip />} />
                    </PieChart>
                  </ResponsiveContainer>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', marginTop: '8px' }}>
                    {verdictData.map((d, i) => (
                      <div key={i} style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                          <div style={{ width: '8px', height: '8px', borderRadius: '50%', background: COLORS[d.name] }} />
                          <span style={{ fontSize: '13px', color: 'var(--text-secondary)' }}>{d.name}</span>
                        </div>
                        <span style={{ fontSize: '13px', fontWeight: 700, color: COLORS[d.name] }}>{d.value}</span>
                      </div>
                    ))}
                  </div>
                </>
              ) : (
                <div style={{ textAlign: 'center', padding: '40px', color: 'var(--text-secondary)', fontSize: '14px' }}>No verdict data yet</div>
              )}
            </div>

            {/* Score Distribution Bar */}
            <div className="card stagger-2">
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '24px' }}>
                <div style={{ width: '32px', height: '32px', borderRadius: '8px', background: '#4f8eff15', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                  <BarChart3 size={15} color="#4f8eff" />
                </div>
                <h3 style={{ fontSize: '15px', fontWeight: 700 }}>Score Distribution</h3>
              </div>
              <ResponsiveContainer width="100%" height={260}>
                <BarChart data={scoreRanges} barSize={32}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#ffffff08" vertical={false} />
                  <XAxis dataKey="range" tick={{ fill: '#64748b', fontSize: 12 }} axisLine={false} tickLine={false} />
                  <YAxis tick={{ fill: '#64748b', fontSize: 12 }} axisLine={false} tickLine={false} allowDecimals={false} />
                  <Tooltip content={<CustomTooltip />} cursor={{ fill: '#ffffff05' }} />
                  <Bar dataKey="count" name="Matches" radius={[6, 6, 0, 0]}>
                    {scoreRanges.map((entry, i) => (
                      <Cell key={i} fill={
                        i === 0 ? '#ef4444' : i === 1 ? '#f97316' : i === 2 ? '#f59e0b' : i === 3 ? '#4f8eff' : '#10b981'
                      } />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Row 2 - Line Charts */}
          <div className="analytics-grid" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>

            {/* Score Trend */}
            <div className="card stagger-3">
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '24px' }}>
                <div style={{ width: '32px', height: '32px', borderRadius: '8px', background: '#10b98115', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                  <TrendingUp size={15} color="#10b981" />
                </div>
                <h3 style={{ fontSize: '15px', fontWeight: 700 }}>Score Trend</h3>
              </div>
              <ResponsiveContainer width="100%" height={220}>
                <AreaChart data={scoreTrend}>
                  <defs>
                    <linearGradient id="scoreGrad" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#4f8eff" stopOpacity={0.3} />
                      <stop offset="95%" stopColor="#4f8eff" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="#ffffff08" vertical={false} />
                  <XAxis dataKey="index" tick={{ fill: '#64748b', fontSize: 11 }} axisLine={false} tickLine={false} />
                  <YAxis domain={[0, 100]} tick={{ fill: '#64748b', fontSize: 11 }} axisLine={false} tickLine={false} />
                  <Tooltip content={<CustomTooltip />} />
                  <Area type="monotone" dataKey="score" name="Score" stroke="#4f8eff" strokeWidth={2.5} fill="url(#scoreGrad)" dot={{ fill: '#4f8eff', r: 4 }} activeDot={{ r: 6 }} />
                </AreaChart>
              </ResponsiveContainer>
            </div>

            {/* Matches Per Day */}
            <div className="card stagger-4">
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '24px' }}>
                <div style={{ width: '32px', height: '32px', borderRadius: '8px', background: '#f59e0b15', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                  <Zap size={15} color="#f59e0b" />
                </div>
                <h3 style={{ fontSize: '15px', fontWeight: 700 }}>Matches Per Day</h3>
              </div>
              {timeData.length > 0 ? (
                <ResponsiveContainer width="100%" height={220}>
                  <BarChart data={timeData} barSize={28}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#ffffff08" vertical={false} />
                    <XAxis dataKey="date" tick={{ fill: '#64748b', fontSize: 11 }} axisLine={false} tickLine={false} />
                    <YAxis tick={{ fill: '#64748b', fontSize: 11 }} axisLine={false} tickLine={false} allowDecimals={false} />
                    <Tooltip content={<CustomTooltip />} cursor={{ fill: '#ffffff05' }} />
                    <Bar dataKey="count" name="Matches" fill="#f59e0b" radius={[6, 6, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              ) : (
                <div style={{ textAlign: 'center', padding: '40px', color: 'var(--text-secondary)', fontSize: '14px' }}>Not enough data yet</div>
              )}
            </div>
          </div>
        </>
      )}
    </div>
  )
}