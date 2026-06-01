import React, { useEffect, useState } from 'react'
import { listCustomers } from '../api/customers'
import CustomerForm from '../components/CustomerForm'

export default function Customers() {
  const [items, setItems] = useState<any[]>([])

  useEffect(() => {
    listCustomers().then(r => setItems(r || []))
  }, [])

  async function refresh(){
    const r = await listCustomers()
    setItems(r || [])
  }

  return (
    <div className="container">
      <h2>Customers</h2>
      <CustomerForm onSaved={refresh} />
      <ul>
        {items.map(c => (
          <li key={c.id}>{c.legal_name} ({c.external_reference})</li>
        ))}
      </ul>
    </div>
  )
}
