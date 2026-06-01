import { request } from './client'

export async function login(payload: { email:string, password:string }){
  const body = await request('/users', { method:'GET' })
  // placeholder: backend auth not implemented; in real app call /auth/token
  // store dummy token for now
  sessionStorage.setItem('token', 'stub-token')
  return body
}

export function logout(){
  sessionStorage.removeItem('token')
}
