import React, { useEffect, useState } from 'react'
import { listTransactions } from '../api/transactions'

export default function Transactions() {
  const [items, setItems] = useState<any[]>([])

  useEffect(() => {
    listTransactions().then(r => setItems(r || []))
  }, [])

  return (
    <div className="container">
      <h2>Transactions</h2>
      <ul>
        {items.map(t => (
          <li key={t.id}>{t.amount} {t.currency} — {t.external_reference}</li>
        ))}
      </ul>
    </div>
  )
}
