import { useEffect, useState } from 'react'
import { getFullList } from '../api'

const ICON_BADGE = {
  '🔥E': { cls: 'badge-essential', label: '🔥 Essential' },
  '⭐R': { cls: 'badge-recommended', label: '⭐ Recommended' },
  '🌘D': { cls: 'badge-dense', label: '🌘 Dense' },
  '⚠️A': { cls: 'badge-harsh', label: '⚠️ Harsh' },
  '🌀X': { cls: 'badge-optional', label: '🌀 Optional' },
}

function ratingColor(r) {
  if (!r) return '#888'
  if (r >= 4.6) return '#f1c40f'
  if (r >= 4.4) return '#e67e22'
  if (r >= 4.0) return '#27ae60'
  return '#7f8c8d'
}

export default function ListPage() {
  const [data, setData] = useState([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState('')
  const [collapsed, setCollapsed] = useState({})

  useEffect(() => {
    getFullList()
      .then(setData)
      .finally(() => setLoading(false))
  }, [])

  const toggle = (id) => setCollapsed(c => ({ ...c, [id]: !c[id] }))

  const filtered = filter.trim()
    ? data.map(cat => ({
        ...cat,
        artists: cat.artists
          .map(a => ({
            ...a,
            albums: a.albums.filter(al =>
              al.title.toLowerCase().includes(filter.toLowerCase())
            )
          }))
          .filter(a =>
            a.name.toLowerCase().includes(filter.toLowerCase()) || a.albums.length > 0
          )
      })).filter(cat => cat.artists.length > 0)
    : data

  if (loading) return <div><span className="spinner" /> Se incarca lista...</div>

  if (!data.length) return (
    <div>
      <div className="page-title">Lista</div>
      <div className="alert alert-info">
        Lista este goala. Mergi la <strong>Import</strong> pentru a importa datele din Google Docs.
      </div>
    </div>
  )

  return (
    <div>
      <div style={{ display: 'flex', alignItems: 'center', gap: 16, marginBottom: 20 }}>
        <div className="page-title" style={{ margin: 0 }}>Lista</div>
        <input
          style={{ maxWidth: 280 }}
          placeholder="Cauta artist sau album..."
          value={filter}
          onChange={e => setFilter(e.target.value)}
        />
      </div>

      {filtered.map(cat => (
        <div key={cat.id} style={{ marginBottom: 28 }}>
          <div
            style={{
              cursor: 'pointer',
              borderBottom: '2px solid var(--accent)',
              paddingBottom: 6,
              marginBottom: 16,
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center'
            }}
            onClick={() => toggle(cat.id)}
          >
            <div>
              <div style={{ fontSize: 13, fontWeight: 800, letterSpacing: 1, color: '#e74c3c', textTransform: 'uppercase' }}>
                {cat.name}
              </div>
              {cat.description && (
                <div style={{ fontSize: 12, color: 'var(--text-muted)', fontStyle: 'italic', marginTop: 2 }}>
                  {cat.description}
                </div>
              )}
            </div>
            <span style={{ color: 'var(--text-muted)', fontSize: 12 }}>
              {cat.artists.length} artisti {collapsed[cat.id] ? '▶' : '▼'}
            </span>
          </div>

          {!collapsed[cat.id] && cat.artists.map(artist => (
            <div key={artist.id} className="card" style={{ marginBottom: 10 }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 10 }}>
                <div>
                  <span style={{ fontWeight: 700, fontSize: 15, color: '#e8e8e8' }}>{artist.name}</span>
                  {artist.description && (
                    <span style={{ color: 'var(--text-muted)', fontSize: 12, marginLeft: 10 }}>
                      — {artist.description}
                    </span>
                  )}
                </div>
                <span style={{ fontSize: 11, color: 'var(--text-muted)' }}>{artist.albums.length} albume</span>
              </div>

              <div>
                {artist.albums.map(album => {
                  const iconInfo = ICON_BADGE[album.icon]
                  return (
                    <div
                      key={album.id}
                      style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: 10,
                        padding: '5px 0',
                        borderBottom: '1px solid var(--border)',
                        fontSize: 13,
                      }}
                    >
                      <span style={{ color: 'var(--text-muted)', width: 34, textAlign: 'right', flexShrink: 0 }}>
                        {album.year || '—'}
                      </span>
                      <span style={{ flex: 1, fontWeight: 500 }}>{album.title}</span>
                      {iconInfo && (
                        <span className={`badge ${iconInfo.cls}`}>{iconInfo.label}</span>
                      )}
                      {album.rating && (
                        <span style={{ fontWeight: 700, color: ratingColor(album.rating), minWidth: 30 }}>
                          ★{album.rating.toFixed(1)}
                        </span>
                      )}
                      {album.description && (
                        <span style={{ color: 'var(--text-muted)', fontSize: 12, maxWidth: 300 }}>
                          {album.description}
                        </span>
                      )}
                    </div>
                  )
                })}
              </div>
            </div>
          ))}
        </div>
      ))}
    </div>
  )
}
