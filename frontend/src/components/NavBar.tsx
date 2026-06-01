import React from 'react'
import { Link } from 'react-router-dom'

export default function NavBar(){
  return (
    <nav>
      <div className="container">
        <Link to="/">Home</Link>
        <Link to="/customers">Customers</Link>
        <Link to="/transactions">Transactions</Link>
        <Link to="/login">Login</Link>
      </div>
    </nav>
  )
}
