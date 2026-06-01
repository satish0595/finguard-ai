import React, { useEffect, useState } from 'react'
import { listTransactions } from '../api/transactions'
import TransactionForm from '../components/TransactionForm'

export default function Transactions() {
  const [items, setItems] = useState<any[]>([])

  useEffect(() => {
    listTransactions().then(r => setItems(r || []))
  }, [])

  async function refresh(){
    const r = await listTransactions()
    setItems(r || [])
  }

  return (
    <div className="container">
      <h2>Transactions</h2>
      <TransactionForm onSaved={refresh} />
      <ul>
        {items.map(t => (
          <li key={t.id}>{t.amount} {t.currency} — {t.external_reference}</li>
        ))}
      </ul>
    </div>
  )
}
