import { API_BASE } from './client'

export async function login(payload: { email: string; password: string }){
  const form = new URLSearchParams()
  form.append('username', payload.email)
  form.append('password', payload.password)
  form.append('grant_type', '')
  const res = await fetch(API_BASE + '/auth/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: form.toString(),
  })
  if(!res.ok){
    const body = await res.json().catch(()=>({ detail: res.statusText }))
    throw new Error(body.detail || 'Login failed')
  }
  const body = await res.json()
  sessionStorage.setItem('token', body.access_token)
  return body
}

export function logout(){
  sessionStorage.removeItem('token')
}
