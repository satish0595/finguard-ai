import { request } from './client'

export async function listTransactions(){
  const data = await request('/transactions')
  return data?.items || []
}

export async function getTransaction(id:string){
  return await request(`/transactions/${id}`)
}

export async function createTransaction(payload: any){
  return await request('/transactions', { method: 'POST', body: JSON.stringify(payload) })
}

export async function updateTransaction(id:string, payload:any){
  return await request(`/transactions/${id}`, { method: 'PUT', body: JSON.stringify(payload) })
}
