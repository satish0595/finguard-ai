import React, { useState } from 'react'
import { login } from '../api/auth'

export default function LoginForm(){
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [msg, setMsg] = useState<string | null>(null)

  async function submit(e: React.FormEvent){
    e.preventDefault()
    try{
      await login({ email, password })
      setMsg('Logged in (token stored in sessionStorage)')
    }catch(err:any){
      setMsg(err?.message || 'Login failed')
    }
  }

  return (
    <form onSubmit={submit} style={{maxWidth:400}}>
      <div>
        <label>Email</label>
        <input value={email} onChange={e=>setEmail(e.target.value)} />
      </div>
      <div>
        <label>Password</label>
        <input type="password" value={password} onChange={e=>setPassword(e.target.value)} />
      </div>
      <div>
        <button className="button" type="submit">Login</button>
      </div>
      {msg && <div style={{marginTop:10}}>{msg}</div>}
    </form>
  )
}
