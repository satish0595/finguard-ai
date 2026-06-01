import { request } from './client'

export async function listTransactions(){
  const data = await request('/transactions')
  return data?.items || []
}

export async function getTransaction(id:string){
  return await request(`/transactions/${id}`)
}
