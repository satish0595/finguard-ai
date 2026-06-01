import React, { createContext, useContext, useEffect, useState, useCallback } from 'react'
import { login as apiLogin } from '../api/auth'
import { API_BASE } from '../api/client'

type AuthContextType = {
  token: string | null
  user: any | null
  isAuthenticated: boolean
  login: (email:string, password:string)=>Promise<void>
  logout: ()=>void
  refresh: ()=>Promise<boolean>
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

function parseJwt(token:string){
  try{
    const payload = token.split('.')[1]
    const padded = payload.padEnd(payload.length + (4 - (payload.length % 4))%4, '=')
    const json = atob(padded)
    return JSON.parse(json)
  }catch{
    return null
  }
}

export function AuthProvider({ children }:{ children: React.ReactNode }){
  const [token, setToken] = useState<string | null>(()=>sessionStorage.getItem('token'))
  const [user, setUser] = useState<any | null>(()=>{
    const t = sessionStorage.getItem('token')
    if(!t) return null
    return parseJwt(t)
  })
  const [timerId, setTimerId] = useState<number | null>(null)

  const logout = useCallback(()=>{
    sessionStorage.removeItem('token')
    setToken(null)
    setUser(null)
    if(timerId) window.clearTimeout(timerId)
  }, [timerId])

  const scheduleAutoLogout = useCallback((tkn:string)=>{
    const payload = parseJwt(tkn)
    if(!payload || !payload.exp){
      return
    }
    const ms = payload.exp * 1000 - Date.now()
    if(ms <= 0){
      logout()
      return
    }
    const id = window.setTimeout(()=>{
      logout()
    }, ms)
    setTimerId(id)
  }, [logout])

  useEffect(()=>{
    if(token){
      const p = parseJwt(token)
      setUser(p)
      scheduleAutoLogout(token)
    }
  }, [token, scheduleAutoLogout])

  async function login(email:string, password:string){
    const body = await apiLogin({ email, password })
    if(body?.access_token){
      sessionStorage.setItem('token', body.access_token)
      setToken(body.access_token)
      const p = parseJwt(body.access_token)
      setUser(p)
      scheduleAutoLogout(body.access_token)
    }
  }

  async function refresh(){
    const t = sessionStorage.getItem('token')
    if(!t) return false
    try{
      const res = await fetch(API_BASE + '/auth/refresh', { method: 'POST', headers: { Authorization: `Bearer ${t}` } })
      if(!res.ok) return false
      const body = await res.json()
      if(body?.access_token){
        sessionStorage.setItem('token', body.access_token)
        setToken(body.access_token)
        setUser(parseJwt(body.access_token))
        scheduleAutoLogout(body.access_token)
        return true
      }
    }catch{}
    return false
  }

  return (
    <AuthContext.Provider value={{ token, user, isAuthenticated: !!token, login, logout, refresh }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth(){
  const ctx = useContext(AuthContext)
  if(!ctx) throw new Error('useAuth must be used within AuthProvider')
  return ctx
}
