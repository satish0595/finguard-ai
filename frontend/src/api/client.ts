const API_BASE = import.meta.env.VITE_API_BASE || '/api/v1'

async function request(path: string, opts: RequestInit = {}){
  const headers: Record<string,string> = { 'Content-Type':'application/json', ...(opts.headers || {}) as any }
  const token = sessionStorage.getItem('token')
  if(token) headers['Authorization'] = `Bearer ${token}`
  const res = await fetch(API_BASE + path, { ...opts, headers })
  if(res.status === 204) return null
  const body = await res.json().catch(()=>null)
  if(!res.ok) throw new Error(body?.detail || res.statusText)
  return body
}

export { API_BASE, request }
