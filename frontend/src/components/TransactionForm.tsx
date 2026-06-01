import React, { useState } from 'react'
import { createTransaction } from '../api/transactions'

export default function TransactionForm({ onSaved }: { onSaved?: (t:any)=>void }){
  const [amount, setAmount] = useState('')
  const [currency, setCurrency] = useState('USD')
  const [external_reference, setExternalReference] = useState('')
  const [msg, setMsg] = useState<string | null>(null)

  async function submit(e: React.FormEvent){
    e.preventDefault()
    try{
      const payload = { amount: parseFloat(amount), currency, external_reference }
      const saved = await createTransaction(payload)
      setMsg('Created')
      setAmount('')
      setExternalReference('')
      onSaved && onSaved(saved)
    }catch(err:any){
      setMsg(err?.message || 'Create failed')
    }
  }

  return (
    <form onSubmit={submit} style={{marginTop:10}}>
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
        <button className="button" type="submit">Create Transaction</button>
      </div>
      {msg && <div style={{marginTop:10}}>{msg}</div>}
    </form>
  )
}
