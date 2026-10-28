// ExportButtons.jsx
// ─────────────────────────────────────────────────────────────────────────────
// Reusable export buttons for CSV + PDF download.
// Place anywhere on Matching page (bulk results) or Results page.
//
// Usage:
//   import ExportButtons from '../components/ExportButtons'
//   <ExportButtons jdId={selectedJdId} jdTitle="Python Developer" />

import { useState } from 'react'
import { Download, FileText, FileSpreadsheet, Loader2 } from 'lucide-react'
import axios from 'axios'

export default function ExportButtons({ jdId, jdTitle = 'results' }) {
  const [loadingCsv, setLoadingCsv] = useState(false)
  const [loadingPdf, setLoadingPdf] = useState(false)

  const triggerDownload = async (format) => {
    const setLoading = format === 'csv' ? setLoadingCsv : setLoadingPdf
    setLoading(true)
    try {
      const response = await axios.get(`/api/v1/export/matches/${format}`, {
        params: { jd_id: jdId },
        responseType: 'blob',
      })
      const blob = new Blob([response.data], {
        type: format === 'csv' ? 'text/csv' : 'application/pdf',
      })
      const url = URL.createObjectURL(blob)
      const a   = document.createElement('a')
      a.href    = url
      a.download = `shortlist_${jdTitle.replace(/\s+/g, '_')}_${new Date().toISOString().slice(0,10)}.${format}`
      document.body.appendChild(a)
      a.click()
      URL.revokeObjectURL(url)
      document.body.removeChild(a)
    } catch (err) {
      alert(`Export failed: ${err?.response?.data?.detail || err.message}`)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex items-center gap-2">
      {/* CSV Button */}
      <button
        onClick={() => triggerDownload('csv')}
        disabled={loadingCsv || !jdId}
        className="flex items-center gap-2 px-4 py-2 bg-green-600/10 border border-green-500/30
                   text-green-400 hover:bg-green-600/20 rounded-xl text-sm font-medium
                   transition-colors disabled:opacity-50"
      >
        {loadingCsv
          ? <Loader2 size={14} className="animate-spin" />
          : <FileSpreadsheet size={14} />}
        Export CSV
      </button>

      {/* PDF Button */}
      <button
        onClick={() => triggerDownload('pdf')}
        disabled={loadingPdf || !jdId}
        className="flex items-center gap-2 px-4 py-2 bg-red-600/10 border border-red-500/30
                   text-red-400 hover:bg-red-600/20 rounded-xl text-sm font-medium
                   transition-colors disabled:opacity-50"
      >
        {loadingPdf
          ? <Loader2 size={14} className="animate-spin" />
          : <FileText size={14} />}
        Export PDF
      </button>
    </div>
  )
}
