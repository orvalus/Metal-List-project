import React, { useEffect, useState } from 'react'
import {
  getCategories, createCategory, updateCategory, deleteCategory,
  getArtists, createArtist, updateArtist, deleteArtist,
  getAlbums, createAlbum, updateAlbum, deleteAlbum,
} from '../api'

const ICONS = ['🔥E', '⭐R', '🌘D', '⚠️A', '🌀X']

function Modal({ title, onClose, children }) {
  return (
    <div style={{
      position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.7)',
      display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 200
    }}>
      <div style={{
        background: 'var(--surface)', border: '1px solid var(--border)',
        borderRadius: 8, padding: 24, width: 460, maxHeight: '80vh', overflowY: 'auto'
      }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
          <strong>{title}</strong>
          <button className="btn-secondary btn-sm" onClick={onClose}>✕</button>
        </div>
        {children}
      </div>
    </div>
  )
}

// ── Category Form ──────────────────────────────────────
function CategoryForm({ initial, onSave, onClose }) {
  const [name, setName] = useState(initial?.name || '')
  const [desc, setDesc] = useState(initial?.description || '')
  const [order, setOrder] = useState(initial?.sort_order ?? 0)
  const [loading, setLoading] = useState(false)

  const save = async () => {
    setLoading(true)
    try {
      await onSave({ name, description: desc || null, sort_order: Number(order) })
      onClose()
    } finally { setLoading(false) }
  }

  return (
    <>
      <div className="form-group"><label>Name</label><input value={name} onChange={e => setName(e.target.value)} /></div>
      <div className="form-group"><label>Description</label><input value={desc} onChange={e => setDesc(e.target.value)} /></div>
      <div className="form-group"><label>Order</label><input type="number" value={order} onChange={e => setOrder(e.target.value)} /></div>
      <div className="row">
        <button className="btn-primary" onClick={save} disabled={loading || !name.trim()}>
          {loading ? <span className="spinner" /> : null} Save
        </button>
        <button className="btn-secondary" onClick={onClose}>Cancel</button>
      </div>
    </>
  )
}

// ── Artist Form ────────────────────────────────────────
function ArtistForm({ initial, categories, onSave, onClose }) {
  const [name, setName] = useState(initial?.name || '')
  const [desc, setDesc] = useState(initial?.description || '')
  const [catId, setCatId] = useState(initial?.category_id || categories[0]?.id || '')
  const [order, setOrder] = useState(initial?.sort_order ?? 0)
  const [loading, setLoading] = useState(false)

  const save = async () => {
    setLoading(true)
    try {
      await onSave({ name, description: desc || null, sort_order: Number(order), category_id: Number(catId) })
      onClose()
    } finally { setLoading(false) }
  }

  return (
    <>
      <div className="form-group">
        <label>Category</label>
        <select value={catId} onChange={e => setCatId(e.target.value)}>
          {categories.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
        </select>
      </div>
      <div className="form-group"><label>Artist name</label><input value={name} onChange={e => setName(e.target.value)} /></div>
      <div className="form-group"><label>Description</label><input value={desc} onChange={e => setDesc(e.target.value)} /></div>
      <div className="form-group"><label>Order</label><input type="number" value={order} onChange={e => setOrder(e.target.value)} /></div>
      <div className="row">
        <button className="btn-primary" onClick={save} disabled={loading || !name.trim()}>
          {loading ? <span className="spinner" /> : null} Save
        </button>
        <button className="btn-secondary" onClick={onClose}>Cancel</button>
      </div>
    </>
  )
}

// ── Album Form ─────────────────────────────────────────
function AlbumForm({ initial, artists, onSave, onClose }) {
  const [title, setTitle] = useState(initial?.title || '')
  const [year, setYear] = useState(initial?.year || '')
  const [icon, setIcon] = useState(initial?.icon || '')
  const [rating, setRating] = useState(initial?.rating || '')
  const [desc, setDesc] = useState(initial?.description || '')
  const [artistId, setArtistId] = useState(initial?.artist_id || artists[0]?.id || '')
  const [order, setOrder] = useState(initial?.sort_order ?? 0)
  const [loading, setLoading] = useState(false)

  const save = async () => {
    setLoading(true)
    try {
      await onSave({
        title,
        year: year ? Number(year) : null,
        icon: icon || null,
        rating: rating ? Number(rating) : null,
        description: desc || null,
        sort_order: Number(order),
        artist_id: Number(artistId),
      })
      onClose()
    } finally { setLoading(false) }
  }

  return (
    <>
      <div className="form-group">
        <label>Artist</label>
        <select value={artistId} onChange={e => setArtistId(e.target.value)}>
          {artists.map(a => <option key={a.id} value={a.id}>{a.name}</option>)}
        </select>
      </div>
      <div className="form-group"><label>Album title</label><input value={title} onChange={e => setTitle(e.target.value)} /></div>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 8 }}>
        <div className="form-group"><label>Year</label><input type="number" value={year} onChange={e => setYear(e.target.value)} /></div>
        <div className="form-group">
          <label>Rating (0-5)</label>
          <input type="number" step="0.1" min="0" max="5" value={rating} onChange={e => setRating(e.target.value)} />
        </div>
      </div>
      <div className="form-group">
        <label>Icon</label>
        <select value={icon} onChange={e => setIcon(e.target.value)}>
          <option value="">— No icon —</option>
          {ICONS.map(i => <option key={i} value={i}>{i}</option>)}
        </select>
      </div>
      <div className="form-group"><label>Short description</label><input value={desc} onChange={e => setDesc(e.target.value)} /></div>
      <div className="form-group"><label>Order</label><input type="number" value={order} onChange={e => setOrder(e.target.value)} /></div>
      <div className="row">
        <button className="btn-primary" onClick={save} disabled={loading || !title.trim()}>
          {loading ? <span className="spinner" /> : null} Save
        </button>
        <button className="btn-secondary" onClick={onClose}>Cancel</button>
      </div>
    </>
  )
}

// ── Main Page ──────────────────────────────────────────
export default function ManagePage() {
  const [categories, setCategories] = useState([])
  const [artists, setArtists] = useState([])
  const [albums, setAlbums] = useState([])
  const [tab, setTab] = useState('albums')
  const [modal, setModal] = useState(null) // { type, item? }
  const [loading, setLoading] = useState(true)
  const [filterArtist, setFilterArtist] = useState('')
  const [filterCat, setFilterCat] = useState('')

  const reload = async () => {
    setLoading(true)
    const [cats, arts, albs] = await Promise.all([getCategories(), getArtists(), getAlbums()])
    setCategories(cats)
    setArtists(arts)
    setAlbums(albs)
    setLoading(false)
  }

  useEffect(() => { reload() }, [])

  const closeModal = () => setModal(null)

  // ── Delete handlers ──
  const delCategory = async (id) => {
    if (!confirm('Delete this category and all its artists/albums?')) return
    await deleteCategory(id)
    reload()
  }

  const delArtist = async (id) => {
    if (!confirm('Delete this artist and all their albums?')) return
    await deleteArtist(id)
    reload()
  }

  const delAlbum = async (id) => {
    if (!confirm('Delete this album?')) return
    await deleteAlbum(id)
    reload()
  }

  // ── Save handlers ──
  const saveCategory = async (data) => {
    if (modal.item) await updateCategory(modal.item.id, data)
    else await createCategory(data)
    reload()
  }

  const saveArtist = async (data) => {
    if (modal.item) await updateArtist(modal.item.id, data)
    else await createArtist(data)
    reload()
  }

  const saveAlbum = async (data) => {
    if (modal.item) await updateAlbum(modal.item.id, data)
    else await createAlbum(data)
    reload()
  }

  // ── Filtered data ──
  const filteredArtists = artists.filter(a =>
    (!filterCat || a.category_id === Number(filterCat)) &&
    a.name.toLowerCase().includes(filterArtist.toLowerCase())
  )

  const filteredAlbums = albums.filter(al => {
    const artist = artists.find(a => a.id === al.artist_id)
    return (
      (!filterArtist || artist?.name.toLowerCase().includes(filterArtist.toLowerCase())) &&
      (!filterCat || artist?.category_id === Number(filterCat))
    )
  })

  const getCatName = (id) => categories.find(c => c.id === id)?.name || '—'
  const getArtistName = (id) => artists.find(a => a.id === id)?.name || '—'

  if (loading) return <div><span className="spinner" /> Loading...</div>

  return (
    <div>
      <div style={{ display: 'flex', alignItems: 'center', gap: 16, marginBottom: 20, flexWrap: 'wrap' }}>
        <div className="page-title" style={{ margin: 0 }}>Management</div>
        <div className="row" style={{ gap: 0 }}>
          {[['albums', 'Albums'], ['artists', 'Artists'], ['categories', 'Categories']].map(([t, label]) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              style={{
                background: tab === t ? 'var(--accent)' : 'var(--surface2)',
                color: tab === t ? '#fff' : 'var(--text-muted)',
                border: '1px solid var(--border)',
                borderRadius: t === 'albums' ? '6px 0 0 6px' : t === 'categories' ? '0 6px 6px 0' : '0',
              }}
            >{label}</button>
          ))}
        </div>
      </div>

      {/* Filters */}
       {tab !== 'categories' && (
         <div className="row" style={{ marginBottom: 16, flexWrap: 'wrap' }}>
           <select
             style={{ width: 200 }}
             value={filterCat}
             onChange={e => setFilterCat(e.target.value)}
           >
             <option value="">All categories</option>
             {categories.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
           </select>
           {tab === 'albums' && (
             <input
               style={{ width: 200 }}
               placeholder="Filter by artist..."
               value={filterArtist}
               onChange={e => setFilterArtist(e.target.value)}
             />
           )}
         </div>
       )}

       {/* ── CATEGORIES ── */}
       {tab === 'categories' && (
         <>
           <button className="btn-primary" style={{ marginBottom: 12 }} onClick={() => setModal({ type: 'category' })}>
             + Add category
           </button>
          {categories.map(cat => (
            <div key={cat.id} className="card" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div>
                <strong style={{ textTransform: 'uppercase', fontSize: 13, color: 'var(--accent2)' }}>{cat.name}</strong>
                {cat.description && <div style={{ fontSize: 12, color: 'var(--text-muted)', fontStyle: 'italic' }}>{cat.description}</div>}
              </div>
               <div className="row">
                 <button className="btn-secondary btn-sm" onClick={() => setModal({ type: 'category', item: cat })}>Edit</button>
                 <button className="btn-danger btn-sm" onClick={() => delCategory(cat.id)}>Delete</button>
               </div>
            </div>
          ))}
        </>
      )}

       {/* ── ARTISTS ── */}
       {tab === 'artists' && (
         <>
           <button className="btn-primary" style={{ marginBottom: 12 }} onClick={() => setModal({ type: 'artist' })}>
             + Add artist
           </button>
          {filteredArtists.map(artist => (
            <div key={artist.id} className="card" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div>
                <strong>{artist.name}</strong>
                <span style={{ fontSize: 12, color: 'var(--text-muted)', marginLeft: 10 }}>
                  {getCatName(artist.category_id)}
                </span>
                {artist.description && (
                  <div style={{ fontSize: 12, color: 'var(--text-muted)', fontStyle: 'italic' }}>{artist.description}</div>
                )}
              </div>
               <div className="row">
                 <button className="btn-secondary btn-sm" onClick={() => setModal({ type: 'artist', item: artist })}>Edit</button>
                 <button className="btn-danger btn-sm" onClick={() => delArtist(artist.id)}>Delete</button>
               </div>
             </div>
           ))}
         </>
       )}

       {/* ── ALBUMS ── */}
       {tab === 'albums' && (
         <>
           <button className="btn-primary" style={{ marginBottom: 12 }} onClick={() => setModal({ type: 'album' })}>
             + Add album
           </button>
          {filteredAlbums.map(album => (
            <div key={album.id} className="card" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: 12 }}>
              <div style={{ flex: 1 }}>
                <div className="row" style={{ flexWrap: 'wrap', gap: 8 }}>
                  <strong>{album.title}</strong>
                  {album.year && <span style={{ color: 'var(--text-muted)', fontSize: 12 }}>({album.year})</span>}
                  {album.icon && <span style={{ fontSize: 13 }}>{album.icon}</span>}
                  {album.rating && <span style={{ color: '#f1c40f', fontWeight: 700, fontSize: 13 }}>★{album.rating.toFixed(1)}</span>}
                  <span style={{ fontSize: 12, color: 'var(--text-muted)' }}>— {getArtistName(album.artist_id)}</span>
                </div>
                {album.description && (
                  <div style={{ fontSize: 12, color: 'var(--text-muted)', marginTop: 2 }}>{album.description}</div>
                )}
              </div>
               <div className="row">
                 <button className="btn-secondary btn-sm" onClick={() => setModal({ type: 'album', item: album })}>Edit</button>
                 <button className="btn-danger btn-sm" onClick={() => delAlbum(album.id)}>Delete</button>
               </div>
            </div>
          ))}
        </>
      )}

       {/* ── Modals ── */}
       {modal?.type === 'category' && (
         <Modal title={modal.item ? 'Edit category' : 'Add category'} onClose={closeModal}>
           <CategoryForm initial={modal.item} onSave={saveCategory} onClose={closeModal} />
         </Modal>
       )}
       {modal?.type === 'artist' && (
         <Modal title={modal.item ? 'Edit artist' : 'Add artist'} onClose={closeModal}>
           <ArtistForm initial={modal.item} categories={categories} onSave={saveArtist} onClose={closeModal} />
         </Modal>
       )}
       {modal?.type === 'album' && (
         <Modal title={modal.item ? 'Edit album' : 'Add album'} onClose={closeModal}>
           <AlbumForm initial={modal.item} artists={artists} onSave={saveAlbum} onClose={closeModal} />
         </Modal>
       )}
    </div>
  )
}
