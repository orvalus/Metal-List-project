import axios from 'axios'

const BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({ baseURL: BASE })

// ── Full list ──────────────────────────────────────────
export const getFullList = () => api.get('/list').then(r => r.data)

// ── Import ─────────────────────────────────────────────
export const importFromUrl = (url, replace = false) =>
  api.post(`/import/url?url=${encodeURIComponent(url)}&replace=${replace}`).then(r => r.data)

export const importFromText = (text, replace = false) =>
  api.post('/import/text', { text, replace }).then(r => r.data)

// ── Categories ─────────────────────────────────────────
export const getCategories = () => api.get('/categories').then(r => r.data)
export const createCategory = (data) => api.post('/categories', data).then(r => r.data)
export const updateCategory = (id, data) => api.patch(`/categories/${id}`, data).then(r => r.data)
export const deleteCategory = (id) => api.delete(`/categories/${id}`)

// ── Artists ────────────────────────────────────────────
export const getArtists = (categoryId) =>
  api.get('/artists', { params: categoryId ? { category_id: categoryId } : {} }).then(r => r.data)
export const createArtist = (data) => api.post('/artists', data).then(r => r.data)
export const updateArtist = (id, data) => api.patch(`/artists/${id}`, data).then(r => r.data)
export const deleteArtist = (id) => api.delete(`/artists/${id}`)

// ── Albums ─────────────────────────────────────────────
export const getAlbums = (artistId) =>
  api.get('/albums', { params: artistId ? { artist_id: artistId } : {} }).then(r => r.data)
export const createAlbum = (data) => api.post('/albums', data).then(r => r.data)
export const updateAlbum = (id, data) => api.patch(`/albums/${id}`, data).then(r => r.data)
export const deleteAlbum = (id) => api.delete(`/albums/${id}`)

// ── Audit (DISABLED) ───────────────────────────────────
// Audit functionality has been disabled to prevent external connections to Sputnikmusic.
// Backend endpoint exists (returns 501 Not Implemented).
// export const auditArtist = (artistId) => api.get(`/audit/${artistId}`).then(r => r.data)
