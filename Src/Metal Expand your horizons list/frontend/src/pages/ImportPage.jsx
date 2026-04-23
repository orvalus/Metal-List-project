import { useState } from 'react'
import { importFromUrl, importFromText } from '../api'

export default function ImportPage() {
  const [tab, setTab] = useState('url')
  const [url, setUrl] = useState('')
  const [text, setText] = useState('')
  const [replace, setReplace] = useState(false)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const handleImport = async () => {
    setLoading(true)
    setResult(null)
    setError(null)
    try {
      const res = tab === 'url'
        ? await importFromUrl(url, replace)
        : await importFromText(text, replace)
      setResult(res.imported)
    } catch (e) {
      setError(e.response?.data?.detail || e.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <div className="page-title">Import date</div>

      <div className="card" style={{ maxWidth: 600 }}>
        <div className="row" style={{ marginBottom: 16, gap: 0 }}>
          {['url', 'text'].map(t => (
            <button
              key={t}
              onClick={() => setTab(t)}
              style={{
                borderRadius: 0,
                background: tab === t ? 'var(--accent)' : 'var(--surface2)',
                color: tab === t ? '#fff' : 'var(--text-muted)',
                border: '1px solid var(--border)',
                borderRadius: t === 'url' ? '6px 0 0 6px' : '0 6px 6px 0',
              }}
            >
              {t === 'url' ? 'Google Docs URL' : 'Text direct'}
            </button>
          ))}
        </div>

        {tab === 'url' ? (
          <div className="form-group">
            <label>URL Google Docs (trebuie sa fie public / "Anyone with link")</label>
            <input
              value={url}
              onChange={e => setUrl(e.target.value)}
              placeholder="https://docs.google.com/document/d/..."
            />
          </div>
        ) : (
          <div className="form-group">
            <label>Lipeste textul din Google Docs</label>
            <textarea
              rows={12}
              value={text}
              onChange={e => setText(e.target.value)}
              placeholder="PROTO-METAL / HARD ROCK&#10;*Early heavy sounds...*&#10;&#10;***Black Sabbath*** - definitive proto-metal..."
              style={{ fontFamily: 'monospace', fontSize: 12 }}
            />
          </div>
        )}

        <div className="row" style={{ marginBottom: 16 }}>
          <label style={{ display: 'flex', alignItems: 'center', gap: 8, cursor: 'pointer', fontSize: 13 }}>
            <input
              type="checkbox"
              style={{ width: 'auto' }}
              checked={replace}
              onChange={e => setReplace(e.target.checked)}
            />
            Sterge datele existente inainte de import
          </label>
        </div>

        {result && (
          <div className="alert alert-success">
            Import reusit: <strong>{result.categories}</strong> categorii,{' '}
            <strong>{result.artists}</strong> artisti,{' '}
            <strong>{result.albums}</strong> albume.
          </div>
        )}

        {error && (
          <div className="alert alert-error">{error}</div>
        )}

        <button
          className="btn-primary"
          onClick={handleImport}
          disabled={loading || (tab === 'url' ? !url.trim() : !text.trim())}
        >
          {loading && <span className="spinner" />}
          {loading ? 'Se importa...' : 'Importa'}
        </button>
      </div>

      <div className="card" style={{ maxWidth: 600, marginTop: 16 }}>
        <div style={{ fontSize: 13, color: 'var(--text-muted)', marginBottom: 8, fontWeight: 600 }}>
          Format asteptat
        </div>
        <pre style={{ fontSize: 11, color: 'var(--text-muted)', lineHeight: 1.7, overflow: 'auto' }}>{`PROTO-METAL / HARD ROCK
*Early heavy sounds before metal crystallized*

***Black Sabbath*** - definitive proto-metal, dark riffs

- Black Sabbath (1970) – 🔥E – ★4.4 – invented the genre
- Paranoid (1970) – 🔥E – ★4.6 – peak sabbath`}
        </pre>
      </div>
    </div>
  )
}
