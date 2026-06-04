import React, { useEffect, useState } from 'react'
import { deleteCustomer, listCustomers } from '../api/customers'
import CustomerForm from '../components/CustomerForm'
import CustomerList from '../components/CustomerList'

export default function Customers() {
  const [items, setItems] = useState<any[]>([])
  const [editing, setEditing] = useState<any | null>(null)

  async function refresh(){
    const r = await listCustomers()
    setItems(r || [])
  }

  useEffect(() => {
    refresh()
  }, [])

  async function handleDelete(id:string){
    await deleteCustomer(id)
    refresh()
  }

  function handleEdit(item:any){
    setEditing(item)
  }

  function handleSaved(){
    setEditing(null)
    refresh()
  }

  return (
    <div className="container">
      <h2>Customers</h2>
      <CustomerForm customer={editing || undefined} onSaved={handleSaved} onCancel={() => setEditing(null)} />
      <CustomerList items={items} onEdit={handleEdit} onDelete={handleDelete} />
    </div>
  )
}
