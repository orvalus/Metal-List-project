import { Routes, Route, NavLink } from 'react-router-dom'
import ListPage from './pages/ListPage'
import ManagePage from './pages/ManagePage'
import ImportPage from './pages/ImportPage'
import AuditPage from './pages/AuditPage'
import './App.css'

export default function App() {
  return (
    <div className="app">
      <header className="header">
        <span className="logo">🤘 Metal List</span>
        <nav className="nav">
          <NavLink to="/">Lista</NavLink>
          <NavLink to="/manage">Management</NavLink>
          <NavLink to="/import">Import</NavLink>
          <NavLink to="/audit">Audit</NavLink>
        </nav>
      </header>
      <main className="main">
        <Routes>
          <Route path="/" element={<ListPage />} />
          <Route path="/manage" element={<ManagePage />} />
          <Route path="/import" element={<ImportPage />} />
          <Route path="/audit" element={<AuditPage />} />
        </Routes>
      </main>
    </div>
  )
}
