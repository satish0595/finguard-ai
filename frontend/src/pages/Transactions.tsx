import React, { useEffect, useState } from 'react'
import { deleteTransaction, listTransactions } from '../api/transactions'
import TransactionForm from '../components/TransactionForm'
import TransactionList from '../components/TransactionList'

export default function Transactions() {
  const [items, setItems] = useState<any[]>([])
  const [editing, setEditing] = useState<any | null>(null)

  async function refresh(){
    const r = await listTransactions()
    setItems(r || [])
  }

  useEffect(() => {
    refresh()
  }, [])

  async function handleDelete(id:string){
    await deleteTransaction(id)
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
      <h2>Transactions</h2>
      <TransactionForm transaction={editing || undefined} onSaved={handleSaved} onCancel={() => setEditing(null)} />
      <TransactionList items={items} onEdit={handleEdit} onDelete={handleDelete} />
    </div>
  )
}
