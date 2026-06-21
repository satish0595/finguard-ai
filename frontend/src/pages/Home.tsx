import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { getDashboardSummary, type DashboardSummary } from '../api/dashboard'
import { useAuth } from '../context/AuthContext'

export default function Home() {
  const auth = useAuth()
  const [summary, setSummary] = useState<DashboardSummary | null>(null)
  const [summaryError, setSummaryError] = useState<string | null>(null)
  const [isRefreshing, setIsRefreshing] = useState(false)
  const [lastUpdated, setLastUpdated] = useState<string | null>(null)

  const loadSummary = async () => {
    setIsRefreshing(true)

    try {
      const data = await getDashboardSummary()
      setSummary(data)
      setSummaryError(null)
      setLastUpdated(new Date().toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' }))
    } catch (error: unknown) {
      setSummaryError(error instanceof Error ? error.message : 'Unable to load stats')
    } finally {
      setIsRefreshing(false)
    }
  }

  useEffect(() => {
    void loadSummary()
  }, [])

  return (
    <div className="home-page">
      <section className="hero">
        <div className="hero-copy">
          <span className="hero-badge">AI-powered fraud monitoring</span>
          <h1>See risk faster and act with confidence.</h1>
          <p>
            FinGuard AI brings customers, transactions, and alerts into one calm workspace so your team can review suspicious activity without the noise.
          </p>
          <div className="cta-row">
            {auth.isAuthenticated ? (
              <Link className="button primary" to="/customers">
                Open dashboard
              </Link>
            ) : (
              <>
                <Link className="button primary" to="/signup">
                  Create account
                </Link>
                <Link className="button secondary" to="/login">
                  Sign in
                </Link>
              </>
            )}
          </div>
        </div>

        <div className="hero-panel">
          <h3>What you can do</h3>
          <ul>
            <li>Review customer risk profiles in seconds</li>
            <li>Spot unusual transaction patterns early</li>
            <li>Keep alerts and follow-ups organized</li>
          </ul>
        </div>
      </section>

      <section className="feature-grid">
        <article className="card">
          <h3>👤 Customer insight</h3>
          <p>Keep customer details, history, and investigations in one accessible place.</p>
        </article>
        <article className="card">
          <h3>💳 Transaction review</h3>
          <p>Track high-risk movements and review the context behind each event quickly.</p>
        </article>
        <article className="card">
          <h3>⚠️ Alert workflow</h3>
          <p>Move from alert to case management with a simple, focused workflow.</p>
        </article>
      </section>

      <section className="summary-strip">
        <div className="summary-heading-row">
          <div className="summary-heading">
            <h3>Live platform snapshot</h3>
            <p>A quick read on what the monitoring workspace is tracking right now.</p>
          </div>
          <button
            type="button"
            className="summary-refresh"
            onClick={() => void loadSummary()}
            disabled={isRefreshing}
          >
            {isRefreshing ? 'Refreshing…' : 'Refresh'}
          </button>
        </div>
        {summary ? (
          <>
          <div className="summary-grid">
            <article className="summary-item">
              <span>Customers</span>
              <strong>{summary.customers_total}</strong>
            </article>
            <article className="summary-item">
              <span>High-risk</span>
              <strong>{summary.customers_high_risk}</strong>
            </article>
            <article className="summary-item">
              <span>Pending review</span>
              <strong>{summary.customers_pending_review}</strong>
            </article>
            <article className="summary-item">
              <span>Open alerts</span>
              <strong>{summary.open_alerts}</strong>
            </article>
            <article className="summary-item">
              <span>Critical alerts</span>
              <strong>{summary.critical_alerts}</strong>
            </article>
            <article className="summary-item">
              <span>Open cases</span>
              <strong>{summary.open_cases}</strong>
            </article>
            <article className="summary-item">
              <span>Urgent cases</span>
              <strong>{summary.urgent_cases}</strong>
            </article>
          </div>
          <div className="summary-meta">
            Last updated {lastUpdated ? `at ${lastUpdated}` : 'just now'}
          </div>
          </>
        ) : (
          <div className="summary-fallback">
            <span>{summaryError || 'Loading snapshot...'}</span>
          </div>
        )}
      </section>

      <section className="status-card">
        {auth.isAuthenticated ? (
          <>
            <strong>Signed in as:</strong> {auth.user?.email}
          </>
        ) : (
          <>
            Sign in to unlock customer and transaction workflows.
          </>
        )}
      </section>
    </div>
  )
}
