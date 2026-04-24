// Audit functionality disabled - no external connections allowed

export default function AuditPage() {
  return (
    <div>
      <div className="page-title">Sputnikmusic Audit</div>

      <div className="alert alert-error" style={{ marginBottom: 20 }}>
        <strong>Audit Functionality Disabled</strong>
        <p style={{ marginTop: 8, marginBottom: 0 }}>
          The Sputnikmusic audit feature has been disabled to prevent external connections.
          No data is being sent to or retrieved from Sputnikmusic.
        </p>
      </div>

      <div className="card" style={{ maxWidth: 500, marginBottom: 20, pointerEvents: 'none' }}>
         <div className="form-group">
            <label>Filter by category (disabled)</label>
            <select disabled>
              <option value="">All categories</option>
            </select>
          </div>
          <div className="form-group">
            <label>Select artist to audit (disabled)</label>
            <select disabled>
              <option value="">— Select artist —</option>
            </select>
          </div>
          <button
            className="btn-primary"
            disabled
          >
            Run Audit (disabled)
          </button>
        </div>
    </div>
  )
}
