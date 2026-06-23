import React, { useEffect } from 'react'
import { Routes, Route, useLocation } from 'react-router-dom'
import Home from './pages/Home'
import Login from './pages/Login'
import Signup from './pages/Signup'
import Customers from './pages/Customers'
import Transactions from './pages/Transactions'
import Account from './pages/Account'
import NavBar from './components/NavBar'
import RequireAuth from './components/RequireAuth'

function ScrollToTop() {
  const { pathname } = useLocation()

  useEffect(() => {
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }, [pathname])

  return null
}

export default function App() {
  return (
    <div>
      <div
        style={{
          background: '#2563eb',
          color: 'white',
          padding: '8px 16px',
          textAlign: 'center',
          fontSize: '14px',
          fontWeight: 600,
        }}
      >
        ✨ Small update: minor UI polish deployed.
      </div>
      <NavBar />
      <main style={{ padding: 20 }}>
        <ScrollToTop />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
          <Route
            path="/customers"
            element={
              <RequireAuth>
                <Customers />
              </RequireAuth>
            }
          />
          <Route
            path="/transactions"
            element={
              <RequireAuth>
                <Transactions />
              </RequireAuth>
            }
          />
          <Route
            path="/account"
            element={
              <RequireAuth>
                <Account />
              </RequireAuth>
            }
          />
          <Route
            path="*"
            element={<div style={{ paddingTop: 24 }}>Page not found. Go back home to continue.</div>}
          />
        </Routes>
      </main>
    </div>
  )
}
