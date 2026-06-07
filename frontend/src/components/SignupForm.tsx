import React, { useState } from 'react'
import { register } from '../api/auth'

export default function SignupForm({ onSuccess }: { onSuccess?: () => void }){
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [full_name, setFullName] = useState('')
  const [msg, setMsg] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)

  async function submit(e: React.FormEvent){
    e.preventDefault()
    setError(null)
    try{
      await register({ email, password, full_name })
      setMsg('Account created successfully. You can now login.')
      setEmail('')
      setPassword('')
      setFullName('')
      onSuccess?.()
    }catch(err:any){
      setError(err?.message || 'Signup failed')
    }
  }

  return (
    <form onSubmit={submit} style={{maxWidth:400}}>
      <div>
        <label>Full name</label>
        <input value={full_name} onChange={e=>setFullName(e.target.value)} />
      </div>
      <div>
        <label>Email</label>
        <input type="email" value={email} onChange={e=>setEmail(e.target.value)} required />
      </div>
      <div>
        <label>Password (min 8 chars)</label>
        <input type="password" value={password} onChange={e=>setPassword(e.target.value)} required />
      </div>
      <div>
        <button className="button" type="submit">Create Account</button>
      </div>
      {msg && <div style={{marginTop:10, color:'green'}}>{msg}</div>}
      {error && <div style={{marginTop:10, color:'red'}}>{error}</div>}
    </form>
  )
}
