import React from 'react'
import { useNavigate } from 'react-router-dom'
import SignupForm from '../components/SignupForm'

export default function Signup() {
  const navigate = useNavigate()

  return (
    <div className="container">
      <h2>Create Account</h2>
      <SignupForm onSuccess={() => navigate('/login')} />
      <p style={{marginTop: 16}}>
        Already have an account? <a href="/login">Login here</a>
      </p>
    </div>
  )
}
