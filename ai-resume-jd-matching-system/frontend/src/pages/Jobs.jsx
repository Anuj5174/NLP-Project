import { useState, useEffect } from 'react'
import api from '../api/axios'
import { Briefcase, MapPin, Clock, Plus, X, Trash2, ChevronRight, Search, Building2, Hash } from 'lucide-react'

export default function Jobs() {
  const [jds, setJds] = useState([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [selected, setSelected] = useState(null)
  const [submitting, setSubmitting] = useState(false)
  const [search, setSearch] = useState('')
  const [form, setForm] = useState({
    title: '', company_name: '', description: '',
    experience_required: '', location: ''
  })

  const fetchJds = async () => {
    try {
      const res = await api.get('/jds/')
      setJds(res.data || [])
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { fetchJds() }, [])

  const handleSubmit = async () => {
    if (!form.title || !form.description) return alert('Title and description are required')
    setSubmitting(true)
    try {
      await api.post('/jds/', form)
      setForm({ title: '', company_name: '', description: '', experience_required: '', location: '' })
      setShowForm(false)
      await fetchJds()
    } catch (err) {
      alert('Failed: ' + (err.response?.data?.detail || err.message))
    } finally {
      setSubmitting(false)
    }
  }

  const handleDelete = async (id) => {
    if (!confirm('Delete this job description?')) return
    try {
      await api.delete(`/jds/${id}`)
      setJds(jds.filter(j => j.jd_id !== id))
      if (selected?.jd_id === id) setSelected(null)
    } catch (err) {
      alert('Delete failed')
    }
  }

  const filtered = jds.filter(j =>
    (j.title || '').toLowerCase().includes(search.toLowerCase()) ||
    (j.company_name || '').toLowerCase().includes(search.toLowerCase())
  )

  const inputStyle = {
    width: '100%', padding: '11px 14px', borderRadius: '10px',
    background: '#ffffff08', border: '1px solid var(--border)',
    color: 'var(--text-primary)', fontSize: '14px', outline: 'none',
    fontFamily: 'DM Sans, sans-serif', transition: 'border-color 0.2s'
  }

  return (
    <div className="fade-up page-enter">
      <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>

      {/* Header */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '32px' }}>
        <div>
          <h1 style={{ fontSize: '34px', fontWeight: 800, letterSpacing: '-0.5px', marginBottom: '6px' }}>Job Descriptions</h1>
          <p style={{ color: 'var(--text-secondary)', fontSize: '14px' }}>
            {jds.length} job description{jds.length !== 1 ? 's' : ''} created
          </p>
        </div>
        <button className="btn-primary" onClick={() => setShowForm(!showForm)} style={{
          display: 'flex', alignItems: 'center', gap: '8px',
          padding: '11px 22px', borderRadius: '12px', border: 'none', cursor: 'pointer',
          background: showForm ? '#ffffff10' : 'linear-gradient(135deg, #8b5cf6, #6366f1)',
          color: 'white', fontSize: '14px', fontWeight: 700,
          fontFamily: 'DM Sans, sans-serif',
          boxShadow: showForm ? 'none' : '0 4px 20px #8b5cf630',
          transition: 'all 0.2s'
        }}>
          {showForm ? <X size={16} /> : <Plus size={16} />}
          {showForm ? 'Cancel' : 'New Job'}
        </button>
      </div>

      {/* Create Form */}
      {showForm && (
        <div className="card" style={{ marginBottom: '24px', border: '1px solid #8b5cf630' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '20px' }}>
            <div style={{ width: '32px', height: '32px', borderRadius: '8px', background: '#8b5cf620', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <Briefcase size={16} color="#8b5cf6" />
            </div>
            <h3 style={{ fontSize: '16px', fontWeight: 700 }}>Create Job Description</h3>
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '14px', marginBottom: '14px' }}>
            {[
              { label: 'Job Title *', key: 'title', placeholder: 'e.g. Python Developer' },
              { label: 'Company Name', key: 'company_name', placeholder: 'e.g. Tech Corp' },
              { label: 'Experience Required', key: 'experience_required', placeholder: 'e.g. 1-3 years' },
              { label: 'Location', key: 'location', placeholder: 'e.g. Pune, Maharashtra' },
            ].map(({ label, key, placeholder }) => (
              <div key={key}>
                <label style={{ fontSize: '12px', color: 'var(--text-secondary)', fontWeight: 600, marginBottom: '6px', display: 'block', letterSpacing: '0.3px' }}>{label}</label>
                <input className="glow-border" style={inputStyle} placeholder={placeholder}
                  value={form[key]} onChange={e => setForm({ ...form, [key]: e.target.value })}
                  onFocus={e => e.target.style.borderColor = '#8b5cf6'}
                  onBlur={e => e.target.style.borderColor = 'var(--border)'}
                />
              </div>
            ))}
          </div>
          <div style={{ marginBottom: '16px' }}>
            <label style={{ fontSize: '12px', color: 'var(--text-secondary)', fontWeight: 600, marginBottom: '6px', display: 'block', letterSpacing: '0.3px' }}>Job Description *</label>
            <textarea style={{ ...inputStyle, minHeight: '120px', resize: 'vertical' }}
              placeholder="Describe requirements, responsibilities, and tech stack..."
              value={form.description} onChange={e => setForm({ ...form, description: e.target.value })}
              onFocus={e => e.target.style.borderColor = '#8b5cf6'}
              onBlur={e => e.target.style.borderColor = 'var(--border)'}
            />
          </div>
          <button className="btn-primary" onClick={handleSubmit} disabled={submitting} style={{
            display: 'flex', alignItems: 'center', gap: '8px',
            padding: '11px 24px', borderRadius: '10px', border: 'none', cursor: submitting ? 'not-allowed' : 'pointer',
            background: submitting ? '#333' : 'linear-gradient(135deg, #8b5cf6, #6366f1)',
            color: 'white', fontSize: '14px', fontWeight: 700, fontFamily: 'DM Sans, sans-serif'
          }}>
            <Plus size={16} />
            {submitting ? 'Creating...' : 'Create Job Description'}
          </button>
        </div>
      )}

      {/* Search */}
      <div style={{ position: 'relative', marginBottom: '20px' }}>
        <Search size={16} color="var(--text-secondary)" style={{ position: 'absolute', left: '14px', top: '50%', transform: 'translateY(-50%)' }} />
        <input className="glow-border" value={search} onChange={e => setSearch(e.target.value)}
          placeholder="Search by title or company..."
          style={{
            width: '100%', padding: '11px 14px 11px 42px', borderRadius: '12px',
            background: 'var(--bg-card)', border: '1px solid var(--border)',
            color: 'var(--text-primary)', fontSize: '14px', outline: 'none', fontFamily: 'DM Sans, sans-serif'
          }}
          onFocus={e => e.target.style.borderColor = '#8b5cf6'}
          onBlur={e => e.target.style.borderColor = 'var(--border)'}
        />
      </div>

      <div style={{ display: 'flex', gap: '20px' }}>
        {/* JD List */}
        <div style={{ flex: 1 }}>
          {loading ? (
            <div style={{ textAlign: 'center', padding: '80px', color: 'var(--text-secondary)' }}>
              <div style={{ width: '24px', height: '24px', border: '2px solid #8b5cf6', borderTopColor: 'transparent', borderRadius: '50%', animation: 'spin 0.8s linear infinite', margin: '0 auto 12px' }} />
              Loading...
            </div>
          ) : filtered.length === 0 ? (
            <div className="card" style={{ textAlign: 'center', padding: '64px' }}>
              <div style={{ width: '64px', height: '64px', borderRadius: '20px', background: '#8b5cf610', border: '1px solid #8b5cf620', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 20px' }}>
                <Briefcase size={28} color="#8b5cf6" />
              </div>
              <h3 style={{ fontSize: '18px', fontWeight: 700, marginBottom: '8px' }}>No job descriptions yet</h3>
              <p style={{ color: 'var(--text-secondary)', fontSize: '14px', marginBottom: '24px' }}>Create your first job description to start AI matching</p>
              <button className="btn-primary" onClick={() => setShowForm(true)} style={{
                padding: '10px 24px', borderRadius: '10px', border: 'none', cursor: 'pointer',
                background: 'linear-gradient(135deg, #8b5cf6, #6366f1)', color: 'white',
                fontWeight: 700, fontSize: '14px', fontFamily: 'DM Sans, sans-serif'
              }}>Create First Job</button>
            </div>
          ) : (
            filtered.map((jd, i) => (
              <div key={jd.jd_id} className={`card stagger-${(i % 8) + 1}`} onClick={() => setSelected(jd)}
                style={{
                  display: 'flex', alignItems: 'center', justifyContent: 'space-between',
                  padding: '16px 20px', marginBottom: '8px', borderRadius: '14px', cursor: 'pointer',
                  background: selected?.jd_id === jd.jd_id ? '#8b5cf608' : 'var(--bg-card)',
                  border: `1px solid ${selected?.jd_id === jd.jd_id ? '#8b5cf640' : 'var(--border)'}`,
                  transition: 'all 0.15s'
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                  <div style={{
                    width: '46px', height: '46px', borderRadius: '14px', flexShrink: 0,
                    background: 'linear-gradient(135deg, #8b5cf620, #6366f120)',
                    border: '1px solid #8b5cf620',
                    display: 'flex', alignItems: 'center', justifyContent: 'center'
                  }}>
                    <Briefcase size={20} color="#8b5cf6" />
                  </div>
                  <div>
                    <div style={{ fontWeight: 700, fontSize: '15px', marginBottom: '4px' }}>{jd.title}</div>
                    <div style={{ fontSize: '12px', color: 'var(--text-secondary)', display: 'flex', alignItems: 'center', gap: '10px', flexWrap: 'wrap' }}>
                      {jd.company_name && <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}><Building2 size={11} />{jd.company_name}</span>}
                      {jd.location && <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}><MapPin size={11} />{jd.location}</span>}
                      {jd.experience_required && <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}><Clock size={11} />{jd.experience_required}</span>}
                    </div>
                  </div>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '5px', padding: '4px 10px', borderRadius: '20px', background: '#8b5cf612', border: '1px solid #8b5cf620' }}>
                    <Hash size={11} color="#8b5cf6" />
                    <span style={{ fontSize: '11px', color: '#8b5cf6', fontWeight: 700 }}>JD {jd.jd_id}</span>
                  </div>
                  <ChevronRight size={16} color="var(--text-secondary)" />
                  <button onClick={(e) => { e.stopPropagation(); handleDelete(jd.jd_id) }}
                    style={{ background: 'none', border: 'none', cursor: 'pointer', padding: '6px', borderRadius: '8px', display: 'flex', transition: 'all 0.15s' }}
                    onMouseEnter={e => e.currentTarget.style.background = '#ef444420'}
                    onMouseLeave={e => e.currentTarget.style.background = 'none'}
                  >
                    <Trash2 size={15} color="#ef4444" />
                  </button>
                </div>
              </div>
            ))
          )}
        </div>

        {/* Detail Panel */}
        {selected && (
          <div className="card" style={{ width: '320px', flexShrink: 0, alignSelf: 'flex-start', position: 'sticky', top: '20px', border: '1px solid #8b5cf630' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
              <h3 style={{ fontSize: '15px', fontWeight: 700 }}>Job Details</h3>
              <button onClick={() => setSelected(null)} style={{ background: '#ffffff10', border: 'none', color: 'var(--text-secondary)', cursor: 'pointer', width: '28px', height: '28px', borderRadius: '8px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <X size={14} />
              </button>
            </div>

            <div style={{ padding: '16px', background: '#ffffff05', borderRadius: '12px', marginBottom: '16px' }}>
              <div style={{ fontSize: '18px', fontWeight: 800, marginBottom: '8px', letterSpacing: '-0.3px' }}>{selected.title}</div>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
                {selected.company_name && <div style={{ fontSize: '13px', color: 'var(--text-secondary)', display: 'flex', alignItems: 'center', gap: '6px' }}><Building2 size={13} />{selected.company_name}</div>}
                {selected.location && <div style={{ fontSize: '13px', color: 'var(--text-secondary)', display: 'flex', alignItems: 'center', gap: '6px' }}><MapPin size={13} />{selected.location}</div>}
                {selected.experience_required && <div style={{ fontSize: '13px', color: 'var(--text-secondary)', display: 'flex', alignItems: 'center', gap: '6px' }}><Clock size={13} />{selected.experience_required}</div>}
              </div>
            </div>

            <div>
              <div style={{ fontSize: '11px', color: 'var(--text-secondary)', fontWeight: 700, letterSpacing: '1px', marginBottom: '10px' }}>DESCRIPTION</div>
              <p style={{ fontSize: '13px', lineHeight: 1.7, color: 'var(--text-primary)' }}>{selected.description}</p>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}