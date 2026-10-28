// EmailShortlistModal.jsx
// ─────────────────────────────────────────────────────────────────────────────
// Drop-in modal component for sending shortlist emails.
// Used on BOTH Bulk Match results page AND individual Match result page.
//
// Usage:
//   import EmailShortlistModal from '../components/EmailShortlistModal'
//
//   // Bulk (from Bulk match page — pass array of match IDs)
//   <EmailShortlistModal
//     isOpen={showEmailModal}
//     onClose={() => setShowEmailModal(false)}
//     matchIds={selectedMatchIds}        // e.g. [1, 3, 5]
//     jobTitle="Python Developer"
//     mode="bulk"
//   />
//
//   // Single (from individual match result page — pass one match ID)
//   <EmailShortlistModal
//     isOpen={showEmailModal}
//     onClose={() => setShowEmailModal(false)}
//     matchIds={[matchId]}               // e.g. [7]
//     jobTitle="Data Scientist"
//     candidateName="Priya Sharma"
//     mode="single"
//   />

import { useState } from 'react'
import api from '../api/axios'
import { X, Mail, Send, CheckCircle, XCircle, Loader2 } from 'lucide-react'

export default function EmailShortlistModal({
  isOpen,
  onClose,
  matchIds = [],
  jobTitle = '',
  candidateName = '',
  mode = 'bulk',           // 'bulk' | 'single'
}) {
  const [subject, setSubject] = useState(
    `Interview Invitation — ${jobTitle}`
  )
  const [message, setMessage] = useState(
    `We have reviewed your profile and are impressed with your background. ` +
    `We would like to invite you for an interview. ` +
    `Please reply to this email with your availability for the coming week.`
  )
  const [sending, setSending] = useState(false)
  const [results, setResults] = useState(null)   // null | { sent, failed, results[] }

  if (!isOpen) return null

  const handleSend = async () => {
    setSending(true)
    setResults(null)
    try {
      const endpoint = mode === 'single'
        ? '/shortlist/email/single'
        : '/shortlist/email'

      const payload = mode === 'single'
        ? { match_id: matchIds[0], custom_message: message, subject }
        : { match_ids: matchIds, custom_message: message, subject }

      const { data } = await api.post(endpoint, payload)

      // Normalise single response to same shape as bulk
      if (mode === 'single') {
        setResults({
          total: 1,
          sent: data.success ? 1 : 0,
          failed: data.success ? 0 : 1,
          results: [data],
        })
      } else {
        setResults(data)
      }
    } catch (err) {
      setResults({
        total: matchIds.length,
        sent: 0,
        failed: matchIds.length,
        results: [{ success: false, error: err?.response?.data?.detail || 'Server error' }],
      })
    } finally {
      setSending(false)
    }
  }

  const handleClose = () => {
    setResults(null)
    onClose()
  }

  return (
    <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div className="bg-[#0d1220] border border-[#1e2d50] rounded-2xl w-full max-w-lg shadow-2xl">

        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-[#1e2d50]">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 bg-blue-600/20 rounded-lg flex items-center justify-center">
              <Mail size={18} className="text-blue-400" />
            </div>
            <div>
              <h2 className="text-white font-semibold text-base">
                {mode === 'bulk' ? `Email ${matchIds.length} Candidate${matchIds.length !== 1 ? 's' : ''}` : `Email ${candidateName || 'Candidate'}`}
              </h2>
              <p className="text-gray-400 text-xs mt-0.5">Re: {jobTitle}</p>
            </div>
          </div>
          <button onClick={handleClose} className="text-gray-400 hover:text-white transition-colors">
            <X size={20} />
          </button>
        </div>

        {/* Results view */}
        {results ? (
          <div className="p-6">
            {/* Summary */}
            <div className="flex gap-3 mb-5">
              <div className="flex-1 bg-green-500/10 border border-green-500/20 rounded-xl p-4 text-center">
                <p className="text-2xl font-bold text-green-400">{results.sent}</p>
                <p className="text-xs text-gray-400 mt-1">Sent ✓</p>
              </div>
              <div className="flex-1 bg-red-500/10 border border-red-500/20 rounded-xl p-4 text-center">
                <p className="text-2xl font-bold text-red-400">{results.failed}</p>
                <p className="text-xs text-gray-400 mt-1">Failed ✗</p>
              </div>
            </div>

            {/* Per-candidate result */}
            <div className="space-y-2 max-h-48 overflow-y-auto">
              {results.results.map((r, i) => (
                <div
                  key={i}
                  className={`flex items-center gap-3 p-3 rounded-lg text-sm ${
                    r.success
                      ? 'bg-green-500/5 border border-green-500/20'
                      : 'bg-red-500/5 border border-red-500/20'
                  }`}
                >
                  {r.success
                    ? <CheckCircle size={15} className="text-green-400 shrink-0" />
                    : <XCircle    size={15} className="text-red-400 shrink-0" />}
                  <span className="text-gray-300 flex-1 truncate">
                    {r.candidate_name || 'Candidate'}{' '}
                    <span className="text-gray-500 text-xs">({r.candidate_email || ''})</span>
                  </span>
                  {!r.success && (
                    <span className="text-red-400 text-xs shrink-0">{r.error}</span>
                  )}
                </div>
              ))}
            </div>

            <button
              onClick={handleClose}
              className="w-full mt-5 bg-blue-600 hover:bg-blue-700 text-white py-2.5 rounded-xl font-medium transition-colors"
            >
              Done
            </button>
          </div>
        ) : (
          /* Compose view */
          <div className="p-6 space-y-4">
            <div>
              <label className="block text-gray-400 text-xs font-medium mb-1.5">Email Subject</label>
              <input
                value={subject}
                onChange={e => setSubject(e.target.value)}
                className="w-full bg-[#060810] border border-[#1e2d50] rounded-xl px-4 py-2.5
                           text-white text-sm focus:outline-none focus:border-blue-500 transition-colors"
              />
            </div>
            <div>
              <label className="block text-gray-400 text-xs font-medium mb-1.5">
                Personal Message <span className="text-gray-600">(added to email body)</span>
              </label>
              <textarea
                value={message}
                onChange={e => setMessage(e.target.value)}
                rows={5}
                className="w-full bg-[#060810] border border-[#1e2d50] rounded-xl px-4 py-2.5
                           text-white text-sm focus:outline-none focus:border-blue-500 transition-colors resize-none"
              />
            </div>

            {/* Info note */}
            <div className="bg-blue-500/10 border border-blue-500/20 rounded-xl p-3 text-xs text-blue-300">
              Each email will include the candidate's match score, verdict, and matched skills automatically.
            </div>

            <div className="flex gap-3 pt-1">
              <button
                onClick={handleClose}
                className="flex-1 border border-[#1e2d50] text-gray-400 hover:text-white
                           py-2.5 rounded-xl font-medium transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={handleSend}
                disabled={sending || matchIds.length === 0}
                className="flex-1 bg-blue-600 hover:bg-blue-700 disabled:opacity-50
                           text-white py-2.5 rounded-xl font-medium transition-colors
                           flex items-center justify-center gap-2"
              >
                {sending
                  ? <><Loader2 size={15} className="animate-spin" /> Sending...</>
                  : <><Send size={15} /> Send {matchIds.length > 1 ? `${matchIds.length} Emails` : 'Email'}</>
                }
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
