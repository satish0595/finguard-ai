import { request } from './client'

export async function listCustomers(){
  const data = await request('/customers')
  return data?.items || []
}

export async function getCustomer(id:string){
  return await request(`/customers/${id}`)
}
