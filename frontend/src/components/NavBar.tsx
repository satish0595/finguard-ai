import React from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function NavBar(){
  const auth = useAuth()
  return (
    <nav>
      <div className="container">
        <Link to="/">Home</Link>
        <Link to="/customers">Customers</Link>
        <Link to="/transactions">Transactions</Link>
        {auth.isAuthenticated ? (
          <>
            <Link to="/account">Account</Link>
            <span style={{marginLeft:8}}>{auth.user?.email}</span>
            <button style={{marginLeft:8}} onClick={auth.logout}>Logout</button>
          </>
        ) : (
          <>
            <Link to="/login">Login</Link>
            <Link to="/signup">Sign Up</Link>
          </>
        )}
      </div>
    </nav>
  )
}
