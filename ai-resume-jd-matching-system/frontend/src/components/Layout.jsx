import { useState, useEffect } from 'react'
import { NavLink } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { 
  LayoutDashboard, FileText, Briefcase, Target, LogOut, 
  ChevronLeft, ChevronRight, Cpu, BarChart3, Menu, X 
} from 'lucide-react'

const navItems = [
  { path: '/dashboard', icon: LayoutDashboard, label: 'Dashboard' },
  { path: '/resumes', icon: FileText, label: 'Resumes' },
  { path: '/jobs', icon: Briefcase, label: 'Job Descriptions' },
  { path: '/matching', icon: Target, label: 'AI Matching' },
  { path: '/analytics', icon: BarChart3, label: 'Analytics' },
]

export default function Layout({ children }) {
  const { user, logout } = useAuth()
  const [collapsed, setCollapsed] = useState(false)
  const [mobileOpen, setMobileOpen] = useState(false)
  const [isMobile, setIsMobile] = useState(window.innerWidth < 768)

  useEffect(() => {
    const handleResize = () => {
      const mobile = window.innerWidth < 768
      setIsMobile(mobile)
      if (!mobile) setMobileOpen(false)
    }
    window.addEventListener('resize', handleResize)
    return () => window.removeEventListener('resize', handleResize)
  }, [])

  // Close mobile menu on nav click
  const handleNavClick = () => {
    if (isMobile) setMobileOpen(false)
  }

  const sidebarWidth = isMobile ? '260px' : collapsed ? '72px' : '248px'

  return (
    <div style={{ display: 'flex', minHeight: '100vh', background: 'var(--bg-primary)' }}>
      <style>{`
        @keyframes slideIn {
          from { transform: translateX(-100%); }
          to   { transform: translateX(0); }
        }
        @keyframes fadeIn {
          from { opacity: 0; }
          to   { opacity: 1; }
        }
        .mobile-overlay {
          position: fixed; inset: 0; background: rgba(0,0,0,0.6);
          z-index: 99; animation: fadeIn 0.2s ease;
          backdrop-filter: blur(4px);
        }
        .nav-link-item {
          display: flex; align-items: center; gap: 10px;
          padding: 10px 10px; border-radius: 8px; margin-bottom: 2px;
          text-decoration: none; font-size: 14px;
          transition: all 0.15s; white-space: nowrap;
        }
        .nav-link-item:hover {
          background: #ffffff08 !important;
        }
        .hamburger-btn {
          position: fixed; top: 14px; left: 14px; z-index: 200;
          width: 40px; height: 40px; border-radius: 10px;
          background: var(--bg-secondary); border: 1px solid var(--border);
          display: flex; align-items: center; justify-content: center;
          cursor: pointer; transition: all 0.2s;
          box-shadow: 0 4px 20px #00000040;
        }
        .hamburger-btn:hover { background: #ffffff10; }
      `}</style>

      {/* MOBILE HAMBURGER BUTTON */}
      {isMobile && (
        <button className="hamburger-btn" onClick={() => setMobileOpen(!mobileOpen)}>
          {mobileOpen 
            ? <X size={18} color="var(--text-primary)" strokeWidth={2} />
            : <Menu size={18} color="var(--text-primary)" strokeWidth={2} />
          }
        </button>
      )}

      {/* MOBILE OVERLAY */}
      {isMobile && mobileOpen && (
        <div className="mobile-overlay" onClick={() => setMobileOpen(false)} />
      )}

      {/* SIDEBAR */}
      <aside style={{
        width: sidebarWidth,
        background: 'var(--bg-secondary)',
        borderRight: '1px solid var(--border)',
        display: 'flex', flexDirection: 'column',
        transition: isMobile ? 'transform 0.3s cubic-bezier(0.4,0,0.2,1)' : 'width 0.3s cubic-bezier(0.4,0,0.2,1)',
        position: 'fixed', height: '100vh', zIndex: 100, overflow: 'hidden',
        transform: isMobile ? (mobileOpen ? 'translateX(0)' : 'translateX(-100%)') : 'translateX(0)',
        animation: isMobile && mobileOpen ? 'slideIn 0.3s ease' : 'none',
      }}>

        {/* Logo */}
        <div style={{
          padding: '20px 16px', borderBottom: '1px solid var(--border)',
          display: 'flex', alignItems: 'center', gap: '12px',
          marginTop: isMobile ? '0' : '0'
        }}>
          <div style={{
            width: '38px', height: '38px', borderRadius: '10px', flexShrink: 0,
            background: 'linear-gradient(135deg, #4f8eff, #8b5cf6)',
            display: 'flex', alignItems: 'center', justifyContent: 'center'
          }}>
            <Cpu size={20} color="white" strokeWidth={2} />
          </div>
          {(!collapsed || isMobile) && (
            <div>
              <div style={{ fontFamily: 'Syne, sans-serif', fontWeight: 800, fontSize: '16px', letterSpacing: '-0.3px' }}>RecruitAI</div>
              <div style={{ fontSize: '11px', color: 'var(--text-secondary)', letterSpacing: '0.3px' }}>SMART HIRING</div>
            </div>
          )}
          {/* Close button on mobile */}
          {isMobile && (
            <button onClick={() => setMobileOpen(false)} style={{
              marginLeft: 'auto', background: 'none', border: 'none',
              cursor: 'pointer', color: 'var(--text-secondary)', display: 'flex', alignItems: 'center'
            }}>
              <X size={18} strokeWidth={2} />
            </button>
          )}
        </div>

        {/* Nav */}
        <nav style={{ padding: '12px 10px', flex: 1, overflowY: 'auto' }}>
          {(!collapsed || isMobile) && (
            <div style={{ fontSize: '10px', color: 'var(--text-secondary)', fontWeight: 700, letterSpacing: '1px', padding: '8px 8px 4px', marginBottom: '4px' }}>
              NAVIGATION
            </div>
          )}
          {navItems.map((item) => {
            const Icon = item.icon
            return (
              <NavLink
                key={item.path}
                to={item.path}
                onClick={handleNavClick}
                style={({ isActive }) => ({
                  display: 'flex', alignItems: 'center', gap: '10px',
                  padding: '10px 10px', borderRadius: '8px', marginBottom: '2px',
                  textDecoration: 'none',
                  color: isActive ? '#fff' : 'var(--text-secondary)',
                  background: isActive ? 'linear-gradient(135deg, #4f8eff, #6366f1)' : 'transparent',
                  fontWeight: isActive ? 600 : 400, fontSize: '14px',
                  transition: 'all 0.15s', whiteSpace: 'nowrap',
                  boxShadow: isActive ? '0 4px 15px #4f8eff30' : 'none'
                })}
              >
                <Icon size={17} strokeWidth={2} style={{ flexShrink: 0 }} />
                {(!collapsed || isMobile) && item.label}
              </NavLink>
            )
          })}
        </nav>

        {/* Bottom */}
        <div style={{ padding: '12px 10px', borderTop: '1px solid var(--border)' }}>
          {(!collapsed || isMobile) && (
            <div style={{
              padding: '10px', marginBottom: '8px', borderRadius: '8px',
              background: '#ffffff05', border: '1px solid var(--border)'
            }}>
              <div style={{ fontSize: '13px', fontWeight: 600, marginBottom: '2px', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                {user?.full_name || 'User'}
              </div>
              <div style={{ fontSize: '11px', color: 'var(--text-secondary)', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                {user?.email}
              </div>
            </div>
          )}
          <button onClick={logout} style={{
            width: '100%', padding: '9px 10px', borderRadius: '8px',
            background: 'transparent', border: 'none',
            color: 'var(--text-secondary)', cursor: 'pointer', fontSize: '13px',
            display: 'flex', alignItems: 'center', gap: '10px',
            transition: 'all 0.15s', fontFamily: 'DM Sans, sans-serif'
          }}
            onMouseEnter={e => { e.currentTarget.style.background = '#ef444415'; e.currentTarget.style.color = '#ef4444' }}
            onMouseLeave={e => { e.currentTarget.style.background = 'transparent'; e.currentTarget.style.color = 'var(--text-secondary)' }}
          >
            <LogOut size={16} strokeWidth={2} style={{ flexShrink: 0 }} />
            {(!collapsed || isMobile) && 'Logout'}
          </button>

          {/* Collapse button — desktop only */}
          {!isMobile && (
            <button onClick={() => setCollapsed(!collapsed)} style={{
              width: '100%', padding: '9px 10px', borderRadius: '8px',
              background: 'transparent', border: 'none',
              color: 'var(--text-secondary)', cursor: 'pointer',
              display: 'flex', alignItems: 'center', gap: '10px',
              marginTop: '2px', transition: 'all 0.15s', fontFamily: 'DM Sans, sans-serif', fontSize: '13px'
            }}
              onMouseEnter={e => e.currentTarget.style.background = '#ffffff08'}
              onMouseLeave={e => e.currentTarget.style.background = 'transparent'}
            >
              {collapsed ? <ChevronRight size={16} /> : <ChevronLeft size={16} />}
              {!collapsed && 'Collapse'}
            </button>
          )}
        </div>
      </aside>

      {/* MAIN CONTENT */}
      <main style={{
        marginLeft: isMobile ? '0' : (collapsed ? '72px' : '248px'),
        flex: 1,
        padding: isMobile ? '64px 16px 24px' : '36px',
        transition: 'margin-left 0.3s cubic-bezier(0.4,0,0.2,1)',
        minHeight: '100vh',
        width: '100%',
        maxWidth: '100%',
        overflowX: 'hidden'
      }}>
        {children}
      </main>
    </div>
  )
}