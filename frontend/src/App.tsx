import React from 'react'
import { Routes, Route } from 'react-router-dom'
import Home from './pages/Home'
import Login from './pages/Login'
import Customers from './pages/Customers'
import Transactions from './pages/Transactions'
import NavBar from './components/NavBar'
import RequireAuth from './components/RequireAuth'

export default function App() {
  return (
    <div>
      <NavBar />
      <main style={{ padding: 20 }}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
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
        </Routes>
      </main>
    </div>
  )
}
