const API_BASE = import.meta.env.VITE_API_BASE || '/api/v1'

async function tryRefreshToken(token: string){
  try{
    const res = await fetch(API_BASE + '/auth/refresh', { method: 'POST', headers: { Authorization: `Bearer ${token}` } })
    if(!res.ok) return null
    const body = await res.json()
    if(body?.access_token){
      sessionStorage.setItem('token', body.access_token)
      return body.access_token
    }
    return null
  }catch{
    return null
  }
}

async function request(path: string, opts: RequestInit = {}){
  const token = sessionStorage.getItem('token')
  const headers: Record<string,string> = { 'Content-Type':'application/json', ...(opts.headers || {}) as any }
  if(token) headers['Authorization'] = `Bearer ${token}`

  let res = await fetch(API_BASE + path, { ...opts, headers })

  if(res.status === 401 && token){
    const newToken = await tryRefreshToken(token)
    if(newToken){
      headers['Authorization'] = `Bearer ${newToken}`
      res = await fetch(API_BASE + path, { ...opts, headers })
    }
  }

  if(res.status === 204) return null
  const body = await res.json().catch(()=>null)
  if(!res.ok) throw new Error(body?.detail || res.statusText)
  return body
}

export { API_BASE, request }
