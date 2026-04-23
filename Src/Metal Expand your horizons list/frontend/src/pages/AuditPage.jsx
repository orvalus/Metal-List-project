import { useEffect, useState } from 'react'
import { getArtists, getCategories, auditArtist } from '../api'

export default function AuditPage() {
  const [categories, setCategories] = useState([])
  const [artists, setArtists] = useState([])
  const [selectedCat, setSelectedCat] = useState('')
  const [selectedArtist, setSelectedArtist] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    Promise.all([getCategories(), getArtists()]).then(([cats, arts]) => {
      setCategories(cats)
      setArtists(arts)
    })
  }, [])

  const filteredArtists = selectedCat
    ? artists.filter(a => a.category_id === Number(selectedCat))
    : artists

  const runAudit = async () => {
    if (!selectedArtist) return
    setLoading(true)
    setResult(null)
    setError(null)
    try {
      const res = await auditArtist(Number(selectedArtist))
      setResult(res)
    } catch (e) {
      setError(e.response?.data?.detail || e.message)
    } finally {
      setLoading(false)
    }
  }

  const hasIssues = result && (
    result.missing_albums?.length > 0 ||
    result.extra_albums?.length > 0 ||
    result.order_issues?.length > 0 ||
    result.rating_diffs?.length > 0
  )

  return (
    <div>
      <div className="page-title">Audit Sputnikmusic</div>

      <div className="card" style={{ maxWidth: 500, marginBottom: 20 }}>
        <div className="form-group">
          <label>Filtreaza dupa categorie</label>
          <select value={selectedCat} onChange={e => { setSelectedCat(e.target.value); setSelectedArtist('') }}>
            <option value="">Toate categoriile</option>
            {categories.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
          </select>
        </div>
        <div className="form-group">
          <label>Alege artistul de auditat</label>
          <select value={selectedArtist} onChange={e => setSelectedArtist(e.target.value)}>
            <option value="">— Selecteaza artist —</option>
            {filteredArtists.map(a => <option key={a.id} value={a.id}>{a.name}</option>)}
          </select>
        </div>
        <button
          className="btn-primary"
          onClick={runAudit}
          disabled={loading || !selectedArtist}
        >
          {loading && <span className="spinner" />}
          {loading ? 'Se verifica...' : 'Ruleaza audit'}
        </button>
      </div>

      {error && <div className="alert alert-error">{error}</div>}

      {result && (
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 16 }}>
            <h2 style={{ fontSize: 17, fontWeight: 700 }}>{result.artist}</h2>
            {result.sputnik_url && (
              <a href={result.sputnik_url} target="_blank" rel="noreferrer" style={{ fontSize: 12 }}>
                Vezi pe Sputnikmusic ↗
              </a>
            )}
            {!result.error && !hasIssues && (
              <span className="badge" style={{ background: '#0d2b1a', color: '#6fcf97' }}>
                ✓ Lista completa, nicio problema
              </span>
            )}
          </div>

          {result.error && (
            <div className="alert alert-error">{result.error}</div>
          )}

          {/* Albume lipsa */}
          {result.missing_albums?.length > 0 && (
            <div className="card" style={{ marginBottom: 12, borderLeft: '3px solid #e74c3c' }}>
              <div style={{ fontWeight: 700, color: '#e74c3c', marginBottom: 10, fontSize: 13 }}>
                ✗ Albume lipsa din lista ta ({result.missing_albums.length})
              </div>
              {result.missing_albums.map((a, i) => (
                <div key={i} style={{ padding: '4px 0', borderBottom: '1px solid var(--border)', fontSize: 13, display: 'flex', gap: 12 }}>
                  <span style={{ color: 'var(--text-muted)', width: 36 }}>{a.year || '—'}</span>
                  <span>{a.title}</span>
                  {a.rating && <span style={{ color: '#f1c40f' }}>★{a.rating}</span>}
                </div>
              ))}
            </div>
          )}

          {/* Albume extra */}
          {result.extra_albums?.length > 0 && (
            <div className="card" style={{ marginBottom: 12, borderLeft: '3px solid #f39c12' }}>
              <div style={{ fontWeight: 700, color: '#f39c12', marginBottom: 10, fontSize: 13 }}>
                ? Albume in lista ta, negasite pe Sputnikmusic ({result.extra_albums.length})
              </div>
              {result.extra_albums.map((title, i) => (
                <div key={i} style={{ padding: '4px 0', borderBottom: '1px solid var(--border)', fontSize: 13 }}>
                  {title}
                </div>
              ))}
            </div>
          )}

          {/* Probleme ordine */}
          {result.order_issues?.length > 0 && (
            <div className="card" style={{ marginBottom: 12, borderLeft: '3px solid #9b59b6' }}>
              <div style={{ fontWeight: 700, color: '#9b59b6', marginBottom: 10, fontSize: 13 }}>
                ↕ Probleme ordine cronologica ({result.order_issues.length})
              </div>
              {result.order_issues.map((issue, i) => (
                <div key={i} style={{ padding: '4px 0', borderBottom: '1px solid var(--border)', fontSize: 12, color: 'var(--text-muted)' }}>
                  {issue}
                </div>
              ))}
            </div>
          )}

          {/* Diferente rating */}
          {result.rating_diffs?.length > 0 && (
            <div className="card" style={{ marginBottom: 12, borderLeft: '3px solid #3498db' }}>
              <div style={{ fontWeight: 700, color: '#3498db', marginBottom: 10, fontSize: 13 }}>
                ★ Diferente de rating ≥ 0.2 ({result.rating_diffs.length})
              </div>
              {result.rating_diffs.map((d, i) => (
                <div key={i} style={{ padding: '4px 0', borderBottom: '1px solid var(--border)', fontSize: 13, display: 'flex', gap: 12, alignItems: 'center' }}>
                  <span style={{ flex: 1 }}>{d.title}</span>
                  <span style={{ color: '#6fcf97' }}>Lista: ★{d.db_rating}</span>
                  <span style={{ color: '#f1c40f' }}>Sputnik: ★{d.sputnik_rating}</span>
                  <span style={{ color: 'var(--text-muted)', fontSize: 11 }}>Δ{d.diff}</span>
                </div>
              ))}
            </div>
          )}

          {/* Discografia completa Sputnikmusic */}
          {result.sputnik_albums?.length > 0 && (
            <details style={{ marginTop: 16 }}>
              <summary style={{ cursor: 'pointer', color: 'var(--text-muted)', fontSize: 13, marginBottom: 8 }}>
                Discografie completa Sputnikmusic ({result.sputnik_albums.length} albume)
              </summary>
              <div className="card" style={{ marginTop: 8 }}>
                {result.sputnik_albums.map((a, i) => (
                  <div key={i} style={{ padding: '4px 0', borderBottom: '1px solid var(--border)', fontSize: 13, display: 'flex', gap: 12 }}>
                    <span style={{ color: 'var(--text-muted)', width: 36 }}>{a.year || '—'}</span>
                    <span style={{ flex: 1 }}>{a.title}</span>
                    {a.rating && <span style={{ color: '#f1c40f' }}>★{a.rating}</span>}
                  </div>
                ))}
              </div>
            </details>
          )}
        </div>
      )}
    </div>
  )
}
