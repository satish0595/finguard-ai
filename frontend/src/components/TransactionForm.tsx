import React, { useEffect, useState } from 'react'
import { createTransaction, updateTransaction } from '../api/transactions'

export default function TransactionForm({
  transaction,
  onSaved,
  onCancel,
}: {
  transaction?: any
  onSaved?: (t:any)=>void
  onCancel?: ()=>void
}){
  const [amount, setAmount] = useState('')
  const [currency, setCurrency] = useState('USD')
  const [external_reference, setExternalReference] = useState('')
  const [msg, setMsg] = useState<string | null>(null)

  useEffect(() => {
    if (transaction) {
      setAmount(String(transaction.amount ?? ''))
      setCurrency(transaction.currency || 'USD')
      setExternalReference(transaction.external_reference || '')
    } else {
      setAmount('')
      setCurrency('USD')
      setExternalReference('')
    }
  }, [transaction])

  async function submit(e: React.FormEvent){
    e.preventDefault()
    try{
      const payload = { amount: parseFloat(amount), currency, external_reference }
      const saved = transaction
        ? await updateTransaction(transaction.id, payload)
        : await createTransaction(payload)
      setMsg(transaction ? 'Updated' : 'Created')
      if (!transaction) {
        setAmount('')
        setExternalReference('')
      }
      onSaved && onSaved(saved)
    }catch(err:any){
      setMsg(err?.message || (transaction ? 'Update failed' : 'Create failed'))
    }
  }

  return (
    <form onSubmit={submit} style={{marginTop:10, border:'1px solid #ddd', padding:16, borderRadius:6}}>
      <h3>{transaction ? 'Edit Transaction' : 'New Transaction'}</h3>
      <div>
        <label>Amount</label>
        <input value={amount} onChange={e=>setAmount(e.target.value)} />
      </div>
      <div>
        <label>Currency</label>
        <input value={currency} onChange={e=>setCurrency(e.target.value)} />
      </div>
      <div>
        <label>External reference</label>
        <input value={external_reference} onChange={e=>setExternalReference(e.target.value)} />
      </div>
      <div>
        <button className="button" type="submit">{transaction ? 'Save Changes' : 'Create Transaction'}</button>
        {transaction && onCancel && (
          <button type="button" className="button" style={{marginLeft:8}} onClick={onCancel}>
            Cancel
          </button>
        )}
      </div>
      {msg && <div style={{marginTop:10}}>{msg}</div>}
    </form>
  )
}
