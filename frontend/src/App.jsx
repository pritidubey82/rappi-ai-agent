import { useState } from 'react';
import './App.css';

export default function App() {
  const [sku, setSku] = useState('SKU-101');
  const [supplierId, setSupplierId] = useState('SUPP-01');
  const [quantity, setQuantity] = useState(800);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const handleEvaluate = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setResult(null);

    try {
      const response = await fetch('http://127.0.0.1:8000/api/v1/evaluate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          sku,
          supplier_id: supplierId,
          recommended_quantity: parseInt(quantity, 10),
        }),
      });

      if (!response.ok) {
        throw new Error('Backend server non-responsive. Ensure FastAPI is running on port 8000.');
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <h1>Rappi AI Purchasing Agent</h1>
        <p>Autonomous stock & budget validation engine with policy controls</p>
      </header>

      <div className="card">
        <form onSubmit={handleEvaluate}>
          <div className="form-grid">
            <div className="form-group">
              <label>SKU ID</label>
              <input
                type="text"
                className="form-input"
                value={sku}
                onChange={(e) => setSku(e.target.value)}
                required
              />
            </div>

            <div className="form-group">
              <label>Supplier ID</label>
              <input
                type="text"
                className="form-input"
                value={supplierId}
                onChange={(e) => setSupplierId(e.target.value)}
                required
              />
            </div>

            <div className="form-group form-group-full">
              <label>Recommended Purchase Quantity</label>
              <input
                type="number"
                className="form-input"
                value={quantity}
                onChange={(e) => setQuantity(e.target.value)}
                required
              />
            </div>
          </div>

          <button type="submit" className="submit-btn" disabled={loading}>
            {loading ? 'Running Guardrail Checks...' : 'Evaluate Recommendation'}
          </button>
        </form>
      </div>

      {error && (
        <div className="card" style={{ borderLeft: '4px solid var(--danger-color)', color: '#f87171' }}>
          <strong>Error:</strong> {error}
        </div>
      )}

      {result && (
        <div className="card">
          <div className="audit-header">
            <h2>Evaluation & Audit Log</h2>
            <span className={`badge badge-${result.decision}`}>
              {result.decision}
            </span>
          </div>

          <div className="section-title">1. Fact-Finding Findings</div>
          <div className="metrics-grid">
            <div className="metric-card">
              <span className="label">Current Stock</span>
              <span className="value">{result.investigation.current_stock}</span>
            </div>
            <div className="metric-card">
              <span className="label">Available Space</span>
              <span className="value">{result.investigation.available_space}</span>
            </div>
            <div className="metric-card">
              <span className="label">Budget Left</span>
              <span className="value">${result.investigation.available_budget}</span>
            </div>
            <div className="metric-card">
              <span className="label">Supplier MOQ</span>
              <span className="value">{result.investigation.supplier_moq}</span>
            </div>
          </div>

          <div className="section-title">2. Policy Decision Justification</div>
          <div className="reason-box">
            {result.execution_details.reason}
          </div>

          {result.execution_details.purchase_order && (
            <>
              <div className="section-title">3. Executed Action (Generated Purchase Order)</div>
              <div className="json-container">
                <pre>{JSON.stringify(result.execution_details.purchase_order, null, 2)}</pre>
              </div>
            </>
          )}
        </div>
      )}
    </div>
  );
}