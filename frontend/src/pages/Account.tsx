import React, { useMemo } from 'react'
import { useAuth } from '../context/AuthContext'

function formatExpiry(exp?: number) {
  if (!exp) return 'Unknown'
  return new Date(exp * 1000).toLocaleString()
}

export default function Account() {
  const auth = useAuth()
  const expiry = useMemo(() => auth.user?.exp, [auth.user])

  return (
    <div className="container">
      <h2>Account</h2>
      <p><strong>Email:</strong> {auth.user?.email || 'Unknown'}</p>
      <p><strong>Token expires at:</strong> {formatExpiry(expiry)}</p>
      <p><strong>Authenticated:</strong> {auth.isAuthenticated ? 'Yes' : 'No'}</p>
      <button className="button" onClick={auth.refresh}>Refresh token</button>
    </div>
  )
}
