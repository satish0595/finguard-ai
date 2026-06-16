import React from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function Home() {
  const auth = useAuth()

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
