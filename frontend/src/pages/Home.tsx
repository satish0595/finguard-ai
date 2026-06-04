import React from 'react'
import { useAuth } from '../context/AuthContext'

export default function Home() {
  const auth = useAuth()

  return (
    <div className="container">
      <h1>FinGuard AI</h1>
      <p>Welcome — frontend scaffold is ready.</p>
      {auth.isAuthenticated ? (
        <div style={{ marginTop: 16 }}>
          <strong>Signed in as:</strong> {auth.user?.email}
        </div>
      ) : (
        <div style={{ marginTop: 16 }}>
          Please log in to access Customers and Transactions.
        </div>
      )}
    </div>
  )
}
