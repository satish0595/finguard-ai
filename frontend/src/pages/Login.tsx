import React, { useEffect } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import LoginForm from '../components/LoginForm'
import { useAuth } from '../context/AuthContext'

export default function Login() {
  const auth = useAuth()
  const navigate = useNavigate()
  const location = useLocation()
  const from = (location.state as any)?.from?.pathname || '/'

  useEffect(() => {
    if (auth.isAuthenticated) {
      navigate(from, { replace: true })
    }
  }, [auth.isAuthenticated, from, navigate])

  return (
    <div className="container">
      <h2>Login</h2>
      <LoginForm onSuccess={() => navigate(from, { replace: true })} />
      <p style={{marginTop: 16}}>
        Don't have an account? <a href="/signup">Sign up here</a>
      </p>
    </div>
  )
}
