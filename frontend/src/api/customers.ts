import { request } from './client'

export async function listCustomers(){
  const data = await request('/customers')
  return data?.items || []
}

export async function getCustomer(id:string){
  return await request(`/customers/${id}`)
}

export async function createCustomer(payload: any){
  return await request('/customers', { method: 'POST', body: JSON.stringify(payload) })
}

export async function updateCustomer(id:string, payload:any){
  return await request(`/customers/${id}`, { method: 'PATCH', body: JSON.stringify(payload) })
}

export async function deleteCustomer(id:string){
  return await request(`/customers/${id}`, { method: 'DELETE' })
}
